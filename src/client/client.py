import socket, ssl
import os, sys
import hashlib
from client_messaging import Messaging

server_addr = ('18.220.165.22', 23456)
storage_addr = ('18.197.19.248', 23456)

class Client:
    def __init__(self, authToken):
        self.authToken = authToken
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        self.ssl_context.load_default_certs()
    
    def get_job_status(self, job_id):
        content = { 'authToken': self.authToken,
                    'role': 'renter',
                    'request-type': 'get-job-status',
                    'job-id': job_id
                    }
        
        response = self.send_request_server(content)

        if response['status'] == 'success':
            print(f'received status of job {job_id}')
            return response['job-status']
        else:
            print('error: couldn\'t receive status')

    def sign_out(self):
        content = { 'authToken': self.authToken,
                    'request-type': 'sign-out',
                    }
        
        response = self.send_request_server(content)
        print('status:', response['status'])

    def send_request_server(self, request_content):
        global server_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = self.ssl_context.wrap_socket(s)
        try:
            ssl_sock.connect(server_addr)
        except:
            print('ERROR: coulnd\'t send request; server does not respond')
            return

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
        # calculate checksum
        checksum = hashlib.md5()
        with open(path_to_file, "rb") as fl:
            for chunk in iter(lambda: fl.read(4096), b""):
                checksum.update(chunk)
        checksum = checksum.hexdigest()

        # send file with checksum
        f = open(path_to_file,'rb')
        conn.send(checksum.encode('utf-8'))
        for chunk in iter(lambda: f.read(4096), b""):
            conn.send(chunk)
        f.close()
        
        conn.shutdown(socket.SHUT_WR)
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