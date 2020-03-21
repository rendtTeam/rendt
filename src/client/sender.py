import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
class Sender:
    def sendToServer(self,fileName):
        # send exec file
        global s
        s.connect(("18.220.165.22", 23456))
        f = open(fileName,'rb')
        l = f.read(1024)
        while (l):
            s.send(l)
            l = f.read(1024)
        f.close()
        print ("Done Sending")
        s.shutdown(socket.SHUT_WR)
        self.receiveFromServer()

    def receiveFromServer(self):
    # receive output
        f = open("received_output.txt", "wb")
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