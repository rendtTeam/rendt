import socket          
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
class Receiver:
    def receiveFromServer(self):
        #receive exec file
        global s
        s.connect(("18.220.165.22", 23456))
        f = open("sender_job.py", "wb")
        data = None
        while True:
            m = s.recv(1024)
            data = m
            while m:
                # break
                m = s.recv(1024)
                data += m
            break
        f.write(data)
        f.close()

        print("Done receiving execution file")

    def execute(self):
        # execute job
        os.system("python3 sender_job.py >> output.txt")
        self.sendToServer()


    def sendToServer(self):
    # send result to server
        f = open('output.txt','rb')
        l = f.read(1024)
        while (l):
            s.send(l)
            l = f.read(1024)
        f.close()
        print ("Done Sending output file")
        s.shutdown(socket.SHUT_WR)

        s.close()                     # Close the socket when done