# -*- coding: utf-8 -*-
'''
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind('127.0.0.1', 7700)
sock.listen(5)

sock.connect(('localhost', 9090))
sock.send(data)
sock.settimeout(5) # установка таймаута
data_rx = sock.recv(1024)

    def handle(self):
#TODO - продолить тут с запоминания адреса и порта входящего соединения
        self.dataTCP = self.request.recv(1024)
        adr, port = self.client_address
        ETH_Tester.SetConnectedTcpClientPort(myapp, port)
        ETH_Tester.SetConnectedTcpClientAddress(myapp, adr)
        cur_thread = self
        # cur_thread = threading.current_thread()
        ETH_Tester.SetTcpThread(myapp, self.request.sendall)
        # self.request.sendall(self.dataTCP + self.dataTCP)
        print('Data: {}'.format(self.dataTCP.decode()))
        print('Adress: {}'.format(self.client_address[0]))
        # , socket = self.request
        ETH_Tester.DataRxAppend(myapp, self.dataTCP)
'''
