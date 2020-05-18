import socket
import os, sys
import hashlib
from client_messaging import Messaging

server_addr = ('18.220.165.22', 23457)
storage_addr = ('18.197.19.248', 23456)

class Sender:
    def __init__(self, authToken):
        self.authToken = authToken

    def get_permission_to_submit_task(self, path_to_file):
        global server_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(server_addr)

        file_size = os.path.getsize(path_to_file)

        content = { 'authToken': self.authToken,
                    'role': 'renter',
                    'request-type': 'submit-permission',
                    'file-size': file_size,
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

    def upload_file_to_db(self, path_to_file, job_id, db_token):
        global storage_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(storage_addr)

        files_size = os.path.getsize(path_to_file)

        content = { 'role': 'renter',
                    'request-type': 'executable-upload',
                    'job-id': job_id,
                    'file-size': files_size,
                    'db-token': db_token
                    }
        request = { 'type' : 'text/json',
                    'content': content
                    }

        req_pipe = Messaging(s, storage_addr, request)
        req_pipe.queue_request()
        req_pipe.write()

        # send exec file
        self.send_file(s, path_to_file)

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
        status = self.receive_file(s, path_to_file, file_size)

        print("- receiving execution file status:", status)
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
        # receive checksum
        checksum_received = conn.recv(32)
        # receive file
        checksum_computed = hashlib.md5()
        f = open(path_to_file, "wb")
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            checksum_computed.update(chunk)
            f.write(chunk)
        f.close()
        # check for integrity
        if checksum_computed.hexdigest().encode('utf-8') == checksum_received:
            return 'success'
        else:
            return 'fail'