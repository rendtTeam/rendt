# TODO
# * surround 'send's with try-except clauses
# * introduce threads for scalability
# * set timeout for issued tokens (permissions)
# * introduce a proper token generator; tokens must depend on user_id,
#   (e.g. hash(user_id)+randint) so that server can verify ownership

import socket
import sys, os
import logging
import random, datetime, time
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
        self.logger = self.configure_logging()

        # all following structs to be replaced when we have better token and id generation
        self.issued_db_tokens = []           # db tokens that have already been used; can't be issued again
        self.issued_job_ids = []             # job ids that have already been used; can't be issued again

    def run(self):
        self.s.listen(self.BACKLOG)           # Now wait for client connection.
        self.logger.info('Server up and running.\n')

        while True:
            # self.logger.info('waiting for connection')
            conn, addr = self.s.accept()
            try:
                Thread(target=self.serve_client, args=(conn, addr)).start()
            except:
                self.refuse_client(conn, addr)
                self.logger.error(f'Couldn\'t create thread. Refused client at {addr[0]}')
    
    def configure_logging(self):
        logger = logging.getLogger('Server.logger')
        logger.setLevel(logging.INFO)

        currentDT = str(datetime.datetime.now()).replace(' ', '_')
        file_handler = logging.FileHandler('logs/logfile_' + currentDT)
        format_ = logging.Formatter('%(asctime)s  %(name)-15s  %(levelname)-8s  %(message)s')
        
        # create console handler with a higher log level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)

        file_handler.setLevel(logging.INFO)
        console_handler.setLevel(logging.ERROR)
        console_handler.setFormatter(format_)
        file_handler.setFormatter(format_)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        logger.info('begin log')
        return logger
        
    def isTokenValid(self, authToken):
        print("valid")
        #TODO
        #check db for validity
        return True

    def serve_client(self, conn, addr):
        self.logger.info(f'Thread {threading.get_ident()} initialized to server request from {addr}')
        req_pipe = Messaging(conn, addr)
        req_pipe.read()

        if not req_pipe.jsonheader or not req_pipe.request:
            self.logger.warning(f'invalid request from {addr}.')
        else:
            self.authHandler = Authentication()
            if req_pipe.request.get('request-type') == 'sign-in':
                # check db generate token and send
                self.signInAuthToken = self.authHandler.createAuthToken()
            elif req_pipe.request.get('request-type') == 'sign-up':
                # check db add to db do sth
                self.signInAuthToken = self.authHandler.createAuthToken()
            else:
                if 'authToken' not in req_pipe.request or 'role' not in req_pipe.request or 'request-type' not in req_pipe.request:
                    self.logger.warning(f'invalid request from {addr}.')
                else:
                    if (self.isTokenValid(req_pipe.request.get('authToken'))):
                        if req_pipe.request.get('role') == 'renter':
                            self.serve_renter_request(req_pipe, conn, addr)
                        elif req_pipe.request.get('role') == 'leaser':
                            self.serve_leaser_request(req_pipe, conn, addr)
                    else:
                        # log error, send error msg
                        self.logger.warning(f'invalid request from {addr}.')

        time.sleep(30)
    
    def refuse_client(self, conn, addr):
        req_pipe = Messaging(conn, addr)
        req_pipe.read()
        response_content = {'status': 'Error: server busy, can\'t serve at the time.',
                                    }
        req_pipe.write(response_content, 'text/json')

    def serve_renter_request(self, req_pipe, conn, addr):
        header, request_content = req_pipe.jsonheader, req_pipe.request
        if request_content['request-type'] == 'submit-permission':
            self.logger.info(f'connection: renter from {addr}; request type: submit-permission')
            job_id = self.generate_job_id() # some unique id generator
            db_token = self.generate_db_token()
            job_type = request_content['file-type']
            files_size = request_content['size']

            response_content = {'status': 'success',
                                'db-token': db_token,
                                'job-id': job_id
                                }
            req_pipe.write(response_content, 'text/json')

            # add job to DB
            self.db_handler.addJob(self.get_user_id(addr[0]), job_id, job_type, files_size, db_token, status='xtbu')

            self.logger.info(f'issued permission to renter {addr[0]} to submit job {job_id} via token {db_token}')
        elif request_content['request-type'] == 'executable-upload':
            self.logger.info(f'connection: renter from {addr}; request type: executable-upload')
            if 'db-token' not in request_content or 'job-id' not in request_content:
                response_content = {'status': 'error: no permission to upload',
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.warning(f'received no token or job id from renter {addr[0]}')
                return
            
            db_token = request_content['db-token']
            job_id = request_content['job-id']

            actual_job_id = self.db_handler.getJobIdFromToken(db_token, 'x')
            if actual_job_id == job_id:
                self.recv_file(conn, f'jobs/toexec{job_id}.py')

                self.db_handler.changeJobStatus(job_id, 'a')

                response_content = {'status': 'success',
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.info(f'received file jobs/toexec{job_id}.py from renter {addr[0]}')
                return
            
            response_content = {'status': 'error: invalid token',
                                }
            req_pipe.write(response_content, 'text/json')

            self.logger.warning(f'received invalid token {db_token} for job {job_id} from renter {addr[0]}')
        elif request_content['request-type'] == 'output-download-permission':
            self.logger.info(f'connection: renter from {addr}; request type: output-download-permission')
            if 'job-id' not in request_content:
                response_content = {'status': 'error: no job id provided',
                                    }
                req_pipe.write(response_content, 'text/json')
                return
            
            requested_job_id = request_content['job-id']

            user_submitted_jobs = self.db_handler.getUserJobs(self.get_user_id(addr[0]), status='f')

            self.logger.debug('+ ' + str(user_submitted_jobs))

            if requested_job_id not in user_submitted_jobs:
                response_content = {'status': 'error: not your job',
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.warning(f'couldn\'t issue permission to renter {addr[0]} to download output of job {requested_job_id}: job doesn\'t belong to this user')
                return

            finished_jobs = self.db_handler.queryJobs(status='f')
            requested_token = self.db_handler.getOutputToken(requested_job_id)

            if requested_job_id in finished_jobs and requested_token:
                response_content = {'status': 'success',
                                    'file-size': os.path.getsize(f'outputs/output{requested_job_id}.txt'),
                                    'db-token': requested_token
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.info(f'issued permission to renter {addr[0]} to download output of job {requested_job_id} via token {requested_token}')
            else:
                response_content = {'status': f'error: no output files found for this job id {requested_job_id}',
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.warning(f'couldn\'t issue permission to renter {addr[0]} to download output of job {requested_job_id}: no output files for this job')
        elif request_content['request-type'] == 'output-download':
            self.logger.info(f'connection: renter from {addr}; request type: output-download')
            if 'db-token' not in request_content:
                response_content = {'status': 'error: no/invalid token provided',
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.warning(f'couldn\'t send output file to renter at {addr[0]}: no/invalid token')
                return
            
            db_token = request_content['db-token']
            job_id = self.db_handler.getJobIdFromToken(db_token, 'o')
            if job_id:
                requested_file_path = f'outputs/output{job_id}.txt'
                if os.path.exists(requested_file_path):
                    self.send_file(conn, requested_file_path)
                    response_content = {'status': 'success',
                                        }
                    req_pipe.write(response_content, 'text/json')
                    self.logger.info(f'sent file {requested_file_path} to renter {addr[0]}')
                    return
            
            response_content = {'status': 'error: invalid token',
                                }
            req_pipe.write(response_content, 'text/json')
            self.logger.warning(f'couldn\'t send file {requested_file_path} to renter {addr[0]}: file doesn\'t exist')
        else:
            self.logger.warning(f'connection: renter from {addr}; request type: invalid')
            response_content = {'status': 'error: unable to serve request. unknown request type',
                                }
            req_pipe.write(response_content, 'text/json')

    def serve_leaser_request(self, req_pipe, conn, addr):
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
                response_content = {'status': 'error: no job id provided',
                                    }
                req_pipe.write(response_content, 'text/json')
                return
                
            requested_job_id = request_content['job-id']
            available_jobs = self.db_handler.queryJobs(status='a')

            # get token of the requested job id
            requested_token = self.db_handler.getExecfileToken(requested_job_id)
            
            if requested_token: 
                response_content = {'status': 'success',
                                    'file-size': os.path.getsize(f'jobs/toexec{requested_job_id}.py'),
                                    'db-token': requested_token
                                    }
                req_pipe.write(response_content, 'text/json')

                # mark this job as in execution
                self.db_handler.changeJobStatus(requested_job_id, 'ix')
                
                self.logger.info(f'issued permission to leaser {addr[0]} to download executable of job {requested_job_id} via token {requested_token}')
            else:
                response_content = {'status': f'error: no files found for this job id {requested_job_id}',
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.warning(f'couldn\'t issue permission to leaser {addr[0]} to download executable of job {requested_job_id}: no files for this job')
        elif request_content['request-type'] == 'executable-download':
            self.logger.info(f'connection: leaser from {addr}; request type: executable-download')

            if 'db-token' not in request_content:
                response_content = {'status': 'error: no/invalid token provided',
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.warning(f'couldn\'t send executable file to leaser at {addr[0]}: no/invalid token')
                return

            db_token = request_content['db-token']
            job_id = self.db_handler.getJobIdFromToken(db_token, 'x')
            
            if job_id:
                requested_file_path = f'jobs/toexec{job_id}.py'
                if os.path.exists(requested_file_path):
                    self.send_file(conn, requested_file_path)
                    response_content = {'status': 'success',
                                        }
                    req_pipe.write(response_content, 'text/json')
                    self.logger.info(f'sent file {requested_file_path} to leaser {addr[0]}')
                    return

            response_content = {'status': 'error: invalid token',
                                }
            req_pipe.write(response_content, 'text/json')
            self.logger.warning(f'couldn\'t send file {requested_file_path} to leaser {addr[0]}: file doesn\'t exist')
        elif request_content['request-type'] == 'output-upload-permission':
            self.logger.info(f'connection: leaser from {addr}; request type: output-upload-permission')
            job_id = request_content['job-id']

            # TODO check if this task was assigned to be executed by this leaser. 
            # have a 'Leases' table in DB for (leaser_id, job_id, status)

            # user_jobs_in_execution = self.db_handler.getUserJobs(self.get_user_id(addr[0]), status='ix')
            # if job_id not in user_jobs_in_execution:
            #     response_content = {'status': 'error: not your job',
            #                         }
            #     req_pipe.write(response_content, 'text/json')
            #     self.logger.warning(f'couldn\'t issue permission to leaser {addr[0]} to upload output of job {job_id}: not their job')
            #     return

            db_token = self.generate_db_token()
            # so that leaser can upload the output file
            self.db_handler.addOutputFileToken(job_id, db_token)
            self.db_handler.changeJobStatus(job_id, 'otbu')

            response_content = {'status': 'success',
                                'db-token': db_token
                                }
            req_pipe.write(response_content, 'text/json')
        
            # tie this job id to its corresponding token so that the file can be accessed knowing job id            
            self.logger.info(f'issued permission to leaser {addr[0]} to upload output of job {job_id} via token {db_token}')

        elif request_content['request-type'] == 'output-upload':
            self.logger.info(f'connection: leaser from {addr}; request type: output-upload')
            if 'db-token' not in request_content or 'job-id' not in request_content:
                response_content = {'status': 'error: no permission to upload',
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.warning(f'received no token or job id from leaser {addr[0]}')
                return
            db_token = request_content['db-token']
            job_id = request_content['job-id']

            actual_job_id = self.db_handler.getJobIdFromToken(db_token, 'o')
            if actual_job_id == job_id:
                self.recv_file(conn, f'outputs/output{job_id}.txt')

                response_content = {'status': 'success',
                                    }
                req_pipe.write(response_content, 'text/json')

                self.db_handler.changeJobStatus(job_id, 'f')

                self.logger.info(f'received file outputs/output{job_id}.txt from renter {addr[0]}')
                return

            response_content = {'status': 'error: invalid token',
                                }
            req_pipe.write(response_content, 'text/json')
            self.logger.warning(f'received invalid token {db_token} for job {job_id} from leaser {addr[0]}')
        else:
            self.logger.warning(f'connection: leaser from {addr}; request type: invalid')
            response_content = {'status': 'error: unable to serve request. unknown request type',
                                }
            req_pipe.write(response_content, 'text/json')
    
    # temporary function to make user id out of host address
    def get_user_id(self, addr):
        return int(''.join(addr.split('.'))[-8:])
        
    def recv_file(self, conn, file_name): # TODO add file_size to this
        f = open(file_name,'wb')
        l = conn.recv(1024)
        while (l):
            f.write(l)
            l = conn.recv(1024)
        f.close()

    def send_file(self, conn, file_name):
        f = open(file_name, "rb")
        l = os.path.getsize(file_name)
        m = f.read(l)
        conn.send(m)
        f.close()
        # conn.shutdown(socket.SHUT_WR)

    def generate_db_token(self):
        token = int(random.random()*90000)+10000
        while token in self.issued_db_tokens:
            token = int(random.random()*90000)+10000
        self.issued_db_tokens.append(token)
        return token

    def generate_job_id(self):
        job_id = int(random.random()*9000000)+1000000
        while job_id in self.issued_job_ids:
            job_id = int(random.random()*9000000)+1000000
        self.issued_job_ids.append(job_id)
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
