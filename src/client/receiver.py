import socket               # Import socket module
import os
from client_messaging import Messaging

server_addr = ('18.220.165.22', 12345)

TEST_JOB_ID = 9358403

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

    print("Done receiving execution file. status:", response['status'])

    s.close()

def execute_job(path_to_executable, output_file_name):
    # execute job
    q = os.system("python3 sender_job.py >> output.txt")

def get_permission_to_upload_output(path_to_file):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_addr)

    file_size = os.path.getsize(path_to_file)

    content = {'role': 'leaser',
                'request-type': 'output-upload-permission',
                'job-id': TEST_JOB_ID,
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

def upload_output_to_db(path_to_file, db_token):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_addr)

    file_size = os.path.getsize(path_to_file)

    content = { 'role': 'leaser',
                'request-type': 'output-upload',
                'file-size': file_size,
                'file-type': 'txt',
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

    print(response_header, response, req_pipe.request)

    s.close()

db_token, size = get_permission_to_execute_task(TEST_JOB_ID)
if db_token:
    download_file_from_db('sender_job.py', db_token, size)
    execute_job('sender_job.py', f'output{db_token}.txt')
    output_db_token = get_permission_to_upload_output('output.txt')
    upload_output_to_db('output.txt', output_db_token)



# # send result to server
# f = open('output.txt','rb')
# l = f.read(1024)
# while (l):
#     s.send(l)
#     l = f.read(1024)
# f.close()
# print ("Done Sending output file")
# s.shutdown(socket.SHUT_WR)
#
# s.close()                     # Close the socket when done
