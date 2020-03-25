from tkinter import *
import os
f = open("Dockerfile", "a")
"""def forjava():
    f.write('FROM java:8-jdk-alpine\n')
    f.write('COPY \n')
    f.write('WORKDIR /usr/app\n')
    f.write('ENTRYPOINT ["java", "-jar", ""]\n')
    f.close()
"""
def forpython():
    f.write('FROM python:3\n')
    f.write('ADD test.py /\n')
    f.write('RUN pip install pystrich\n')
    f.write('CMD [ "python", "./test.py" ]\n')
    f.write('CMD ls\n')

    f.close()

def forc():
    f.write('FROM ubuntu:latest\n')
    f.write('RUN apt-get -y update && apt-get install -y\n')
    f.write('RUN apt-get -y install clang\n')
    f.write('COPY . \n')
    f.write('WORKDIR /usr/src/dockertest1\n')
    f.write('RUN clang++ -o Test Test.cpp\n')
    f.write('CMD ["./Test"]\n')
    f.close()



home_dir = os.system("docker build -t rendt .")
home_dir = os.system("docker run rendt")


p = os.popen("docker system prune", "w")
p.write("y\n")
home_dir = os.system("docker rmi -f rendt")
p.write("exit")

