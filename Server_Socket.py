# -*- coding: utf-8 -*-
import socket

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, addr = sock.accept()
print ('connected:', addr)

while True:
    try:
        conn.settimeout(5) # установка таймаута
        data = conn.recv(1024)
        data = data + bytearray(b' recieve')
        conn.send(data)
    except:ConnectionAbortedError
    conn.close()
    print ('disconnected from client:', addr)
    break

sock.listen(1)
conn, addr = sock.accept()
while True:
    try:
        conn.settimeout(5) # установка таймаута
        data = conn.recv(1024)
        data = data + bytearray(b' recieve')
        conn.send(data)
    except:ConnectionAbortedError
    conn.close()
    print ('disconnected from client:', addr)
    break
