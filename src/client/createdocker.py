from tkinter import *
import os

import ui
"""
def createfilesdir():
    workd = "" + os.getcwd() + "/files"
    home_dir = os.system("mkdir " + workd )
    home_dir = os.system("cp /Users/cenker/Documents/CS/cs492/try/readdocker.py " + workd )
def forjava():
    f.write('FROM java:8-jdk-alpine\n')
    f.write('COPY \n')
    f.write('WORKDIR /usr/app\n')
    f.write('ENTRYPOINT ["java", "-jar", ""]\n')
    f.close()

def forpython(filename): 
    f = open("Dockerfile", "a")
    f.write('FROM python:3\n')
    f.write('ADD /files /\n')
    f.write('CMD [ "python", "./readdocker.py" ]\n') 


    f.close()
    home_dir = os.system("rm -R files")
    home_dir = os.system("docker build -t rendt .")
    home_dir = os.system("docker run rendt")


    p = os.popen("docker system prune", "w")
    p.write("y\n")
    home_dir = os.system("docker rmi -f rendt")
    p.write("exit")

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

"""

workd = "" + os.getcwd() + "/files"
home_dir = os.system("mkdir " + workd )
home_dir = os.system("cp /Users/cenker/Documents/CS/cs492/try/readdocker.py " + workd )
home_dir = os.system("cp /Users/cenker/Documents/CS/cs492/try/cenk.py " + workd )
print(workd)
f = open("Dockerfile", "a")
f.write('FROM python\n')
f.write('ADD /files /\n')
f.write('CMD python readdocker.py\n') 


f.close()

home_dir = os.system("docker build -t rendt .")
home_dir = os.system("docker run rendt")
home_dir = os.system("rm -R files")
home_dir = os.system("rm Dockerfile")
p = os.popen("docker system prune", "w")
p.write("y\n")
home_dir = os.system("docker rmi -f rendt")
p.write("exit")