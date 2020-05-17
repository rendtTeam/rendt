# TODO
# * surround 'send's with try-except clauses

import socket
import sys, os
import logging
import random
import datetime
import threading
from threading import Thread
from server_messaging import Messaging
from dbHandler import DBHandler
from authentication import Authentication

class Server:
    def __init__(self, port):
        self.BACKLOG = 1024      # size of the queue for pending connections

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', port))          # Bind to the port

        self.db_handler = DBHandler()
        self.auth = Authentication()
        self.logger = self.configure_logging()

    def run(self):
        self.s.listen(self.BACKLOG)           # Now wait for client connection.
        self.logger.info('Server up and running.\n')

        while True:
            conn, addr = self.s.accept()
            try:
                Thread(target=self.serve_client, args=(conn, addr)).start()
            except:
                self.refuse_client(conn, addr)
                self.logger.error(f'Couldn\'t create thread. Refused client at {addr}')

    def configure_logging(self):
        logger = logging.getLogger('Server.logger')
        logger.setLevel(logging.INFO)

        currentDT = str(datetime.datetime.now()).replace(' ', '_')
        format_ = logging.Formatter('%(asctime)s  %(name)-12s  %(levelname)-8s  %(message)s')

        # create log fle handler
        file_handler = logging.FileHandler('logs/logfile_' + currentDT)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(format_)
        # create console handler with a higher log level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(format_)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        logger.info('begin log')
        return logger

    def serve_client(self, conn, addr):
        self.logger.info(f'Thread {threading.get_ident()} initialized to server request from {addr}')
        req_pipe = Messaging(conn, addr)
        req_pipe.read()

        if not req_pipe.jsonheader or not req_pipe.request:
            self.logger.warning(f'invalid request from {addr}.')
        else:
            # self.authHandler = Authentication()
            if req_pipe.request.get('request-type') == 'sign-in':
                self.sign_in_user(req_pipe, conn, addr)
            elif req_pipe.request.get('request-type') == 'sign-up':
                self.register_user(req_pipe, conn, addr)
            else:
                if 'authToken' not in req_pipe.request or 'role' not in req_pipe.request or 'request-type' not in req_pipe.request:
                    self.logger.warning(f'invalid request from {addr}.')
                    response_content = {'status': 'error',
                                        'error-msg': 'invalid request. check that you have authToken, role and request-type in the request',
                                    }
                    req_pipe.write(response_content, 'text/json')
                else:
                    authToken = req_pipe.request.get('authToken')
                    if (self.db_handler.checkAuthToken(authToken)):
                        uid = self.db_handler.getUserIdFromAuthToken(authToken)
                        if req_pipe.request.get('role') == 'renter':
                            self.serve_renter_request(req_pipe, conn, addr, uid)
                        elif req_pipe.request.get('role') == 'leaser':
                            self.serve_leaser_request(req_pipe, conn, addr, uid)
                    else:
                        # log error, send error msg
                        self.logger.warning(f'invalid request from {addr}: no/invalid credentials')
    
    def register_user(self, req_pipe, conn, addr):
        request = req_pipe.request
        if 'email' not in request or 'password' not in request or 'user-type' not in request or 'machine-chars' not in request:
            self.logger.warning(f'could not sign up: missing field(s) in a sign up request from {addr}.')
            response_content = {'status': 'error',
                                'error-msg': 'could not sign up: some field(s) missing'
                                    }
            req_pipe.write(response_content, 'text/json')
        else:
            email, pswd, usr_type, chars = request['email'], request['password'], request['user-type'], request['machine-chars']
            res = self.auth.register_user(email, pswd)
            if res == 1:
                self.logger.warning('could not sign up: email already in use')
                response_content = {'status': 'error',
                                    'error-msg': 'could not sign up: email already in use'
                                        }
                req_pipe.write(response_content, 'text/json')
            else:       
                user_id, authToken = res         
                self.logger.info(f'successfully registered user {user_id}')
                response_content = {'status': 'success',
                                    'user-id': user_id, 
                                    'authToken': authToken,
                                    # 'user-type': usr_type
                                        }
                req_pipe.write(response_content, 'text/json')                
        
    def sign_in_user(self, req_pipe, conn, addr):
        request = req_pipe.request
        if 'email' not in request or 'password' not in request:
            self.logger.warning(f'could not sign in: missing field(s) in the request from {addr}.')
            response_content = {'status': 'error',
                                'error-msg': 'could not sign in: some field(s) missing'
                                    }
            req_pipe.write(response_content, 'text/json')
        else:
            email, pswd = request['email'], request['password']
            authToken = self.auth.sign_in_user(email, pswd)
            if authToken == 1:
                self.logger.warning(f'could not sign in: bad credentials from {addr}.')
                response_content = {'status': 'error',
                                    'error-msg': 'bad credentials'
                                        }
                req_pipe.write(response_content, 'text/json')
            else:
                user_id, user_type = self.db_handler.getUserIdAndType(email)
                self.db_handler.addAuthToken(user_id, authToken)
                self.logger.info(f'successful sign in. uid: {user_id}')
                response_content = {'status': 'success',
                                    'authToken': authToken,
                                    'user-type': user_type
                                        }
                req_pipe.write(response_content, 'text/json')                

    def refuse_client(self, conn, addr):
        req_pipe = Messaging(conn, addr)
        req_pipe.read()
        response_content = {'status': 'error',
                            'error-msg': 'Server busy, can\'t serve at the time.'
                                    }
        req_pipe.write(response_content, 'text/json')

    def serve_renter_request(self, req_pipe, conn, addr, uid):
        header, request_content = req_pipe.jsonheader, req_pipe.request
        if request_content['request-type'] == 'submit-permission':
            self.logger.info(f'connection: renter {uid} from {addr}; request type: submit-permission')
            job_id = self.generate_job_id() # some unique id generator
            db_token = self.generate_db_token()
            job_type = request_content['file-type']
            file_size = request_content['file-size']
            script_size = request_content['script-size']

            response_content = {'status': 'success',
                                'db-token': db_token,
                                'job-id': job_id
                                }
            req_pipe.write(response_content, 'text/json')

            # add job to DB
            self.db_handler.addJob(uid, job_id, job_type, file_size, script_size, db_token, status='xtbu')

            self.logger.info(f'issued permission to renter {uid} to submit job {job_id} via token {db_token}')
        elif request_content['request-type'] == 'output-download-permission':
            self.logger.info(f'connection: renter from {addr}; request type: output-download-permission')
            if 'job-id' not in request_content:
                response_content = {'status': 'error',
                                    'error-msg': 'no job id provided'
                                    }
                req_pipe.write(response_content, 'text/json')
                return
            
            requested_job_id = request_content['job-id']
            user_submitted_jobs = self.db_handler.getUserJobs(uid, status='f')

            if requested_job_id not in user_submitted_jobs:
                response_content = {'status': 'error',
                                    'error-msg': 'not your job'
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.warning(f'couldn\'t issue permission to renter {uid} to download output of job {requested_job_id}: job doesn\'t belong to this user')
                return

            finished_jobs = self.db_handler.queryJobs(status='f')
            requested_token = self.db_handler.getOutputToken(requested_job_id)

            if requested_job_id in finished_jobs and requested_token:
                file_size = self.db_handler.getOutputFileSize(requested_job_id)
                response_content = {'status': 'success',
                                    'file-size': file_size, 
                                    'db-token': requested_token
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.info(f'issued permission to renter {uid} to download output of job {requested_job_id} via token {requested_token}')
            else:
                response_content = {'status': 'error',
                                    'error-msg': 'no output files found for this job id'
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.warning(f'couldn\'t issue permission to renter {uid} to download output of job {requested_job_id}: no output files for this job')
        else:
            self.logger.warning(f'connection: renter {uid} from {addr}; request type: invalid')
            response_content = {'status': 'error',
                                'error-msg': 'unable to serve request. unknown request type'
                                }
            req_pipe.write(response_content, 'text/json')

    def serve_leaser_request(self, req_pipe, conn, addr, uid):
        header, request_content = req_pipe.jsonheader, req_pipe.request
        if request_content['request-type'] == 'get-available-jobs':
            self.logger.info(f'connection: leaser from {addr}; request type: get-available-jobs')
            available_jobs = self.db_handler.queryJobs(status='a')
            response_content = {'status': 'success',
                                'jobs': available_jobs,
                                }
            req_pipe.write(response_content, 'text/json')
            self.logger.info(f'available jobs sent to leaser at {addr}')
        elif request_content['request-type'] == 'execute-permission':
            self.logger.info(f'connection: leaser from {addr}; request type: execute-permission')
            if 'job-id' not in request_content:
                response_content = {'status': 'error',
                                    'error-msg': 'no job id provided'
                                    }
                req_pipe.write(response_content, 'text/json')
                return
                
            requested_job_id = request_content['job-id']
            available_jobs = self.db_handler.queryJobs(status='a')

            # get token of the requested job id
            requested_token = self.db_handler.getExecfileToken(requested_job_id)
            
            if requested_token: 
                file_size, script_size = self.db_handler.getJobFileSize(requested_job_id)
                response_content = {'status': 'success',
                                    'file-size': file_size, 
                                    'script-size': script_size,
                                    'db-token': requested_token
                                    }
                req_pipe.write(response_content, 'text/json')

                # mark this job as in execution
                self.db_handler.changeJobStatus(requested_job_id, 'ix')
                
                self.logger.info(f'issued permission to leaser {uid} to download executable of job {requested_job_id} via token {requested_token}')
            else:
                response_content = {'status': 'error',
                                    'error-msg': 'no files found for this job id'
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.warning(f'couldn\'t issue permission to leaser {uid} to download executable of job {requested_job_id}: no files for this job')
        elif request_content['request-type'] == 'output-upload-permission':
            self.logger.info(f'connection: leaser from {addr}; request type: output-upload-permission')
            job_id = request_content['job-id']
            file_size = request_content['file-size']

            # TODO check if this task was assigned to be executed by this leaser. 
            # have a 'Leases' table in DB for (leaser_id, job_id, status)

            # user_jobs_in_execution = self.db_handler.getUserJobs(self.get_user_id(addr[0]), status='ix')
            # if job_id not in user_jobs_in_execution:
            #     response_content = {'status': 'error: not your job',
            #                         }
            #     req_pipe.write(response_content, 'text/json')
            #     self.logger.warning(f'couldn\'t issue permission to leaser {checkAuthTokenAvailability]} to upload output of job {job_id}: not their job')
            #     return
            file_size = request_content['file-size']
            db_token = self.generate_db_token()
            # so that leaser can upload the output file
            self.db_handler.addOutputFileToken(job_id, db_token, file_size)
            self.db_handler.changeJobStatus(job_id, 'otbu')

            response_content = {'status': 'success',
                                'db-token': db_token
                                }
            req_pipe.write(response_content, 'text/json')
        
            # tie this job id to its corresponding token so that the file can be accessed knowing job id            
            self.logger.info(f'issued permission to leaser {uid} to upload output of job {job_id} via token {db_token}')
        else:
            self.logger.warning(f'connection: leaser from {addr}; request type: invalid')
            response_content = {'status': 'error',
                                'error-msg': 'unable to serve request. unknown request type'
                                }
            req_pipe.write(response_content, 'text/json')
     
    def generate_db_token(self):
        token = int(random.random()*90000)+10000
        while not self.db_handler.checkDBTokenAvailability(token):
            token = int(random.random()*90000)+10000
        return token

    def generate_job_id(self):
        job_id = int(random.random()*9000000)+1000000
        while not self.db_handler.checkJobIdAvailability(job_id):
            job_id = int(random.random()*9000000)+1000000
        return job_id

    def shutdown_server(self):
        self.s.close()
        self.logger.critical('Server shut down.')

def main():
    args = sys.argv[1:]
    port = int(args[0])

    server_instance = Server(port)
    server_instance.run()

if __name__ == '__main__':
    main()
