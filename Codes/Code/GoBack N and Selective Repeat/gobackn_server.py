import socket
import os
import csv
import datetime as d
from _thread import *
import time
import random

def decimalToBinary(n):
    return n.replace("0b", "")

def binarycode(s):
    a_byte_array = bytearray(s, "utf8")

    byte_list = []

    for byte in a_byte_array:
        binary_representation = bin(byte)
        byte_list.append(decimalToBinary(binary_representation))

    #print(byte_list)
    a=""
    for i in byte_list:
        a=a+i
    return a

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
        with open('match.csv','r') as csvfile:
            r=csv.reader(csvfile)
            for x in r:
                if(id==x[0] and pas==x[1]):
                    with open('entry.csv','a')as cf:
                        w=csv.writer(cf)
                        w.writerow([id,pas,d.datetime.now(),'p'])
                    cf.close()
                    f=1
                    #while True:
                    ok = 'Marked present'
                    reply = 'Server Says: ' + ok
                    message = (str(reply))
                    connection.send(message.encode())
                    message=binarycode(message)
                    f=str(len(message))
                    connection.send(f.encode())

                    i=0
                    j=0
                    j=int(input("Enter the window size -> "))
                    b=""
                    j=j-1
                    f=int(f)
                    k=j
                    while i!=f:
                        while(i!=(f-j)):
                            connection.send(message[i].encode())
                            b=connection.recv(1024)
                            b=b.decode()
                            print(b)
                            if(b!="ACK Lost"):
                                time.sleep(1)
                                print("Acknowledgement Received! The sliding window is in the range "+(str(i+1))+" to "+str(k+1)+" Now sending the next packet")
                                i=i+1
                                k=k+1
                                time.sleep(1)
                            else:
                                time.sleep(1)
                                print("Acknow of the data bit is LOST!  window remains in the  "+(str(i+1))+" to "+str(k+1)+" Now Resending the same packet")
                                time.sleep(1)
                        while(i!=f):

                            connection.send(message[i].encode())
                            b=connection.recv(1024)
                            b=b.decode()
                            print(b)
                            if(b!="ACK Lost"):
                                time.sleep(1)
                                print("Acknowledgement Received! The sliding window is in the range "+(str(i+1))+" to "+str(k)+" Now sending the next packet")
                                i=i+1
                                time.sleep(1)
                            else:
                                time.sleep(1)
                                print("Acknowledgement of the data bit is LOST! The sliding window remains in the range "+(str(i+1))+" to "+str(k)+" Now Resending the same packet")
                                time.sleep(1)


    if inout=='0':
        data = connection.recv(2048)
        data=data.decode('utf-8')
        id,pas=data.split(",")
        print(id,pas)
        with open('match.csv','r') as csvfile:
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
                    message = (str(reply))
                    connection.send(message.encode())
                    message=binarycode(message)
                    f=str(len(message))
                    connection.send(f.encode())

                    i=0
                    j=0
                    j=int(input("Enter the window size -> "))
                    b=""
                    j=j-1
                    f=int(f)
                    k=j
                    while i!=f:
                        while(i!=(f-j)):
                            connection.send(message[i].encode())
                            b=connection.recv(1024)
                            b=b.decode()
                            print(b)
                            if(b!="ACK Lost"):
                                time.sleep(1)
                                print("Acknowledgement Received! The sliding window is in the range "+(str(i+1))+" to "+str(k+1)+" Now sending the next packet")
                                i=i+1
                                k=k+1
                                time.sleep(1)
                            else:
                                time.sleep(1)
                                print("Acknow of the data bit is LOST!  window remains in the  "+(str(i+1))+" to "+str(k+1)+" Now Resending the same packet")
                                time.sleep(1)
                        while(i!=f):

                            connection.send(message[i].encode())
                            b=connection.recv(1024)
                            b=b.decode()
                            print(b)
                            if(b!="ACK Lost"):
                                time.sleep(1)
                                print("Acknowledgement Received! The sliding window is in the range "+(str(i+1))+" to "+str(k)+" Now sending the next packet")
                                i=i+1
                                time.sleep(1)
                            else:
                                time.sleep(1)
                                print("Acknowledgement of the data bit is LOST! The sliding window remains in the range "+(str(i+1))+" to "+str(k)+" Now Resending the same packet")
                                time.sleep(1)


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
