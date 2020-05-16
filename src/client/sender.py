import socket
import os, sys
from client_messaging import Messaging

server_addr = ('18.220.165.22', 23457)
storage_addr = ('18.197.19.248', 23456)

class Sender:
    def __init__(self, authToken):
        self.authToken = authToken

    def get_permission_to_submit_task(self, path_to_files):
        global server_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(server_addr)

        file_size = os.path.getsize(path_to_files[0])
        script_size =  os.path.getsize(path_to_files[1])

        content = { 'authToken': self.authToken,
                    'role': 'renter',
                    'request-type': 'submit-permission',
                    'files-size': file_size,
                    'script-size': script_size,
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

    def upload_file_to_db(self, path_to_files, job_id, db_token):
        global storage_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(storage_addr)

        files_size = os.path.getsize(path_to_files[0])
        script_size =  os.path.getsize(path_to_files[1])

        content = { 'role': 'renter',
                    'request-type': 'executable-upload',
                    'job-id': job_id,
                    'files-size': files_size,
                    'script-size': script_size,
                    'db-token': db_token
                    }
        request = { 'type' : 'text/json',
                    'content': content
                    }

        req_pipe = Messaging(s, storage_addr, request)
        req_pipe.queue_request()
        req_pipe.write()

        # send exec file
        self.send_file(s, path_to_files[0])
        self.send_file(s, path_to_files[1])

        s.shutdown(socket.SHUT_WR)

        req_pipe.read()
        response_header = req_pipe.jsonheader
        response = req_pipe.response

        print('- server response:', response_header, response['status'])

        s.close()

    def get_permission_to_download_output(self, job_id):
        global server_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(server_addr)
        
        content = { 'authToken': self.authToken,
                    'role': 'renter',
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
        global storage_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(storage_addr)

        content = { 'role': 'renter',
                    'request-type': 'output-download',
                    'db-token': db_token
                    }
        request = { 'type' : 'text/json',
                    'content': content
                    }

        req_pipe = Messaging(s, storage_addr, request)
        req_pipe.queue_request()
        req_pipe.write()

        # receive exec file
        self.receive_file(s, path_to_file, file_size)
        # f = open(path_to_file, "wb")
        # data = None
        # while True:
        #     received = 0
        #     chunk = min(1024, file_size-received)
        #     m = s.recv(chunk)
        #     data = m
        #     received += chunk
        #     while received < file_size:
        #         # break
        #         m = s.recv(chunk)
        #         data += m
        #         received += chunk
        #     break
        # f.write(data)
        # f.close()

        req_pipe.read()
        response_header = req_pipe.jsonheader
        response = req_pipe.response      
        
        print("- receiving output file status:", response['status'])

        s.close()

    def send_file(self, conn, path_to_file):
        f = open(path_to_file,'rb')
        l = f.read(1024)
        while (l):
            conn.send(l)
            l = f.read(1024)
        f.close()
        print ('Done sending file(s)')

    def receive_file(self, conn, path_to_file, size):
        f = open(path_to_file, "wb")
        data = None
        received = 0
        while received < size:
            chunk = min(1024, size-received)
            m = conn.recv(chunk)
            if not data:
                data = m
            else: 
                data += m
            received += chunk

        f.write(data)
        f.close()