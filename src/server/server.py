# TODO
# * create a log file, log timestamped actions
# * surround 'send's with try-except clauses
# * replace selectors with threads for scalability

import socket
import sys
import os
import selectors
import random
from server_messaging import Messaging

BACKLOG = 1024      # size of the queue for pending connections

s = None            # main socket object

# all following structs to be replaced by the db
jobs_to_execfile_tokens = {}    # maps job ids to corresponding database tokens (executables)
jobs_to_output_tokens = {}      # maps job ids to corresponding database tokens (outputs)
issued_db_tokens = []           # db tokens that have already been used; can't be issued again
issued_job_ids = []             # job ids that have already been used; can't be issued again
user_execfile_tokens = {}       # stores tokens that have been issued to a user to upload exec files
user_output_tokens = {}         # stores tokens that have been issued to a user to upload output files
available_jobs = []             # all jobs available for execution
jobs_in_execution = []          # all jobs currently in execution
finished_jobs = []              # all jobs have been executed
execfile_db = {}                # maps db tokens to job_ids (to access execfiles)
output_db = {}                  # maps db tokens to job_ids (to access outputs)

user_submitted_jobs = {}        # dict of jobs submitted by users
user_jobs_in_execution = {}         # dict of jobs that are being executed by users

def init_server(port):
    global s
    global sel

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sel = selectors.DefaultSelector()
    # port = 12345                # Reserve a port for your service.
    s.bind(('', port))          # Bind to the port
    s.listen(BACKLOG)           # Now wait for client connection.
    print('Server up and running.')

    while True:
        print('\nwaiting for connection')
        conn, addr = s.accept()
        req_pipe = Messaging(conn, addr)
        req_pipe.read()

        if 'role' not in req_pipe.request:
            print(f'got invalid connection at {addr}. ignored.')
        if req_pipe.request.get('role') == 'renter':
            print(f'got connection from renter at {addr}')
            serve_renter_request(req_pipe, conn, addr)
        elif req_pipe.request.get('role') == 'leaser':
            print(f'got connection from receiver at {addr}')
            serve_leaser_request(req_pipe, conn, addr)
            

def serve_renter_request(req_pipe, conn, addr):
    header, request_content = req_pipe.jsonheader, req_pipe.request
    if request_content['request-type'] == 'submit-permission':
        job_id = generate_job_id() # some unique id generator
        db_token = generate_db_token()
        execfile_db[db_token] = job_id

        # authorize user to use this token
        if addr[0] in user_execfile_tokens:
            user_execfile_tokens[addr[0]].append(db_token)
        else:
            user_execfile_tokens[addr[0]] = [db_token]

        response_content = {'status': 'success',
                            'db-token': db_token,
                            'job-id': job_id
                            }
        req_pipe.write(response_content, 'text/json')

        # tie this job id to its corresponding token so that the file can be accessed knowing job id
        jobs_to_execfile_tokens[job_id] = db_token
    elif request_content['request-type'] == 'executable-upload':
        if addr[0] not in user_execfile_tokens or 'db-token' not in request_content:
            response_content = {'status': 'error: no permission to upload',
                                }
            req_pipe.write(response_content, 'text/json')
            return
        db_token = request_content['db-token']
        job_id = request_content['job-id']

        if db_token in user_execfile_tokens[addr[0]]: # if db_token really belongs to this user
            if execfile_db[db_token] == job_id:
                recv_file(conn, f'jobs/toexec{job_id}.py')
                
                # add job to the list of jobs by this user
                if addr[0] in user_submitted_jobs:
                    user_submitted_jobs[addr[0]].append(job_id)
                else:
                    user_submitted_jobs[addr[0]] = [job_id]
                # add job to the db of available
                available_jobs.append(job_id)

                response_content = {'status': 'success',
                                    }
                req_pipe.write(response_content, 'text/json')
                return
        
        response_content = {'status': 'error: invalid token',
                            }
        req_pipe.write(response_content, 'text/json')
    elif request_content['request-type'] == 'output-download-permission':
        requested_job_id = request_content['job-id']

        if requested_job_id not in user_submitted_jobs[addr[0]]:
            response_content = {'status': 'error: not your job',
                                }
            req_pipe.write(response_content, 'text/json')
            return
        # TODO check if available
        if requested_job_id in finished_jobs and requested_job_id in jobs_to_output_tokens:
            response_content = {'status': 'success',
                                'file-size': os.path.getsize(f'outputs/output{requested_job_id}.txt'),
                                'db-token': jobs_to_output_tokens[requested_job_id]
                                }
            req_pipe.write(response_content, 'text/json')
        else:
            response_content = {'status': f'error: no files found for this job id {requested_job_id}',
                                }
            req_pipe.write(response_content, 'text/json')
    elif request_content['request-type'] == 'output-download':
        db_token = request_content['db-token']
        requested_file_path = f'outputs/output{output_db[db_token]}.txt'
        if os.path.exists(requested_file_path):
            send_file(conn, requested_file_path)
            print('file sent to sender')

            response_content = {'status': 'success',
                                }
            req_pipe.write(response_content, 'text/json')
        else:
            response_content = {'status': 'error: invalid token',
                                }
            req_pipe.write(response_content, 'text/json')
    else:
        response_content = {'status': 'error: unable to serve request. unknown request type',
                            }
        req_pipe.write(response_content, 'text/json')

def serve_leaser_request(req_pipe, conn, addr):
    header, request_content = req_pipe.jsonheader, req_pipe.request
    if request_content['request-type'] == 'get-available-jobs':
        response_content = {'status': 'success',
                            'jobs': available_jobs,
                            }
        req_pipe.write(response_content, 'text/json')
    elif request_content['request-type'] == 'execute-permission':
        requested_job_id = request_content['job-id']

        # TODO check if availabe
        if requested_job_id in available_jobs and requested_job_id in jobs_to_execfile_tokens:
            response_content = {'status': 'success',
                                'file-size': os.path.getsize(f'jobs/toexec{requested_job_id}.py'),
                                'db-token': jobs_to_execfile_tokens[requested_job_id]
                                }
            req_pipe.write(response_content, 'text/json')
            # mark job unavailable
            available_jobs.remove(requested_job_id)
            jobs_in_execution.append(requested_job_id)
            # mark this job being executed by this leaser, so that he can later obtain permission to submit its outputs
            if addr[0] in user_jobs_in_execution:
                user_jobs_in_execution[addr[0]].append(requested_job_id)
            else:
                user_jobs_in_execution[addr[0]] = [requested_job_id]
        else:
            response_content = {'status': f'error: no files found for this job id {requested_job_id}',
                                }
            req_pipe.write(response_content, 'text/json')
    elif request_content['request-type'] == 'executable-download':
        db_token = request_content['db-token']
        requested_file_path = f'jobs/toexec{execfile_db[db_token]}.py'
        if os.path.exists(requested_file_path):
            send_file(conn, requested_file_path)
            print('file sent to receiver')

            response_content = {'status': 'success',
                                }
            req_pipe.write(response_content, 'text/json')
        else:
            response_content = {'status': 'error: invalid token',
                                }
            req_pipe.write(response_content, 'text/json')

    elif request_content['request-type'] == 'output-upload-permission':
        job_id = request_content['job-id']
        if addr[0] not in user_jobs_in_execution or job_id not in user_jobs_in_execution[addr[0]]:
            response_content = {'status': 'error: not your job',
                                }
            req_pipe.write(response_content, 'text/json')
            return

        db_token = generate_db_token()
        output_db[db_token] = job_id # so that leaser can upload the output file

        # authorize user to use this token
        if addr[0] in user_output_tokens:
            user_output_tokens[addr[0]].append(db_token)
        else:
            user_output_tokens[addr[0]] = [db_token]

        response_content = {'status': 'success',
                            'db-token': db_token
                            }
        req_pipe.write(response_content, 'text/json')
    
        # tie this job id to its corresponding token so that the file can be accessed knowing job id
        jobs_to_output_tokens[job_id] = db_token

    elif request_content['request-type'] == 'output-upload':
        if addr[0] not in user_output_tokens or 'db-token' not in request_content:
            response_content = {'status': 'error: no permission to upload',
                                }
            req_pipe.write(response_content, 'text/json')
            return
        db_token = request_content['db-token']
        job_id = request_content['job-id']

        if db_token in user_output_tokens[addr[0]]: # if db_token really belongs to this user
            if output_db[db_token] == job_id:
                recv_file(conn, f'outputs/output{job_id}.txt')

                response_content = {'status': 'success',
                                    }
                req_pipe.write(response_content, 'text/json')
                jobs_to_output_tokens[job_id] = db_token

                jobs_in_execution.remove(job_id)
                finished_jobs.append(job_id)
                return
        response_content = {'status': 'error: invalid token',
                            }
        req_pipe.write(response_content, 'text/json')
    else:
        response_content = {'status': 'error: unable to serve request. unknown request type',
                            }
        req_pipe.write(response_content, 'text/json')

def recv_file(conn, file_name): # TODO add file_size to this
    f = open(file_name,'wb')
    l = conn.recv(1024)
    while (l):
        f.write(l)
        l = conn.recv(1024)
    f.close()

def send_file(conn, file_name):
    f = open(file_name, "rb")
    l = os.path.getsize(file_name)
    m = f.read(l)
    conn.send(m)
    f.close()
    # conn.shutdown(socket.SHUT_WR)

def generate_db_token():
    token = int(random.random()*90000)+10000
    while token in issued_db_tokens:
        token = int(random.random()*90000)+10000
    issued_db_tokens.append(token)
    return token

def generate_job_id():
    job_id = int(random.random()*9000000)+1000000
    while job_id in issued_job_ids:
        job_id = int(random.random()*9000000)+1000000
    issued_job_ids.append(job_id)
    return job_id

def test():
    # Server receives file from renter
    c_send, addr_send = s.accept()     # Establish connection with client.
    print ('Got connection from renter:', addr_send)
    recv_file(c_send, 'toexec.py')
    print('file recevied from renter')

    # Server sends file to receiver
    c_rec, addr_rec = s.accept()
    print('Got connection from receiver:', addr_rec)
    send_file(c_rec, 'toexec.py')
    print('file sent to receiver')

    # Server receives output from receiver
    print('receiving file from receiver')
    recv_file(c_rec, 'output.txt')
    print('output file received from receiver')

    # Server sends output to renter
    print('sending output file to renter')
    send_file(c_send, 'output.txt')
    print('output file send to renter')

    # close servers
    c_rec.close()
    c_send.close()

def shutdown_server():
    s.close()
    print('Server shut down.')

def main():
    args = sys.argv[1:]
    port = int(args[0])
    init_server(port)
    # test()

if __name__ == '__main__':
    main()
