import socket               # Import socket module
from client_messaging import Messaging

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("18.220.165.22", 12345))

# send request
content = {'role': 'sender'}
request = {'type' : 'text/json',
            'content': content}
req_pipe = Messaging(s, ("18.220.165.22", 12346), request)
req_pipe.queue_request()
req_pipe.write()

req_pipe.read()
response_header = req_pipe.jsonheader
response = req_pipe.response

print(response_header, response, req_pipe.request)


# # send exec file
# f = open('exec_test.py','rb')
# l = f.read(1024)
# while (l):
#     s.send(l)
#     l = f.read(1024)
# f.close()
# print ("Done Sending")
# s.shutdown(socket.SHUT_WR)
#
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
