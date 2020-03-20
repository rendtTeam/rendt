import socket               # Import socket module
from client_messaging import Messaging
import os

server_addr = ('18.220.165.22', 12346)

def get_permission_to_submit_task(path_to_file):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_addr)

    file_size = os.path.getsize(path_to_file)

    content = {'role': 'sender',
                'request-type': 'submit-permission',
                'file-size': file_size,
                'file-type': 'py'}
    request = {'type' : 'text/json',
                'content': content}
    req_pipe = Messaging(s, server_addr, request)
    req_pipe.queue_request()
    req_pipe.write()

    req_pipe.read()
    response_header = req_pipe.jsonheader
    response = req_pipe.response

    s.close()

    if response['status'] == 'success':
        print('received db token')
        return response['db-token']

def upload_file_to_db(path_to_file, db_token):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_addr) 

    file_size = os.path.getsize(path_to_file)

    content = { 'role': 'sender',
                'request-type': 'executable-upload',
                'file-size': file_size,
                'file-type': 'py',
                'db-token': db_token
                }
    request = { 'type' : 'text/json',
                'content': content
                }

    req_pipe = Messaging(s, server_addr, request)
    req_pipe.queue_request()
    req_pipe.write()

    # send exec file
    f = open(path_to_file,'rb')
    l = f.read(1024)
    while (l):
        s.send(l)
        l = f.read(1024)
    f.close()
    print ('Done Sending')
    s.shutdown(socket.SHUT_WR)

    req_pipe.read()
    response_header = req_pipe.jsonheader
    response = req_pipe.response

    print(response_header, response, req_pipe.request)

    s.close()

db_token = get_permission_to_submit_task('/Users/m4hmmd/Desktop/senior/base_server_test/sender/exec_test.py')
upload_file_to_db('/Users/m4hmmd/Desktop/senior/base_server_test/sender/exec_test.py', db_token)



# # receive output
# f = open("recieved_ouput.txt", "wb")
# data = None
# while True:
#     m = s.recv(1024)
#     data = m
#     if m:
#         while m:
#             m = s.recv(1024)
#             data += m
#         else:
#             break
# f.write(data)
# f.close()
# print("Done receiving output file")
#
#
# s.close()                     # Close the socket when done
