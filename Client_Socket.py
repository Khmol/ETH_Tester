#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

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
