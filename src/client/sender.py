import socket, ssl
import os, sys
import hashlib
from client_messaging import Messaging
from client import Client

storage_addr = ('18.197.19.248', 23456)

class Sender(Client):
    def __init__(self, authToken):
        super().__init__(authToken)
        
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
        try:
            ssl_sock.connect(storage_addr)
        except:
            print('coulnd\'t upload file; server does not respond')
            return

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

        status = self.get_job_status(job_id)
        if status == 'a':
            print('File successfully received by server')
        elif status == 'xuf': 
            print('Server couldn\'t receive file')
        else:
            print('File is being uploaded/processed')

    def submit_job_order(self, job_id, leaser_id, file_size, job_description, job_mode='n'):
        content = { 'authToken': self.authToken,
                    'role': 'renter',
                    'request-type': 'submit-job-order',
                    'job-mode': job_mode,
                    'job-id': job_id,
                    'file-size': file_size,
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
        try:
            ssl_sock.connect(storage_addr)
        except:
            print('coulnd\'t download ouput; server does not respond')
            return

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
