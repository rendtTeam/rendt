import socket
from client_messaging import Messaging

server_addr = ('18.220.165.22', 23457)

class Auth:

    def sign_in(self, email, password):
        global server_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(server_addr)

        content = { 'request-type': 'sign-in', 
                    'email': email,
                    'password': password
                    }
        request = {'type' : 'text/json',
                    'content': content}
        request_pipe = Messaging(s, server_addr, request)
        request_pipe.queue_request()
        request_pipe.write()
        request_pipe.read()
        response = request_pipe.response
        s.close()

        if response['status'] == 'error':
            print('ERROR:', response['error-msg'])
        else:
            return response['authToken'], response['user-type']
        
    def sign_up(self, email, password, user_type='U', machine_chars=' '):
        global server_addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(server_addr)

        content = { 'request-type': 'sign-up',
                    'email': email,
                    'password': password,
                    'user-type': user_type,
                    'machine-chars': machine_chars
                    }
        request = {'type' : 'text/json',
                    'content': content}
        request_pipe = Messaging(s, server_addr, request)
        request_pipe.queue_request()
        request_pipe.write()
        request_pipe.read()
        response = request_pipe.response
        s.close()
        if response['status'] == 'error':
            print('ERROR:', response['error-msg'])
        else:
            return response['authToken'], user_type
