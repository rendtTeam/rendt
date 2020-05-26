import os, sys

path_to_output = 'sender_output.txt'


f = open("Dockerfile", "a")

f.write('FROM ubuntu:latest\n') 
f.write('RUN apt update && apt install -y zip\n')
f.write('RUN apt install -y python\n')
f.write('RUN apt install -y python3.7\n')
f.write('RUN apt install -y default-jdk\n')
f.write('RUN apt-get install -y gcc\n')
f.write('RUN apt-get install -y python-pip\n')
f.write('RUN apt-get install -y python3-pip\n')
f.write('RUN apt-get install -y openmpi-bin\n')


f.close()

home_dir = os.system("docker build -t rendt .")

#home_dir = os.system("rm Dockerfile")
###############################################################
