import socket, ssl
import os, sys
import hashlib
from client_messaging import Messaging

server_addr = ('18.220.165.22', 23456)
storage_addr = ('18.197.19.248', 23456)

class Sender:
    def __init__(self, authToken):
        self.authToken = authToken
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        self.ssl_context.load_default_certs()

    def get_job_statuses(self):
        content = { 'authToken': self.authToken,
                    'role': 'renter',
                    'request-type': 'get-job-statuses',
                    }
        
        response = self.send_request_server(content)

        if response['status'] == 'success':
            print('received list of statuses')
            return response['statuses']
        else:
            print('error: couldn\'t receive list of statuses')
    
    def get_available_leasers(self):
        content = { 'authToken': self.authToken,
                    'role': 'renter',
                    'request-type': 'get-available-leasers',
                    }
        
        response = self.send_request_server(content)

        if response['status'] == 'success':
            print('received list of leasers')
            return response['leasers']
        else:
            print('error: couldn\'t receive list of leasers')

    def get_permission_to_upload_job(self, path_to_file):
        file_size = os.path.getsize(path_to_file)

        content = { 'authToken': self.authToken,
                    'role': 'renter',
                    'request-type': 'executable-upload-permission',
                    'file-size': file_size,
                    'file-type': 'py'}

        response = self.send_request_server(content)
        
        if response['status'] == 'success':
            print('received db token')
            return response['job-id'], response['db-token']

    def upload_file_to_db(self, path_to_file, job_id, db_token):
        global storage_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = self.ssl_context.wrap_socket(s)
        ssl_sock.connect(storage_addr)

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

        req_pipe = Messaging(ssl_sock, storage_addr, request)
        req_pipe.queue_request()
        req_pipe.write()

        # send exec file
        self.send_file(ssl_sock, path_to_file)

        ssl_sock.shutdown(socket.SHUT_RDWR)
        ssl_sock.close()

    def submit_job_order(self, job_id, leaser_id, job_description):
        content = { 'authToken': self.authToken,
                    'role': 'renter',
                    'request-type': 'submit-job-order',
                    'job-id': job_id,
                    'leaser-id': leaser_id,
                    'job-description': job_description
                    }
        
        response = self.send_request_server(content)

        if response['status'] == 'success':
            print('job order submitted')
        elif response['status'] == 'error':
            print('error:', response['error-msg'])

    def get_permission_to_download_output(self, job_id):
        content = { 'authToken': self.authToken,
                    'role': 'renter',
                    'request-type': 'output-download-permission',
                    'job-id': job_id}
        
        response = self.send_request_server(content)

        if response['status'] == 'success':
            print('received db token')
            return response['db-token'], response['file-size']

    def download_output_from_db(self, path_to_file, db_token, file_size):
        global storage_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = self.ssl_context.wrap_socket(s)
        ssl_sock.connect(storage_addr)

        content = { 'role': 'renter',
                    'request-type': 'output-download',
                    'db-token': db_token
                    }
        request = { 'type' : 'text/json',
                    'content': content
                    }

        req_pipe = Messaging(ssl_sock, storage_addr, request)
        req_pipe.queue_request()
        req_pipe.write()

        # receive exec file
        status = self.receive_file(ssl_sock, path_to_file, file_size)

        print("- receiving execution file status:", status)

        ssl_sock.close()
        s.close()

    def send_request_server(self, request_content):
        global server_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = self.ssl_context.wrap_socket(s)
        ssl_sock.connect(server_addr)

        request = {'type' : 'text/json',
                    'content': request_content}

        req_pipe = Messaging(ssl_sock, server_addr, request)
        req_pipe.queue_request()
        req_pipe.write()

        req_pipe.read()
        #response_header = req_pipe.jsonheader
        response = req_pipe.response

        ssl_sock.close()
        s.close()

        return response

    def send_file(self, conn, path_to_file):
        f = open(path_to_file,'rb')
        l = f.read(4096)
        while (l):
            conn.send(l)
            l = f.read(4096)
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