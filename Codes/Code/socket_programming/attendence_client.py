import socket
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
Input = input('Say passwrod to mark attendence  as --> empid,pass: ')
ClientSocket.send(str.encode(Input))
Response = ClientSocket.recv(1024)
print(Response.decode('utf-8'))
print("closing connection")
ClientSocket.close()
#py multi_c.py
