import socket
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind(('', port))          # Bind to the port

print('Server Running.')

# Server receives file from sender
f = open('toexec.py','wb')
s.listen(1)                  # Now wait for client connection.
while True:
    c_send, addr_send = s.accept()     # Establish connection with client.
    print ('Got connection from sender:', addr_send)
    l = c_send.recv(1024)
    while (l):
        f.write(l)
        l = c_send.recv(1024)
    f.close()
    break


print('file recevied from sender')


# Server sends file to receiver
s.listen(1)
c_rec, addr_rec = s.accept()
print('Got connection from receiver:', addr_rec)
f = open("toexec.py", "rb")
l = os.path.getsize("toexec.py")
m = f.read(l)
c_rec.send(m)
f.close()
c_rec.shutdown(socket.SHUT_WR)


print('file sent to receiver')


# Server receives output from receiver
f = open('output.txt','wb')
print('receiving file from receiver')
l = c_rec.recv(1024)
while (l):
    f.write(l)
    l = c_rec.recv(1024)
f.close()


print('output file received from receiver')

# Server sends output to sender
f = open("output.txt", "rb")
l = os.path.getsize("output.txt")
m = f.read(l)
c_send.send(m)
f.close()
c_send.shutdown(socket.SHUT_WR)


print('output file send to sender')



c_rec.close()              
c_send.close()

