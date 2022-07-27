import socket
import random
ClientSocket = socket.socket()
host = '127.126.45.1'
port = 1233
print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))
Response = ClientSocket.recv(1024)
cate=input("exit or entry(0->exit 1->entry)")
ClientSocket.send(str.encode(cate))
Input = input('Say passwrod to mark att: as empid,pass: ')
ClientSocket.send(str.encode(Input))
#Response = ClientSocket.recv(1024)
while True:

    m=ClientSocket.recv(1024)
    m=m.decode()
    k=ClientSocket.recv(1024)
    k=k.decode()
    k=int(k)
    i=0
    a=""
    b=""
    f=random.randint(0,1)
    message=""
    while i!=k:

        f=random.randint(0,1)
        if(f==0):
            b="ACK Lost"
            message = ClientSocket.recv(1024)
            message = message.decode()
            ClientSocket.send(b.encode())

        elif(f==1):
            b="ACK "+str(i)
            message = ClientSocket.recv(1024)
            message = message.decode()

            ClientSocket.send(b.encode())
            a=a+message
            i=i+1

    print("The message received is :", m)
#print(Response.decode('utf-8'))
print("closing connection")
ClientSocket.close()
#py multi_c.py
