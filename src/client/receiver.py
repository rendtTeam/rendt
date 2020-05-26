import socket, ssl
import os, sys
import hashlib
from client_messaging import Messaging
from client import Client

storage_addr = ('18.197.19.248', 23456)

class Receiver(Client):
    def __init__(self, authToken):
        super().__init__(authToken)
        
    def mark_available(self):
        content = { 'authToken': self.authToken,
                    'role': 'leaser',
                    'request-type': 'mark-available',
                    }
        
        response = self.send_request_server(content)
        
        if response['status'] == 'success':
            print('marked as available')
        elif response['status'] == 'error':
            print('error:', response['error-msg'])
        else:
            print('Something went very wrong')

    def get_job_notifications(self):
        content = { 'authToken': self.authToken,
                    'role': 'leaser',
                    'request-type': 'get-job-requests',
                    }
        
        response = self.send_request_server(content)

        if response['status'] == 'success':
            print('received list of requests')
            return response['jobs']
        else:
            print('error: couldn\'t receive list of requests')

    def accept_order(self, order_id):
        content = { 'authToken': self.authToken,
                    'role': 'leaser',
                    'request-type': 'accept-job-order',
                    'order-id': order_id,
                    }
        
        response = self.send_request_server(content)

        if response['status'] == 'success':
            print('successfully accepted order', order_id)
            return response['db-token'], response['file-size']
        else:
            print('error')

    def decline_order(self, order_id):
        content = { 'authToken': self.authToken,
                    'role': 'leaser',
                    'request-type': 'decline-job-order',
                    'order-id': order_id,
                    }
        
        response = self.send_request_server(content)

        if response['status'] == 'success':
            print('successfully declined order', order_id)
        else:
            print('error')
            
    def download_file_from_db(self, path_to_file, db_token, file_size):
        global storage_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = self.ssl_context.wrap_socket(s)
        try:
            ssl_sock.connect(storage_addr)
        except:
            print('coulnd\'t download file; server does not respond')
            return

        content = { 'role': 'leaser',
                    'request-type': 'executable-download',
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

    def execute_job(self, path_to_executable, path_to_output):
        # execute job
        home_dir = os.system("docker run -it -d --name rendtcont rendt")
        home_dir = os.system("docker cp " + path_to_executable + "/files.zip rendtcont:/ ")
        home_dir = os.system("docker exec -it rendtcont bash -c 'unzip files.zip && rm files.zip'")
        home_dir = os.system("docker exec -it rendtcont bash -c 'cd files && chmod +x run.sh'")
        a = './run.sh >> sender_output.txt'
        print(a)
        b = "docker exec -it rendtcont bash -c 'cd files && " + a + "'"
        home_dir = os.system(b) 
        home_dir = os.system("docker exec -it rendtcont bash -c 'mv /files/sender_output.txt /files/output/sender_output.txt'") 
        home_dir = os.system("docker exec -it rendtcont bash -c 'cd files && zip -r -X output.zip output'") 
        home_dir = os.system("docker cp rendtcont:/files/output.zip " + path_to_output)
        home_dir = os.system("docker exec -it rendtcont bash -c 'rm -R files'")
        home_dir = os.system("docker stop rendtcont")
        home_dir = os.system("docker container rm rendtcont")


    def get_permission_to_upload_output(self, job_id, path_to_file):
        file_size = os.path.getsize(path_to_file)

        content = { 'authToken': self.authToken,
                    'role': 'leaser',
                    'request-type': 'output-upload-permission',
                    'job-id': job_id,
                    'file-size': file_size
                    }
        
        response = self.send_request_server(content)

        if response['status'] == 'success':
            print('received db token')
            return response['db-token']

    def upload_output_to_db(self, path_to_file, job_id, db_token):
        global storage_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = self.ssl_context.wrap_socket(s)
        try:
            ssl_sock.connect(storage_addr)
        except:
            print('coulnd\'t upload output; server does not respond')
            return

        content = { 'role': 'leaser',
                    'request-type': 'output-upload',
                    'job-id': job_id,
                    'db-token': db_token
                    }
        request = { 'type' : 'text/json',
                    'content': content
                    }

        req_pipe = Messaging(ssl_sock, storage_addr, request)
        req_pipe.queue_request()
        req_pipe.write()

        # send output file
        self.send_file(ssl_sock, path_to_file)

        status = self.get_job_status(job_id)
        if status == 'f':
            print('File successfully received by server')
        elif status == 'ouf': 
            print('Server couldn\'t receive file')
        else:
            print('File is being uploaded/processed')
