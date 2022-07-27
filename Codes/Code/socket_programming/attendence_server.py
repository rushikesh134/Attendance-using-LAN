import socket
import os
import csv
import datetime as d
from _thread import *
import random
ServerSocket = socket.socket()
host = '127.126.45.1'
port = 1233
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)
head = ['empIP','password','timestamp','marked']
with open("entry.csv", 'a') as csvfile:
    w=csv.DictWriter(csvfile,fieldnames=head)
    w.writeheader()
csvfile.close()
with open("exit.csv", 'a') as csvfile:
    w=csv.DictWriter(csvfile,fieldnames=head)
    w.writeheader()
csvfile.close()

def threaded_client(connection):
    connection.send(str.encode('Welcome to the Server\n'))

    f=0
    inout=connection.recv(1024)
    inout=inout.decode('utf-8')

    if inout=='1':
        data = connection.recv(2048)
        data=data.decode('utf-8')
        id,pas=data.split(",")
        print(id,pas)
        with open('credentials.csv','r') as csvfile:
            r=csv.reader(csvfile)
            for x in r:
                if(id==x[0] and pas==x[1]):
                    with open('entry.csv','a')as cf:
                        w=csv.writer(cf)
                        w.writerow([id,pas,d.datetime.now(),'p'])
                    cf.close()
                    f=1
                    ok = 'Marked present'
                    reply = 'Server Says: ' + ok

    if inout=='0':
        data = connection.recv(2048)
        data=data.decode('utf-8')
        id,pas=data.split(",")
        print(id,pas)
        with open('credentials.csv','r') as csvfile:
            r=csv.reader(csvfile)
            for x in r:
                if(id==x[0] and pas==x[1]):
                    with open('exit.csv','a')as cf:
                        w=csv.writer(cf)
                        w.writerow([id,pas,d.datetime.now(),'l'])
                    cf.close()
                    f=1
                    otp=random.randrange(1001,9000,1)
                    otp=str(otp)
                    ok = 'Marked exit\n'
                    reply = 'Server Says: ' + ok+" OTP for exit is :> "+otp



    if f==0:
        oops="fail"
        connection.send(str.encode(oops))

    connection.send(str.encode(reply))
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()
#py server.py
