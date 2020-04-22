import socket
import sys
import os
import logging
import datetime
from storage_messaging import Messaging
from dbHandler import DBHandler
import random

class Storage:
    def __init__(self, port):
        self.BACKLOG = 1024      # size of the queue for pending connections

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', port))          # Bind to the port
        self.db_handler = DBHandler()

    def run(self):
        self.s.listen(self.BACKLOG)           # Now wait for client connection.
        while True:
            conn, addr = self.s.accept()
            req_pipe = Messaging(conn, addr)
            req_pipe.read()

            if not req_pipe.jsonheader or not req_pipe.request or 'role' not in req_pipe.request or 'request-type' not in req_pipe.request:
                return
            elif req_pipe.request.get('role') == 'renter':
                self.serve_renter_request(req_pipe, conn, addr)
            elif req_pipe.request.get('role') == 'leaser':
                self.serve_leaser_request(req_pipe, conn, addr)
        
    def serve_renter_request(self, req_pipe, conn, addr):
        header, request_content = req_pipe.jsonheader, req_pipe.request
        # job_id = 7
        client_db_token = request_content['db-token']
        if request_content['request-type'] == 'executable-upload':
            job_id = self.db_handler.getJobIdFromToken(client_db_token, 'x')
            
            self.recv_file(conn, f'jobs/toexec{job_id}.py')
            response_content = {'status': 'success',}
            req_pipe.write(response_content, 'text/json')
            return
        
        elif request_content['request-type'] == 'output-download':
            job_id = self.db_handler.getJobIdFromToken(client_db_token, 'o')

            requested_file_path = f'outputs/output{job_id}.txt'
            if os.path.exists(requested_file_path):
                self.send_file(conn, requested_file_path)
                response_content = {'status': 'success',}
                req_pipe.write(response_content, 'text/json')
                return

    def serve_leaser_request(self, req_pipe, conn, addr):
        header, request_content = req_pipe.jsonheader, req_pipe.request
        # job_id = 7
        client_db_token = request_content['db-token']

        if request_content['request-type'] == 'executable-download':
            job_id = self.db_handler.getJobIdFromToken(client_db_token, 'x')
            requested_file_path = f'jobs/toexec{job_id}.py'
            if os.path.exists(requested_file_path):
                self.send_file(conn, requested_file_path)
                response_content = {'status': 'success',}
                req_pipe.write(response_content, 'text/json')
                return
        
        elif request_content['request-type'] == 'output-upload':
            job_id = self.db_handler.getJobIdFromToken(client_db_token, 'o')
            self.recv_file(conn, f'outputs/output{job_id}.txt')
            response_content = {'status': 'success',}
            req_pipe.write(response_content, 'text/json')
            return

    def recv_file(self, conn, file_name): # TODO add file_size to this
        f = open(file_name,'wb')
        l = conn.recv(1024)
        while (l):
            f.write(l)
            l = conn.recv(1024)
        f.close()

    def send_file(self, conn, file_name):
        f = open(file_name, "rb")
        l = os.path.getsize(file_name)
        m = f.read(l)
        conn.send(m)
        f.close()
        # conn.shutdown(socket.SHUT_WR)

            
def main():
    args = sys.argv[1:]
    port = int(args[0])

    server_instance = Storage(port)
    server_instance.run()

if __name__ == '__main__':
    main()
