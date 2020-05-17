import socket
import sys
import os
import logging
import datetime
import threading
from threading import Thread
from storage_messaging import Messaging
from dbHandler import DBHandler
import random

class Storage:
    def __init__(self, port):
        self.BACKLOG = 1024      # size of the queue for pending connections

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', port))          # Bind to the port

        self.db_handler = DBHandler()
        self.logger = self.configure_logging()

    def run(self):
        self.s.listen(self.BACKLOG)           # Now wait for client connection.
        self.logger.info('Storage up and running.\n')

        while True:
            conn, addr = self.s.accept()

            try:
                Thread(target=self.serve_client, args=(conn, addr)).start()
            except:
                self.refuse_client(conn, addr)
                self.logger.error(f'Couldn\'t create thread. Refused client at {addr}')
    
    def configure_logging(self):
        logger = logging.getLogger('Storage.logger')
        logger.setLevel(logging.INFO)

        currentDT = str(datetime.datetime.now()).replace(' ', '_')
        format_ = logging.Formatter('%(asctime)s  %(name)-12s  %(levelname)-8s  %(message)s')

        # create log fle handler
        file_handler = logging.FileHandler('logs/logfile_' + currentDT)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(format_)
        # create console handler with a higher log level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(format_)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        logger.info('begin log')
        return logger

    def serve_client(self, conn, addr):
        self.logger.info(f'Thread {threading.get_ident()} initialized to server request from {addr}')
        req_pipe = Messaging(conn, addr)
        req_pipe.read()

        if not req_pipe.jsonheader or not req_pipe.request or 'role' not in req_pipe.request or 'request-type' not in req_pipe.request:
            self.logger.warning(f'invalid request from {addr}.')
        elif req_pipe.request.get('role') == 'renter':
            self.serve_renter_request(req_pipe, conn, addr)
        elif req_pipe.request.get('role') == 'leaser':
            self.serve_leaser_request(req_pipe, conn, addr)
    
    def refuse_client(self, conn, addr):
        req_pipe = Messaging(conn, addr)
        req_pipe.read()
        response_content = {'status': 'error',
                            'error-msg': 'Storage server busy, can\'t serve at the time.'
                                    }
        req_pipe.write(response_content, 'text/json')

    def serve_renter_request(self, req_pipe, conn, addr):
        header, request_content = req_pipe.jsonheader, req_pipe.request
        if 'db-token' not in request_content:
            response_content = {'status': 'error: no/invalid token provided',
                                }
            req_pipe.write(response_content, 'text/json')
            self.logger.warning(f'invalid connection from retner at {addr[0]}: no/invalid token')
            return
        
        client_db_token = request_content['db-token']

        if request_content['request-type'] == 'executable-upload':
            self.logger.info(f'connection: renter from {addr}; request type: executable-upload')
            job_id = self.db_handler.getJobIdFromToken(client_db_token, 'x')
            file_size = request_content['file-size']
            self.recv_file(conn, f'jobs/toexec{job_id}.zip', file_size)
            self.db_handler.changeJobStatus(job_id, 'a')
            self.logger.info(f'successfully received exec files for job {job_id} from renter {addr[0]}')
            response_content = {'status': 'success',}
            req_pipe.write(response_content, 'text/json')

            file_size_new = os.path.getsize(f'jobs/toexec{job_id}.zip')
            self.db_handler.setJobFileSize(job_id, file_size_new)
            return
        
        elif request_content['request-type'] == 'output-download':
            self.logger.info(f'connection: renter from {addr}; request type: output-download')
            job_id = self.db_handler.getJobIdFromToken(client_db_token, 'o')
            requested_file_path = f'outputs/output{job_id}.txt'
            if os.path.exists(requested_file_path):
                self.send_file(conn, requested_file_path)
                self.logger.info(f'successfully sent output file for job {job_id} to renter {addr[0]}')
                response_content = {'status': 'success',}
                req_pipe.write(response_content, 'text/json')
                return
            # TODO handle error

    def serve_leaser_request(self, req_pipe, conn, addr):
        header, request_content = req_pipe.jsonheader, req_pipe.request
        if 'db-token' not in request_content:
            response_content = {'status': 'error: no/invalid token provided',
                                }
            req_pipe.write(response_content, 'text/json')
            self.logger.warning(f'invalid connection from leaser at {addr[0]}: no/invalid token')
            return
        
        client_db_token = request_content['db-token']

        if request_content['request-type'] == 'executable-download':
            self.logger.info(f'connection: leaser from {addr}; request type: executable-download')
            job_id = self.db_handler.getJobIdFromToken(client_db_token, 'x')
            requested_file_path = f'jobs/toexec{job_id}.zip'
            if os.path.exists(requested_file_path):
                self.send_file(conn, requested_file_path)
                self.logger.info(f'successfully sent exec file for job {job_id} to leaser {addr[0]}')
                response_content = {'status': 'success',}
                req_pipe.write(response_content, 'text/json')
                return
        
        elif request_content['request-type'] == 'output-upload':
            self.logger.info(f'connection: leaser from {addr}; request type: output-upload')
            job_id = self.db_handler.getJobIdFromToken(client_db_token, 'o')
            file_size = request_content['file-size']
            self.recv_file(conn, f'outputs/output{job_id}.txt', file_size)
            self.db_handler.changeJobStatus(job_id, 'f')
            self.logger.info(f'successfully received output file for job {job_id} from leaser {addr[0]}')
            response_content = {'status': 'success',}
            req_pipe.write(response_content, 'text/json')
            return

    def recv_file(self, conn, file_name, size):
        f = open(file_name,'wb')

        received = 0
        while received < size:
            chunk = min(1024, size-received)
            l = conn.recv(chunk)
            f.write(l)
            received += chunk

        f.close()

    def send_file(self, conn, file_name):
        f = open(file_name, "rb")
        l = os.path.getsize(file_name)
        m = f.read(l)
        conn.send(m)
        f.close()
        print('file sent')
        # conn.shutdown(socket.SHUT_WR)

            
def main():
    args = sys.argv[1:]
    port = int(args[0])

    server_instance = Storage(port)
    server_instance.run()

if __name__ == '__main__':
    main()
