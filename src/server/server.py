# TODO
# * surround 'send's with try-except clauses
# * introduce threads for scalability
# * set timeout for issued tokens (permissions)

import socket
import sys
import os
import logging
import selectors
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

        # all following structs to be replaced by the db
        self.jobs_to_execfile_tokens = {}    # maps job ids to corresponding database tokens (executables)
        self.jobs_to_output_tokens = {}      # maps job ids to corresponding database tokens (outputs)
        self.issued_db_tokens = []           # db tokens that have already been used; can't be issued again
        self.issued_job_ids = []             # job ids that have already been used; can't be issued again
        self.user_execfile_tokens = {}       # stores tokens that have been issued to a user to upload exec files
        self.user_output_tokens = {}         # stores tokens that have been issued to a user to upload output files
        self.available_jobs = []             # all jobs available for execution
        self.jobs_in_execution = []          # all jobs currently in execution
        self.finished_jobs = []              # all jobs have been executed
        self.execfile_db = {}                # maps db tokens to job_ids (to access execfiles)
        self.output_db = {}                  # maps db tokens to job_ids (to access outputs)

        self.user_submitted_jobs = {}        # dict of jobs submitted by users
        self.user_jobs_in_execution = {}         # dict of jobs that are being executed by users


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
                # self.logger.info(f'connection: renter from {addr}')
                self.serve_renter_request(req_pipe, conn, addr)
            elif req_pipe.request.get('role') == 'leaser':
                # self.logger.info(f'connection: leaser from {addr}')
                self.serve_leaser_request(req_pipe, conn, addr)
                
    def configure_logging(self):
        logger = logging.getself.logger('Serverself.logger')
        logger.setLevel(logging.INFO)

        currentDT = str(datetime.datetime.now()).replace(' ', '_')
        file_handler = logging.FileHandler('logs/logfile_' + currentDT)
        format_ = logging.Formatter('%(asctime)s  %(name)-12s  %(levelname)-8s  %(message)s')
        
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(format_)
        logger.addHandler(file_handler)

        logger.info('begin log')
        return logger

    def serve_renter_request(self, req_pipe, conn, addr):
        header, request_content = req_pipe.jsonheader, req_pipe.request
        if request_content['request-type'] == 'submit-permission':
            self.logger.info(f'connection: renter from {addr}; request type: submit-permission')
            job_id = self.generate_job_id() # some unique id generator
            db_token = self.generate_db_token()
            self.execfile_db[db_token] = job_id

            # authorize user to use this token
            if addr[0] in self.user_execfile_tokens:
                self.user_execfile_tokens[addr[0]].append(db_token)
            else:
                self.user_execfile_tokens[addr[0]] = [db_token]

            response_content = {'status': 'success',
                                'db-token': db_token,
                                'job-id': job_id
                                }
            req_pipe.write(response_content, 'text/json')

            # tie this job id to its corresponding token so that the file can be accessed knowing job id
            self.jobs_to_execfile_tokens[job_id] = db_token

            self.logger.info(f'issued permission to renter {addr[0]} to submit job {job_id} via token {db_token}')
        elif request_content['request-type'] == 'executable-upload':
            self.logger.info(f'connection: renter from {addr}; request type: executable-upload')
            if addr[0] not in self.user_execfile_tokens or 'db-token' not in request_content or 'job-id' not in request_content:
                response_content = {'status': 'error: no permission to upload',
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.warning(f'received no token or job id from renter {addr[0]}')
                return
            
            db_token = request_content['db-token']
            job_id = request_content['job-id']

            if db_token in self.user_execfile_tokens[addr[0]]: # if db_token really belongs to this user
                if self.execfile_db[db_token] == job_id:
                    self.recv_file(conn, f'jobs/toexec{job_id}.py')                
                    # add job to the list of jobs by this user
                    if addr[0] in self.user_submitted_jobs:
                        self.user_submitted_jobs[addr[0]].append(job_id)
                    else:
                        self.user_submitted_jobs[addr[0]] = [job_id]
                    # add job to the db of available
                    self.available_jobs.append(job_id)

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

            if requested_job_id not in self.user_submitted_jobs[addr[0]]:
                response_content = {'status': 'error: not your job',
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.warning(f'couldn\'t issue permission to renter {addr[0]} to download output of job {requested_job_id} via token {self.jobs_to_output_tokens[requested_job_id]}: invalid token')
                return

            if requested_job_id in self.finished_jobs and requested_job_id in self.jobs_to_output_tokens:
                response_content = {'status': 'success',
                                    'file-size': os.path.getsize(f'outputs/output{requested_job_id}.txt'),
                                    'db-token': self.jobs_to_output_tokens[requested_job_id]
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.info(f'issued permission to renter {addr[0]} to download output of job {requested_job_id} via token {self.jobs_to_output_tokens[requested_job_id]}')
            else:
                response_content = {'status': f'error: no files found for this job id {requested_job_id}',
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.warning(f'couldn\'t issue permission to renter {addr[0]} to download output of job {requested_job_id} via token {self.jobs_to_output_tokens[requested_job_id]}: no files for this job')
        elif request_content['request-type'] == 'output-download':
            self.logger.info(f'connection: renter from {addr}; request type: output-download')
            if 'db-token' not in request_content or request_content['db-token'] not in self.output_db:
                response_content = {'status': 'error: no/invalid token provided',
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.warning(f'couldn\'t send output file to renter at {addr[0]}: no/invalid token')
                return
            
            db_token = request_content['db-token']
            requested_file_path = f'outputs/output{self.output_db[db_token]}.txt'
            if os.path.exists(requested_file_path):
                self.send_file(conn, requested_file_path)
                response_content = {'status': 'success',
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.info(f'sent file {requested_file_path} to renter {addr[0]}')
            else:
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
            available_jobs = self.get_available_jobs()
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
            available_jobs = self.get_available_jobs()

            # TODO we can delegate the first condition check below to DB, which would be much much more efficient 
            if requested_job_id in available_jobs and requested_job_id in self.jobs_to_execfile_tokens: 
                response_content = {'status': 'success',
                                    'file-size': os.path.getsize(f'jobs/toexec{requested_job_id}.py'),
                                    'db-token': self.jobs_to_execfile_tokens[requested_job_id]
                                    }
                req_pipe.write(response_content, 'text/json')
                # mark job unavailable

                # TODO mark this job as in execution
                self.available_jobs.remove(requested_job_id)
                self.jobs_in_execution.append(requested_job_id)
                
                # mark this job being executed by this leaser, so that he can later obtain permission to submit its outputs
                if addr[0] in self.user_jobs_in_execution:
                    self.user_jobs_in_execution[addr[0]].append(requested_job_id)
                else:
                    self.user_jobs_in_execution[addr[0]] = [requested_job_id]
                self.logger.info(f'issued permission to leaser {addr[0]} to download executable of job {requested_job_id} via token {self.jobs_to_execfile_tokens[requested_job_id]}')
            else:
                response_content = {'status': f'error: no files found for this job id {requested_job_id}',
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.warning(f'couldn\'t issue permission to leaser {addr[0]} to download output of job {requested_job_id} via token {self.jobs_to_execfile_tokens[requested_job_id]}: no files for this job')
        elif request_content['request-type'] == 'executable-download':
            self.logger.info(f'connection: leaser from {addr}; request type: executable-download')
            if 'db-token' not in request_content or request_content['db-token'] not in self.execfile_db:
                response_content = {'status': 'error: no/invalid token provided',
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.warning(f'couldn\'t send executable file to leaser at {addr[0]}: no/invalid token')
                return

            db_token = request_content['db-token']
            requested_file_path = f'jobs/toexec{self.execfile_db[db_token]}.py'
            if os.path.exists(requested_file_path):
                self.send_file(conn, requested_file_path)
                response_content = {'status': 'success',
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.info(f'sent file {requested_file_path} to leaser {addr[0]}')
            else:
                response_content = {'status': 'error: invalid token',
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.warning(f'couldn\'t send file {requested_file_path} to leaser {addr[0]}: file doesn\'t exist')
        elif request_content['request-type'] == 'output-upload-permission':
            self.logger.info(f'connection: leaser from {addr}; request type: output-upload-permission')
            job_id = request_content['job-id']
            if addr[0] not in self.user_jobs_in_execution or job_id not in self.user_jobs_in_execution[addr[0]]:
                response_content = {'status': 'error: not your job',
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.warning(f'couldn\'t issue permission to leaser {addr[0]} to upload output of job {job_id}: not their job')
                return

            db_token = self.generate_db_token()
            self.output_db[db_token] = job_id # so that leaser can upload the output file

            # authorize user to use this token
            if addr[0] in self.user_output_tokens:
                self.user_output_tokens[addr[0]].append(db_token)
            else:
                self.user_output_tokens[addr[0]] = [db_token]

            response_content = {'status': 'success',
                                'db-token': db_token
                                }
            req_pipe.write(response_content, 'text/json')
        
            # tie this job id to its corresponding token so that the file can be accessed knowing job id
            self.jobs_to_output_tokens[job_id] = db_token
            self.logger.info(f'issued permission to leaser {addr[0]} to upload output of job {job_id} via token {db_token}')

        elif request_content['request-type'] == 'output-upload':
            self.logger.info(f'connection: leaser from {addr}; request type: output-upload')
            if addr[0] not in self.user_output_tokens or 'db-token' not in request_content or 'job-id' not in request_content:
                response_content = {'status': 'error: no permission to upload',
                                    }
                req_pipe.write(response_content, 'text/json')
                self.logger.warning(f'received no token or job id from leaser {addr[0]}')
                return
            db_token = request_content['db-token']
            job_id = request_content['job-id']

            if db_token in self.user_output_tokens[addr[0]]: # if db_token really belongs to this user
                if self.output_db[db_token] == job_id:
                    recv_file(conn, f'outputs/output{job_id}.txt')

                    response_content = {'status': 'success',
                                        }
                    req_pipe.write(response_content, 'text/json')
                    self.jobs_to_output_tokens[job_id] = db_token
                    self.jobs_in_execution.remove(job_id)
                    self.finished_jobs.append(job_id)

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

    # TODO pull from DB
    def get_available_jobs(self):
        return self.available_jobs

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
