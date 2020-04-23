# TODO
# * surround 'send's with try-except clauses
# * introduce threads for scalability
# * set timeout for issued tokens (permissions)
# * introduce a proper token generator; tokens must depend on user_id,
#   (e.g. hash(user_id)_randint) so that server can verify ownership

# TODO migrate upload/download functions (not permissions) to storage.py

import socket
import sys
import os
import logging
import random
import datetime
from server_messaging import Messaging
from dbHandler import DBHandler

class Server:

    def __init__(self, port):
        self.BACKLOG = 1024      # size of the queue for pending connections

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', port))          # Bind to the port

        self.db_handler = DBHandler()
        self.logger = self.configure_logging()

        # TODO all following structs to be replaced when we have better token and id generation
        self.issued_db_tokens = []           # db tokens that have already been used; can't be issued again
        self.issued_job_ids = []             # job ids that have already been used; can't be issued again

    def run(self):
        self.s.listen(self.BACKLOG)           # Now wait for client connection.
        self.logger.info('Server up and running.\n')

        while True:
            # self.logger.info('waiting for connection')
            conn, addr = self.s.accept()
            req_pipe = Messaging(conn, addr)
            req_pipe.read()

            if not req_pipe.jsonheader or not req_pipe.request or 'role' not in req_pipe.request or 'request-type' not in req_pipe.request:
                self.logger.warning(f'invalid request from {addr}.')
            elif req_pipe.request.get('role') == 'renter':
                self.serve_renter_request(req_pipe, conn, addr)
            elif req_pipe.request.get('role') == 'leaser':
                self.serve_leaser_request(req_pipe, conn, addr)
                
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
                file_size = self.db_handler.getOutputFileSize(requested_job_id)
                response_content = {'status': 'success',
                                    'file-size': file_size, 
                                    'db-token': requested_token
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.info(f'issued permission to renter {addr[0]} to download output of job {requested_job_id} via token {requested_token}')
            else:
                response_content = {'status': f'error: no output files found for this job id {requested_job_id}',
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.warning(f'couldn\'t issue permission to renter {addr[0]} to download output of job {requested_job_id}: no output files for this job')
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
                file_size = self.db_handler.getJobFileSize(requested_job_id)
                response_content = {'status': 'success',
                                    'file-size': file_size, 
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
            #     self.logger.warning(f'couldn\'t issue permission to leaser {addr[0]} to upload output of job {job_id}: not their job')
            #     return

            db_token = self.generate_db_token()
            # so that leaser can upload the output file
            self.db_handler.addOutputFileToken(job_id, db_token, file_size)
            self.db_handler.changeJobStatus(job_id, 'otbu')

            response_content = {'status': 'success',
                                'db-token': db_token
                                }
            req_pipe.write(response_content, 'text/json')
        
            # tie this job id to its corresponding token so that the file can be accessed knowing job id            
            self.logger.info(f'issued permission to leaser {addr[0]} to upload output of job {job_id} via token {db_token}')
        else:
            self.logger.warning(f'connection: leaser from {addr}; request type: invalid')
            response_content = {'status': 'error: unable to serve request. unknown request type',
                                }
            req_pipe.write(response_content, 'text/json')
    
    # temporary function to make user id out of host address
    def get_user_id(self, addr):
        return int(''.join(addr.split('.'))[-8:])
        
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
