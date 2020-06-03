import os, sys

"""path_to_output = 'sender_output.txt'


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

home_dir = os.system("docker build -t rendt .")"""

#home_dir = os.system("rm Dockerfile")
###############################################################
home_dir = os.system("pwd>pwd.txt")

f = open("pwd.txt", "r")
x = f.readline()
x = x.split("/")        
y = "/" + x[1] + "/" + x[2] + "/rendt"
f.close()
home_dir = os.system("rm pwd.txt")
home_dir = os.system("mkdir " + y)
home_dir = os.system("docker run -it -d --name rendtcont rendt")
home_dir = os.system("docker cp " + y + "/files.zip rendtcont:/ ")
home_dir = os.system("docker exec -it rendtcont bash -c 'unzip files.zip && rm files.zip'")
home_dir = os.system("docker exec -it rendtcont bash -c 'cd files && chmod +x run.sh'")
a = './run.sh >> sender_output.txt'
print(a)
b = "docker exec -it rendtcont bash -c 'cd files && " + a + "'"
home_dir = os.system(b) 
home_dir = os.system("docker exec -it rendtcont bash -c 'cd files && mkdir output'") 
home_dir = os.system("docker exec -it rendtcont bash -c 'mv /files/sender_output.txt /files/output/sender_output.txt'") 
home_dir = os.system("docker exec -it rendtcont bash -c 'cd files && zip -r -X output.zip output'") 
home_dir = os.system("docker cp rendtcont:/files/output.zip .")
home_dir = os.system("docker exec -it rendtcont bash -c 'rm -R files'")
home_dir = os.system("docker stop rendtcont")
home_dir = os.system("docker container rm rendtcont")