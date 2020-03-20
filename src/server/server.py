# TODO
# * create a log file, log timestamped actions
# * surround 'send's with try-except clauses
# * replace selectors with threads for scalability

import socket
import sys
import os
import selectors
from server_messaging import Messaging

BACKLOG = 1024      # size of the queue for pending connections

sel = None          # selector object
s = None            # main socket object

jobs = {} # to be replaced by the db
outputs = {} # to be replaced by the db

def init_server(port):
    global s
    global sel

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sel = selectors.DefaultSelector()
    # port = 12345                # Reserve a port for your service.
    s.bind(('', port))          # Bind to the port
    s.listen(BACKLOG)           # Now wait for client connection.
    print('Server up and running.')

    # while True:
    for i in range(8):
        print('waiting for connection')
        conn, addr = s.accept()
        req_pipe = Messaging(conn, addr)
        req_pipe.read()
        header, request_content = req_pipe.jsonheader, req_pipe.request

        if req_pipe.request.get('role') == 'renter':
            print(f'got connection from renter at {addr}')
            if request_content['request-type'] == 'submit-permission':
                response_content = {'status': 'success',
                                    'db-token': 12737
                                    }
                req_pipe.write(response_content, 'text/json')
            elif request_content['request-type'] == 'executable-upload':
                if request_content['db-token'] == 12737:
                    recv_file(conn, f'toexec{request_content["db-token"]}.py')
                    job_id = 9358403 # some id generator
                    response_content = {'status': 'success',
                                        'job-id': job_id
                                        }
                    req_pipe.write(response_content, 'text/json')
                    jobs[job_id] = request_content['db-token']
                else:
                    response_content = {'status': 'error: invalid token',
                                        }
                    req_pipe.write(response_content, 'text/json')
            elif request_content['request-type'] == 'output-download-permission':
                requested_job_id = request_content['job-id']

                # TODO check if availabe
                if requested_job_id in outputs:
                    response_content = {'status': 'success',
                                        'file-size': os.path.getsize(f'output{outputs[requested_job_id]}.txt'),
                                        'db-token': outputs[requested_job_id]
                                        }
                    req_pipe.write(response_content, 'text/json')
                else:
                    response_content = {'status': f'error: no files found for this job id {requested_job_id}',
                                        }
                    req_pipe.write(response_content, 'text/json')
            elif request_content['request-type'] == 'output-download':
                requested_file_path = f'output{request_content["db-token"]}.txt'
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
            else:
                response_content = {'status': 'error: unable to serve request. unknown request type',
                                    }
                req_pipe.write(response_content, 'text/json')
        elif req_pipe.request.get('role') == 'leaser':
            print(f'got connection from receiver at {addr}')
            if request_content['request-type'] == 'execute-permission':
                requested_job_id = request_content['job-id']

                # TODO check if availabe
                if requested_job_id in jobs:
                    response_content = {'status': 'success',
                                        'file-size': os.path.getsize(f'toexec{jobs[requested_job_id]}.py'),
                                        'db-token': jobs[requested_job_id]
                                        }
                    req_pipe.write(response_content, 'text/json')
                else:
                    response_content = {'status': f'error: no files found for this job id {requested_job_id}',
                                        }
                    req_pipe.write(response_content, 'text/json')
            elif request_content['request-type'] == 'executable-download':
                requested_file_path = f'toexec{request_content["db-token"]}.py'
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
                if request_content['job-id'] == 9358403:

                    response_content = {'status': 'success',
                                        'db-token': 37261
                                        }
                    req_pipe.write(response_content, 'text/json')
                else:
                    response_content = {'status': f'error: incalid job id {request_content["job-id"]}',
                                        }
                    req_pipe.write(response_content, 'text/json')
            elif request_content['request-type'] == 'output-upload':
                if request_content['db-token'] == 37261:
                    recv_file(conn, f'output{request_content["db-token"]}.txt')

                    response_content = {'status': 'success',
                                        }
                    req_pipe.write(response_content, 'text/json')
                    outputs[job_id] = request_content['db-token']
                else:
                    response_content = {'status': 'error: invalid token',
                                        }
                    req_pipe.write(response_content, 'text/json')
            else:
                response_content = {'status': 'error: unable to serve request. unknown request type',
                                    }
                req_pipe.write(response_content, 'text/json')



def recv_file(conn, file_name):
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



# https://stackoverflow.com/questions/27241804/sending-a-file-over-tcp-sockets-in-python
