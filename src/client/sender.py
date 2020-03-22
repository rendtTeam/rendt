import socket
from client_messaging import Messaging
import os
import sys
import time

server_addr = ('18.220.165.22', 23456)

def get_permission_to_submit_task(path_to_file):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_addr)

    file_size = os.path.getsize(path_to_file)

    content = {'role': 'renter',
                'request-type': 'submit-permission',
                'file-size': file_size,
                'file-type': 'py'}
    request = {'type' : 'text/json',
                'content': content}
    request_pipe = Messaging(s, server_addr, request)
    request_pipe.queue_request()
    request_pipe.write()

    request_pipe.read()
    response_header = request_pipe.jsonheader
    response = request_pipe.response

    s.close()

    if response['status'] == 'success':
        print('received db token')
        return response['job-id'], response['db-token']

def upload_file_to_db(path_to_file, job_id, db_token):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_addr)

    file_size = os.path.getsize(path_to_file)

    content = { 'role': 'renter',
                'request-type': 'executable-upload',
                'file-size': file_size,
                'file-type': 'py',
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

    print('- server response:', response_header, response['status'])

    s.close()

def get_permission_to_download_output(job_id):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_addr)

    content = {'role': 'renter',
                'request-type': 'output-download-permission',
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

def download_output_from_db(path_to_file, db_token, file_size):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_addr)

    content = { 'role': 'renter',
                'request-type': 'output-download',
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

    print("- receiving output file status:", response['status'])

    s.close()

# job_id, db_token = get_permission_to_submit_task('/Users/m4hmmd/Desktop/senior/base_server_test/sender/exec_test.py')
# upload_file_to_db('/Users/m4hmmd/Desktop/senior/base_server_test/sender/exec_test.py', job_id, db_token)

# time.sleep(10)

# output_db_token, file_size = get_permission_to_download_output(job_id)
# download_output_from_db('received_output.txt', output_db_token, file_size )

def main():

    while True:
        arg = input('command: ')
        if arg == 'exit':
            break
        if arg == 'send-perm':
            job_id, db_token = get_permission_to_submit_task('/Users/m4hmmd/Desktop/senior/base_server_test/sender/exec_test.py')
            print('job_id, db_token:', job_id, db_token)
        if arg == 'send-up':
            job_id, db_token = int(input('job-id ')), int(input('db-token '))
            upload_file_to_db('/Users/m4hmmd/Desktop/senior/base_server_test/sender/exec_test.py', job_id, db_token)
        if arg == 'down-perm':
            job_id = int(input('job-id '))
            permission = get_permission_to_download_output(job_id)
            if permission:
                output_db_token, file_size = permission
                print('output_db_token, file_size:', output_db_token, file_size)
            else:
                print('error: didn\'t receive db token')
        if arg == 'down':
            output_db_token, file_size = int(input('db-token ')), int(input('file-size '))
            download_output_from_db('received_output.txt', output_db_token, file_size)
        
if __name__ == '__main__':
    main()
