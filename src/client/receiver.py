import socket, ssl
import os, sys
import hashlib
from client_messaging import Messaging

server_addr = ('18.220.165.22', 23456)
storage_addr = ('18.197.19.248', 23456)

class Receiver:
    def __init__(self, authToken):
        self.authToken = authToken
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        self.ssl_context.load_default_certs()
    
    def get_available_jobs(self):
        global server_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = self.ssl_context.wrap_socket(s)
        ssl_sock.connect(server_addr)

        content = { 'authToken': self.authToken,
                    'role': 'leaser',
                    'request-type': 'get-available-jobs',
                    }
        request = {'type' : 'text/json',
                    'content': content}

        req_pipe = Messaging(ssl_sock, server_addr, request)
        req_pipe.queue_request()
        req_pipe.write()

        req_pipe.read()
        #response_header = req_pipe.jsonheader
        response = req_pipe.response

        ssl_sock.close()
        s.close()

        if response['status'] == 'success':
            print('received list of jobs')
            return response['jobs']
        else:
            print('error: couldn\'t receive list of jobs')

    def get_permission_to_execute_task(self, job_id):
        global server_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = self.ssl_context.wrap_socket(s)
        ssl_sock.connect(server_addr)

        content = { 'authToken': self.authToken,
                    'role': 'leaser',
                    'request-type': 'execute-permission',
                    'job-id': job_id}
        request = {'type' : 'text/json',
                    'content': content}

        req_pipe = Messaging(ssl_sock, server_addr, request)
        req_pipe.queue_request()
        req_pipe.write()

        req_pipe.read()
        #response_header = req_pipe.jsonheader
        response = req_pipe.response

        ssl_sock.close()
        s.close()

        if response['status'] == 'success':
            print('received db token')
            return response['db-token'], response['file-size']

    def download_file_from_db(self, path_to_file, db_token, file_size):
        global storage_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = self.ssl_context.wrap_socket(s)
        ssl_sock.connect(storage_addr)

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
        f = open("Dockerfile", "a")

        f.write('FROM python\n') 
        f.write('FROM java:8-jdk-alpine\n')
        f.write('FROM ubuntu\n') 
        f.write('RUN apt update && apt install -y zip\n')
        f.write('RUN apt-get -y update && apt-get install -y\n')
        f.write('RUN apt-get -y install clang\n')
        f.write('ADD /files.zip /\n')
        f.write('RUN unzip files.zip && rm files.zip\n')
        # f.write('ADD /commands.txt /\n')
        f.write('RUN chmod +x run.sh')

        f.close()

        home_dir = os.system("docker build -t rendt .")
        home_dir = os.system("docker run -it -d --name rendtcont rendt")
        home_dir = os.system("rm Dockerfile") 

        a = './run.sh >> sender_output.txt'
        print(a)
        b = "docker exec -it rendtcont bash -c '" + a + "'"

        home_dir = os.system(b) 

        home_dir = os.system("docker cp rendtcont:/sender_output.txt " + path_to_output)
        home_dir = os.system("docker stop rendtcont")
        home_dir = os.system("docker container rm rendtcont")

        home_dir = os.system("cat " + path_to_output)

    def get_permission_to_upload_output(self, job_id, path_to_file):
        global server_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = self.ssl_context.wrap_socket(s)
        ssl_sock.connect(server_addr)

        file_size = os.path.getsize(path_to_file)

        content = { 'authToken': self.authToken,
                    'role': 'leaser',
                    'request-type': 'output-upload-permission',
                    'job-id': job_id,
                    'file-size': file_size,
                    'file-type': 'txt'}
        request = {'type' : 'text/json',
                    'content': content}
        req_pipe = Messaging(ssl_sock, server_addr, request)
        req_pipe.queue_request()
        req_pipe.write()

        req_pipe.read()
        #response_header = req_pipe.jsonheader
        response = req_pipe.response

        ssl_sock.close()
        s.close()

        if response['status'] == 'success':
            print('received db token')
            return response['db-token']

    def upload_output_to_db(self, path_to_file, job_id, db_token):
        global storage_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = self.ssl_context.wrap_socket(s)
        ssl_sock.connect(storage_addr)

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

        req_pipe = Messaging(ssl_sock, storage_addr, request)
        req_pipe.queue_request()
        req_pipe.write()

        # send output file
        self.send_file(ssl_sock, path_to_file)

        ssl_sock.shutdown(socket.SHUT_RDWR)
        ssl_sock.close()

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
            return 'fail' # TODO handle
