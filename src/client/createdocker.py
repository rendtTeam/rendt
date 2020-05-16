import os, sys
f = open("Dockerfile", "a")

f.write('FROM python\n') 
f.write('FROM java:8-jdk-alpine\n')
f.write('FROM ubuntu\n') 
f.write('RUN apt update && apt install -y zip\n')
f.write('RUN apt-get -y update && apt-get install -y\n')
f.write('RUN apt-get -y install clang\n')
f.write('ADD /files.zip /\n')
f.write('RUN unzip files.zip && rm files.zip\n')
f.write('ADD /commands.txt /\n')

f.close()

home_dir = os.system("docker build -t rendt .")
home_dir = os.system("docker run -it -d --name rendtcont rendt")
home_dir = os.system("rm Dockerfile") 
f = open("commands.txt", "r")
a = "cd files && "
for x in f:
    a = a + x.strip('\n') + ">>sender_output.txt && "
            
    a = a[:-3]
    print(a)
b = "docker exec -it rendtcont bash -c '" + a + "'"

home_dir = os.system(b) 

home_dir = os.system("docker cp rendtcont:/files/sender_output.txt .")
home_dir = os.system("docker stop rendtcont")
home_dir = os.system("docker container rm rendtcont")

home_dir = os.system("cat sender_output.txt")
path_to_output = os.getcwd() + "/sender_output.txt"