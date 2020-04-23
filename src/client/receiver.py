import socket
import os
import sys
from client_messaging import Messaging

server_addr = ('18.220.165.22', 23456)
storage_addr = ('18.197.19.248', 23456)

class Receiver:

    def get_available_jobs(self):
        global server_addr
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
        #response_header = req_pipe.jsonheader
        response = req_pipe.response

        s.close()

        if response['status'] == 'success':
            print('received list of jobs')
            return response['jobs']
        else:
            print('error: couldn\'t receive list of jobs')

    def get_permission_to_execute_task(self, job_id):
        global server_addr
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
        #response_header = req_pipe.jsonheader
        response = req_pipe.response

        s.close()

        if response['status'] == 'success':
            print('received db token')
            return response['db-token'], response['file-size']

    def download_file_from_db(self, path_to_file, db_token, file_size):
        global storage_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(storage_addr)

        content = { 'role': 'leaser',
                    'request-type': 'executable-download',
                    'db-token': db_token
                    }
        request = { 'type' : 'text/json',
                    'content': content
                    }

        req_pipe = Messaging(s, storage_addr, request)
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

    def execute_job(self, path_to_executable, path_to_output):
        # execute job
        q = os.system(f'python {path_to_executable} >> {path_to_output}')

    def get_permission_to_upload_output(self, job_id, path_to_file):
        global server_addr
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
        #response_header = req_pipe.jsonheader
        response = req_pipe.response

        s.close()

        if response['status'] == 'success':
            print('received db token')
            return response['db-token']

    def upload_output_to_db(self, path_to_file, job_id, db_token):
        global storage_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(storage_addr)

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

        req_pipe = Messaging(s, storage_addr, request)
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
