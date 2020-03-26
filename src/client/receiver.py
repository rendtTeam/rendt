import socket
import os
import sys
from client_messaging import Messaging

server_addr = ('18.220.165.22', 23456)

def get_available_jobs():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_addr)

    content = {'role': 'leaser',
                'request-type': 'get-available-jobs',
                }
    request = {'type' : 'text/json',
                'content': content}

    req_pipe = Messaging(s, server_addr, request)
    req_pipe.queue_request()
    req_pipe.write()

    req_pipe.read()
    response_header = req_pipe.jsonheader
    response = req_pipe.response

    s.close()

    if response['status'] == 'success':
        print('received list of jobs')
        return response['jobs']
    else:
        print('error: couldn\'t receive list of jobs')

def get_permission_to_execute_task(job_id):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_addr)

    content = {'role': 'leaser',
                'request-type': 'execute-permission',
                'job-id': job_id}
    request = {'type' : 'text/json',
                'content': content}

    req_pipe = Messaging(s, server_addr, request)
    req_pipe.queue_request()
    req_pipe.write()

    req_pipe.read()
    response_header = req_pipe.jsonheader
    response = req_pipe.response

    s.close()

    if response['status'] == 'success':
        print('received db token')
        return response['db-token'], response['file-size']

def download_file_from_db(path_to_file, db_token, file_size):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_addr)

    content = { 'role': 'leaser',
                'request-type': 'executable-download',
                'db-token': db_token
                }
    request = { 'type' : 'text/json',
                'content': content
                }

    req_pipe = Messaging(s, server_addr, request)
    req_pipe.queue_request()
    req_pipe.write()

    # receive exec file
    f = open(path_to_file, "wb")
    data = None
    while True:
        received = 0
        chunk = min(1024, file_size-received)
        m = s.recv(chunk)
        data = m
        received += chunk
        while received < file_size:
            # break
            m = s.recv(chunk)
            data += m
            received += chunk
        break
    f.write(data)
    f.close()

    req_pipe.read()
    response_header = req_pipe.jsonheader
    response = req_pipe.response

    print("- receiving execution file status:", response['status'])

    s.close()

def execute_job(path_to_executable, path_to_output):
    # execute job
    q = os.system(f'python3 {path_to_executable} >> {path_to_output}')

def get_permission_to_upload_output(job_id, path_to_file):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_addr)

    file_size = os.path.getsize(path_to_file)

    content = {'role': 'leaser',
                'request-type': 'output-upload-permission',
                'job-id': job_id,
                'file-size': file_size,
                'file-type': 'txt'}
    request = {'type' : 'text/json',
                'content': content}
    req_pipe = Messaging(s, server_addr, request)
    req_pipe.queue_request()
    req_pipe.write()

    req_pipe.read()
    response_header = req_pipe.jsonheader
    response = req_pipe.response

    s.close()

    if response['status'] == 'success':
        print('received db token')
        return response['db-token']

def upload_output_to_db(path_to_file, job_id, db_token):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_addr)

    file_size = os.path.getsize(path_to_file)

    content = { 'role': 'leaser',
                'request-type': 'output-upload',
                'file-size': file_size,
                'file-type': 'txt',
                'job-id': job_id,
                'db-token': db_token
                }
    request = { 'type' : 'text/json',
                'content': content
                }

    req_pipe = Messaging(s, server_addr, request)
    req_pipe.queue_request()
    req_pipe.write()

    # send exec file
    f = open(path_to_file,'rb')
    l = f.read(1024)
    while (l):
        s.send(l)
        l = f.read(1024)
    f.close()
    print ('Done Sending')
    s.shutdown(socket.SHUT_WR)

    req_pipe.read()
    response_header = req_pipe.jsonheader
    response = req_pipe.response

    print('- uploading output file status:', response['status'])

    s.close()

# available_jobs = get_available_jobs()
# if len(available_jobs) == 0:
#     print('error: no available jobs.')
# else:
#     job_id = available_jobs[0]
#     db_token, size = get_permission_to_execute_task(job_id)
#     if db_token:
#         download_file_from_db('sender_job.py', db_token, size)
#         execute_job('sender_job.py', f'sender_output.txt')
#         output_db_token = get_permission_to_upload_output(job_id, 'sender_output.txt')
#         upload_output_to_db('sender_output.txt', job_id, output_db_token)

def main():
    
    while True:
        arg = input('command ')

        if arg == 'exit':
            break
        if arg == 'get':
            available_jobs = get_available_jobs()
            print('available jobs:', available_jobs)
        if arg == 'exec-perm':
            job_id = int(input('job-id '))
            db_token, size = get_permission_to_execute_task(job_id)
            print('db token, size:', db_token, size)
        if arg == 'exec-down':
            db_token, size = int(input('db-token ')), int(input('size '))
            download_file_from_db('sender_job.py', db_token, size)
        if arg == 'exec':
            if os.path.exists('sender_job.py'):
                execute_job('sender_job.py', f'sender_output.txt')
            else:
                print('exec file doesn\'t exist')
        if arg == 'out-perm':
            if os.path.exists('sender_output.txt'):
                job_id = int(input('job-id '))
                output_db_token = get_permission_to_upload_output(job_id, 'sender_output.txt')
                print('output db token:', output_db_token)
            else:
                print('output file doesn\'t exist')
        if arg == 'out-up':
            job_id, output_db_token = int(input('job-id ')), int(input('db-token '))
            upload_output_to_db('sender_output.txt', job_id, output_db_token)

if __name__ == '__main__':
    main()

