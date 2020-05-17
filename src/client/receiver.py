import socket
import os, sys
from client_messaging import Messaging

server_addr = ('18.220.165.22', 23457)
storage_addr = ('18.197.19.248', 23456)

class Receiver:
    def __init__(self, authToken):
        self.authToken = authToken
    
    def get_available_jobs(self):
        global server_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(server_addr)

        content = { 'authToken': self.authToken,
                    'role': 'leaser',
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

        content = { 'authToken': self.authToken,
                    'role': 'leaser',
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
            return response['db-token'], response['file-size'], response['script-size']

    def download_file_from_db(self, path_to_files, db_token, file_size, script_size):
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
        self.receive_file(s, path_to_files[0], file_size)
        self.receive_file(s, path_to_files[1], script_size)

        req_pipe.read()
        # response_header = req_pipe.jsonheader
        response = req_pipe.response

        print("- receiving execution file status:", response['status'])
        
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
        f.write('ADD /commands.txt /\n')
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
        s.connect(server_addr)

        file_size = os.path.getsize(path_to_file)

        content = { 'authToken': self.authToken,
                    'role': 'leaser',
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

        # send output file
        self.send_file(s, path_to_file)
        s.shutdown(socket.SHUT_WR)

        req_pipe.read()
        # response_header = req_pipe.jsonheader
        response = req_pipe.response

        print('- uploading output file status:', response['status'])

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