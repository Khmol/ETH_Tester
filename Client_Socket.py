#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys

HOST, PORT = "localhost", 7700
data = b"aaaaaaaaaa "

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.settimeout(30)
received = None
try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(data)
    received = sock.recv(1024)
    print("Sent:     {}".format(data))
    print("Received: {}".format(received))
    sock.sendall(data)
    received = sock.recv(1024)
except Exception as EXP:
    print(str(EXP))
finally:
    sock.close()

print ("Sent:     {}".format(data))
print ("Received: {}".format(received))
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(('192.168.0.234', 7700))
# sock.send(b'Test message 111')
# sock.close()
'''
sock = socket.socket()
sock.connect(('localhost', 9090))
data = bytearray(b'hello world!')

i = 0
#while i<10:
sock.send(data)
sock.send(data)
sock.send(data)
sock.send(data)
sock.settimeout(5) # установка таймаута
data_rx = sock.recv(1024)
sock.close()
print (data_rx)
data = bytearray(b'222222222!')
sock = socket.socket()
sock.connect(('localhost', 9090))
sock.send(data)
sock.settimeout(5) # установка таймаута
data_rx = sock.recv(1024)
print (data_rx)
sock.close()
'''
