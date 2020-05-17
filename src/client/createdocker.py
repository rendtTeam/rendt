import os, sys

path_to_output = 'sender_output.txt'

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
f.write('RUN chmod +x run.sh')

f.close()

home_dir = os.system("docker build -t rendt .")
home_dir = os.system("docker run -it -d --name rendtcont rendt")
home_dir = os.system("rm Dockerfile") 

a = './run.sh >> sender_output.txt'
print(a)
b = "docker exec -it rendtcont bash -c '" + a + "'"

home_dir = os.system("docker cp rendtcont:/sender_output.txt " + path_to_output)
home_dir = os.system("docker stop rendtcont")
home_dir = os.system("docker container rm rendtcont")

home_dir = os.system("cat " + path_to_output)