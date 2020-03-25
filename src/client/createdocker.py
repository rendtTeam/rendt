from tkinter import *
import os

from ui import filelist

def createfilesdir(filelist):
    workd = "" + os.getcwd() + "/files"
    home_dir = os.system("mkdir " + workd )
    for i in filelist:
        home_dir = os.system("cp /" + i + workd )

def forjava():
    f = open("Dockerfile", "a")
    f.write('FROM java:8-jdk-alpine\n')
    f.write('COPY \n')
    f.write('WORKDIR /usr/app\n')
    f.write('ENTRYPOINT ["java", "-jar", ""]\n')
    f.close()

def forpython(filelist): 
    createfilesdir(filelist)
    f = open("Dockerfile", "a")
    f.write('FROM python\n')
    f.write('ADD /files /\n')
    f.write('CMD python '+ os.path.basename(filelist[0]) + '\n') 


    f.close()

    home_dir = os.system("docker build -t rendt .")
    home_dir = os.system("docker run rendt")
    home_dir = os.system("rm -R files")
    home_dir = os.system("rm Dockerfile")
    p = os.popen("docker system prune", "w")
    p.write("y\n")
    home_dir = os.system("docker rmi -f rendt")
    p.write("exit")

def forc():
    f = open("Dockerfile", "a")
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
    home_dir = os.system("rm -R files")
    home_dir = os.system("rm Dockerfile")
    p = os.popen("docker system prune", "w")
    p.write("y\n")
    home_dir = os.system("docker rmi -f rendt")
    p.write("exit")
