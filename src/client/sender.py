import socket               # Import socket module

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("18.220.165.22", 12345))

# send exec file
f = open('exec_test.py','rb')
print ('Sending...')
l = f.read(1024)
while (l):
    print ('Sending...')
    s.send(l)
    l = f.read(1024)
f.close()
print ("Done Sending")
s.shutdown(socket.SHUT_WR)

# receive output
f = open("recieved_ouput.txt", "wb")
data = None
while True:
    m = s.recv(1024)
    data = m
    if m:
        while m:
            m = s.recv(1024)
            data += m
        else:
            break
f.write(data)
f.close()
print("Done receiving output file")


print (s.recv(1024))
s.close                     # Close the socket when done

# https://stackoverflow.com/questions/27241804/sending-a-file-over-tcp-sockets-in-python
