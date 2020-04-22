import socket
from client_messaging import Messaging
import os
import sys
import time

server_addr = ('18.220.165.22', 23457)
storage_addr = ('18.197.19.248', 23456)
class Sender:
    def get_permission_to_submit_task(self, path_to_file):
        global server_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(server_addr)

        file_size = os.path.getsize(path_to_file)

        content = {'role': 'renter',
                    'request-type': 'submit-permission',
                    'size': file_size,
                    'file-type': 'py'}
        request = {'type' : 'text/json',
                    'content': content}
        request_pipe = Messaging(s, server_addr, request)
        request_pipe.queue_request()
        request_pipe.write()

        request_pipe.read()
        #response_header = request_pipe.jsonheader
        response = request_pipe.response

        s.close()

        if response['status'] == 'success':
            print('received db token')
            return response['job-id'], response['db-token']

    def upload_file_to_db(self,path_to_file, job_id, db_token):
        global server_addr
        global storage_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(server_addr)
        s1.connect(storage_addr)

        file_size = os.path.getsize(path_to_file)

        content = { 'role': 'renter',
                    'request-type': 'executable-upload',
                    'job-id': job_id,
                    'db-token': db_token
                    }
        request = { 'type' : 'text/json',
                    'content': content
                    }

        req_pipe = Messaging(s, server_addr, request)
        req_pipe.queue_request()
        req_pipe.write()

        req_pipe1 = Messaging(s1, storage_addr, request)
        req_pipe1.queue_request()
        req_pipe1.write()

        # send exec file
        f = open(path_to_file,'rb')
        l = f.read(1024)
        while (l):
            s1.send(l)
            l = f.read(1024)
        f.close()
        print ('Done Sending')
        s1.shutdown(socket.SHUT_WR)

        req_pipe.read()
        response_header = req_pipe.jsonheader
        response = req_pipe.response

        req_pipe1.read()

        print('- server response:', response_header, response['status'])

        s.close()
        s1.close()

    def get_permission_to_download_output(self, job_id):
        global server_addr
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
        #response_header = req_pipe.jsonheader
        response = req_pipe.response

        s.close()

        if response['status'] == 'success':
            print('received db token')
            return response['db-token'], response['file-size']

    def download_output_from_db(self, path_to_file, db_token, file_size):
        global server_addr
        global storage_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(server_addr)
        s1.connect(storage_addr)

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

        req_pipe1 = Messaging(s1, storage_addr, request)
        req_pipe1.queue_request()
        req_pipe1.write()

        # receive exec file
        f = open(path_to_file, "wb")
        data = None
        while True:
            received = 0
            chunk = min(1024, file_size-received)
            m = s1.recv(chunk)
            data = m
            received += chunk
            while received < file_size:
                # break
                m = s1.recv(chunk)
                data += m
                received += chunk
            break
        f.write(data)
        f.close()

        req_pipe.read()
        #response_header = req_pipe.jsonheader
        response = req_pipe.response

        req_pipe1.read()

        print("- receiving output file status:", response['status'])

        s.close()
        s1.close()

