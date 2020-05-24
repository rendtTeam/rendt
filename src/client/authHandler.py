import socket, ssl
from client_messaging import Messaging

server_addr = ('18.220.165.22', 23457)

class Auth:
    def __init__(self):
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        self.ssl_context.load_default_certs()

    def sign_in(self, email, password):
        global server_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = self.ssl_context.wrap_socket(s)
        try:
            ssl_sock.connect(server_addr)
        except:
            print('coulnd\'t sign in; server unavailable')
            return

        content = { 'request-type': 'sign-in', 
                    'email': email,
                    'password': password
                    }
        request = {'type' : 'text/json',
                    'content': content}
        request_pipe = Messaging(ssl_sock, server_addr, request)
        request_pipe.queue_request()
        request_pipe.write()
        request_pipe.read()
        response = request_pipe.response
        ssl_sock.close()
        s.close()

        if response['status'] == 'error':
            print('ERROR:', response['error-msg'])
        else:
            return response['authToken'], response['user-type']
        
    def sign_up(self, email, password, user_type='U', machine_chars=' '):
        global server_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = self.ssl_context.wrap_socket(s)
        try:
            ssl_sock.connect(server_addr)
        except:
            print('coulnd\'t sign in; server unavailable')
            return

        content = { 'request-type': 'sign-up',
                    'email': email,
                    'password': password,
                    'user-type': user_type,
                    'machine-chars': machine_chars
                    }
        request = {'type' : 'text/json',
                    'content': content}
        request_pipe = Messaging(ssl_sock, server_addr, request)
        request_pipe.queue_request()
        request_pipe.write()
        request_pipe.read()
        response = request_pipe.response
        ssl_sock.close()
        s.close()
        
        if response['status'] == 'error':
            print('ERROR:', response['error-msg'])
        else:
            return response['authToken'], user_type
