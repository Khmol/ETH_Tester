import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(False)

with sock as s:
    print('Bind 8888')
    sock.bind(('127.0.0.1', 8888))

    while True:
        result = sock.recv(1024)
        print('Message', result.decode('utf-8'))
