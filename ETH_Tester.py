#coding: utf8
import socket
import socketserver
import sys
import threading
from configparser import ConfigParser         # импортируем парсер ini файлов

import serial
from BIN_ASCII import *
from BIN_ASCII import Convert_ArrBite_to_ArrCharHex, Convert_ArrBite_to_ArrChar
from CRC16 import *
from Config_ETH_Tester import *
from ETH_Tester_Main import *
from OperationUI import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import QBasicTimer, QTimer
from PyQt5.QtWidgets import QMessageBox
from pyexcel_xlsx import get_data
from pyexcel_xlsx import save_data

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        dataTCP = self.request.recv(1024)
        adr, port = self.client_address
        if len(dataTCP) > 0:
            ETH_Tester.DataRxAppend(myapp, dataTCP, adr, port)

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.dataUDP, socket = self.request
        adr, port = self.client_address
        ETH_Tester.DataRxAppend(myapp, self.dataUDP, adr, port)

class ETH_Tester(QtWidgets.QMainWindow):

    #инициализация окна
    # c:\Python36\Scripts\pyuic5 ETH_Tester_Main.ui -o ETH_Tester_Main.py
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        # инициализация переменных
        self.xlsFilename = ''
        self.cntPosition = CNT_POSITION
        self.log = LOG
        self.txtFilename = DEFAULT_TXT_FILENAME
        self.maxRxLength = MAX_RX_LENGTH

        self.lastLengthRxData = 1
        # словарь для STATUS
        self.CUR_STATUS = {
            "IDLE": 1,
            "RS_SEND": 2,
            "RS_RECIEVE": 3,
            "UDP_SEND": 4,
            "UDP_RECIEVE": 5,
            "UDP_ALL": 6,
            "TCP_SEND": 7,
            "TCP_RECIEVE": 8,
            "TCP_ALL": 9,
        }
        self.STATUS_NEW = 1  # текущее состояние
        self.STATUS_OLD = 1  # прошлое состояние
        self.CUR_CONNECTION = {
            "IDLE": 1,
            "RS": 2,
            "TCP": 3,
            "UDP": 4,
        }
        self.cur_line = 1
        self.activeConnection = 1
        self.counter = 0
        self.sentOne = False
        self.dataTx = []
        self.dataRx = []
        self.dataRx.append(DEFAULT_RX_DATA)
        self.sockUDP = None
        self.sockTCP = None
        self.udpServer = None
        self.tcpServer = None
        self.timerUi = None
        self.curClientAddress = DEFAULT_IP_ADDRESS[0]
        self.curUDPServerPort = DEFAULT_UDP_PORT
        self.curTCPServerPort = DEFAULT_TCP_PORT
        self.curUDPClientPort = DEFAULT_UDP_PORT
        self.curTCPClientPort = DEFAULT_TCP_PORT
        self.connectedTCPClientPort = None
        self.connectedTCPClientAddress = None
        self.curTCPClientThread = None
        #инициализация интерфейса
        self.ui = Ui_ETH_Tester_Main()
        self.ui.setupUi(self)
        #настройка действий по кнопкам
        self.ui.pushButton_Send.clicked.connect(self.SendStopAllPushButtonHandler)             #начинаем передачу файла в порт
        self.ui.pushButton_Send_One_Pack.clicked.connect(self.SendStopOnePushButtonHandler)             #начинаем передачу файла в порт
        self.ui.pushButton_Choice_File.clicked.connect(self.ShowDialog_Open_File)   #выбрать файл
        self.ui.pushButton_open_COM.clicked.connect(self.OpenRsHandler)          #обрабатываем нажатие кнопки отсрыть порт
        self.ui.pushButton_close_COM.clicked.connect(self.CloseRsPushButtonHandler)        #обрабатываем нажатие кнопки закрыть порт
        self.ui.checkBoxXlsSave.stateChanged.connect(self.EnableRxCheckboxHandler)          # обработка изменения состояния checkBoxXlsSave
        self.ui.pushButton_open_TCP_Server.clicked.connect(self.TcpServerOpenHendler)
        self.ui.pushButton_open_UDP_Server.clicked.connect(self.UdpServerOpenHendler)
        self.ui.pushButton_close_UDP_Server.clicked.connect(self.UdpServerCloseHendler)
        self.ui.pushButton_close_TCP_Server.clicked.connect(self.TcpServerCloseHendler)
        self.ui.pushButton_open_UDP_Client.clicked.connect(self.UdpClientConnectHendler)
        self.ui.pushButton_close_UDP_Client.clicked.connect(self.UdpClientDisconnectHendler)
        self.ui.pushButton_open_TCP_Client.clicked.connect(self.TcpClientConnectHendler)
        self.ui.pushButton_close_TCP_Client.clicked.connect(self.TcpClientDisconnectHendler)
        self.ui.pushButtonClearText.clicked.connect(self.ClearTextHendler)

        # вывод строки в statusbar
        self.ui.statusbar.showMessage('Версия 1.00')
        # инициализация RS
        self.InitRS()

        # добавляем нужные скорости в comboBox_Baudrate
        self.ui.comboBox_Baudrate.addItems(BAUDRATES)
        self.ui.comboBox_Baudrate.setCurrentIndex(5)
        # читаем настройки из ini файла
        self.ReadSettings()
        # отобразить имя файла
        ShowFileName(self.xlsFilename, self.ui)

        # задаем начальные параметры lineEdit_UDP_Server_IP_port
        self.ui.lineEdit_UDP_Server_IP_port.setText(str(self.curUDPServerPort))
        self.ui.lineEdit_UDP_Server_IP_port.setInputMask('0000')
        self.ui.lineEdit_UDP_IP_Addr.setInputMask('000.000.000.000')
        self.ui.lineEdit_UDP_IP_Addr.setText(self.curClientAddress)
        self.ui.lineEdit_UDP_Client_IP_Port.setText(str(self.curUDPClientPort))
        self.ui.lineEdit_UDP_Client_IP_Port.setInputMask('0000')

        # добавляем нужные IP адреса для comboBox_IP_Address_UDP_Server
        self.curServerAddress = DEFAULT_IP_ADDRESS
        self.curServerAddress.append(socket.gethostbyname(socket.getfqdn()))
        self.ui.comboBox_IP_Address_UDP_Server.addItems(self.curServerAddress)
        self.ui.comboBox_IP_Address_UDP_Server.setCurrentIndex(len(self.curServerAddress)-1)

        # задаем начальные параметры lineEdit_TCP_Server_IP_port
        self.ui.lineEdit_TCP_Server_IP_port.setText(str(self.curTCPServerPort))
        self.ui.lineEdit_TCP_Server_IP_port.setInputMask('0000')
        self.ui.lineEdit_TCP_IP_Addr.setInputMask('000.000.000.000')
        self.ui.lineEdit_TCP_IP_Addr.setText(self.curClientAddress)
        self.ui.lineEdit_TCP_Client_IP_Port.setText(str(self.curTCPClientPort))
        self.ui.lineEdit_TCP_Client_IP_Port.setInputMask('0000')

        # добавляем нужные IP адреса для comboBox_IP_Address_UDP_Server
        self.ui.comboBox_IP_Address_TCP_Server.addItems(self.curServerAddress)
        self.ui.comboBox_IP_Address_TCP_Server.setCurrentIndex(len(self.curServerAddress)-1)
        # инициализация таймера
        self.startBasicTimer()
        self.startUiUpdateTimer(self.UpdateTextTextEdit)

    # *********************************************************************
    def startBasicTimer(self):
        #инициализация таймера приемника по RS
        self.mainTimer = QBasicTimer()
        self.mainTimer.stop()

    # *********************************************************************
    def startUiUpdateTimer(self, func, interval=DEFAULT_UI_TIMER):
        def handler():
            func()
        self.timerUi = QtCore.QTimer()
        self.timerUi.timeout.connect(handler)
        self.timerUi.start(interval)

    # *********************************************************************
    def DataRxAppend(self, data, address, port):
        '''
        добавить данные к allDataRx
        :return:
        '''
        self.dataRx.append(['Rx:<<<',Convert_ArrBite_to_ArrCharHex(data),
                            Convert_ArrBite_to_ArrChar(data),
                            str(address), str(port)])

    # *********************************************************************
    def SetConnectedTcpClientPort(self, port):
        self.connectedTCPClientPort = port

    # *********************************************************************
    def SetConnectedTcpClientAddress(self, address):
        self.connectedTCPClientAddress = address

    # *********************************************************************
    def TcpServerOpenHendler(self):
        '''
        обработчик нажатия кнопки "Запуск TCP сервера"
        :return:
        '''
        if  self.activeConnection == self.CUR_CONNECTION["IDLE"] or \
                self.activeConnection == self.CUR_CONNECTION["TCP"]  :
            try:
                self.curTCPServerPort = int(self.ui.lineEdit_TCP_Server_IP_port.text())
            except:
                out_str = "Такого порта нет. Введите корректное значение."
                QMessageBox(QMessageBox.Warning, 'Сообщение', out_str, QMessageBox.Ok).exec()
                self.ui.lineEdit_TCP_Server_IP_port.setText(str(DEFAULT_TCP_PORT))
                return
            try:
                self.tcpServer = ThreadedTCPServer((self.ui.comboBox_IP_Address_TCP_Server.currentText(),
                                                               self.curTCPServerPort), ThreadedTCPRequestHandler)
                server_thread = threading.Thread(target = self.tcpServer.serve_forever)
                server_thread.daemon = True
                server_thread.start()
            except Exception as EXP:
                out_str = str(EXP)
                QMessageBox(QMessageBox.Warning, 'Ошибка открытия сокета', out_str, QMessageBox.Ok).exec()
                return
            ChangeButtonsTCPServerConnected(self.ui)
            if self.activeConnection == self.CUR_CONNECTION["IDLE"]:
                self.STATUS_OLD = self.STATUS_NEW
                self.STATUS_NEW = self.CUR_STATUS["TCP_RECIEVE"]
                # переходим в режим RS_RECIEVE если флаг установлен
                self.activeConnection = self.CUR_CONNECTION["TCP"]
            elif self.activeConnection == self.CUR_CONNECTION["TCP"]:
                self.STATUS_OLD = self.STATUS_NEW
                self.STATUS_NEW = self.CUR_STATUS["TCP_ALL"]
            DisableAllButtonsRS(self.ui)
            DisableAllButtonsUDP(self.ui)
            # запускаем обработку таймера
            self.mainTimer.start(DEFAULT_TIMER, self)

    # *********************************************************************
    def UdpServerOpenHendler(self):
        '''
        обработчик нажатия кнопки "Запуск UDP сервера"
        :return:
        '''
        if  self.activeConnection == self.CUR_CONNECTION["IDLE"] or \
                self.activeConnection == self.CUR_CONNECTION["UDP"]  :
            try:
                self.curUDPServerPort = int(self.ui.lineEdit_UDP_Server_IP_port.text())
            except:
                out_str = "Такого порта нет. Введите корректное значение."
                QMessageBox(QMessageBox.Warning, 'Сообщение', out_str, QMessageBox.Ok).exec()
                self.ui.lineEdit_UDP_Server_IP_port.setText(str(DEFAULT_UDP_PORT))
                return
            try:
                self.udpServer = ThreadedUDPServer((self.ui.comboBox_IP_Address_UDP_Server.currentText(),
                                                               self.curUDPServerPort), ThreadedUDPRequestHandler)
                server_thread = threading.Thread(target = self.udpServer.serve_forever)
                server_thread.daemon = True
                server_thread.start()
            except Exception as EXP:
                out_str = str(EXP)
                QMessageBox(QMessageBox.Warning, 'Ошибка открытия сокета', out_str, QMessageBox.Ok).exec()
                return
            ChangeButtonsUDPServerConnected(self.ui)
            if self.activeConnection == self.CUR_CONNECTION["IDLE"]:
                self.STATUS_OLD = self.STATUS_NEW
                self.STATUS_NEW = self.CUR_STATUS["UDP_RECIEVE"]
                # переходим в режим RS_RECIEVE если флаг установлен
                self.activeConnection = self.CUR_CONNECTION["UDP"]
            elif self.activeConnection == self.CUR_CONNECTION["UDP"]:
                self.STATUS_OLD = self.STATUS_NEW
                self.STATUS_NEW = self.CUR_STATUS["UDP_ALL"]
            DisableAllButtonsRS(self.ui)
            DisableAllButtonsTCP(self.ui)
            # запускаем обработку таймера
            self.mainTimer.start(DEFAULT_TIMER, self)

    # *********************************************************************
    def TcpServerCloseHendler(self):
        '''
        обработчик нажатия кнопки "Остановка TCP сервера"
        :return:
        '''
        self.tcpServer.shutdown()
        self.tcpServer.server_close()
        # if self.ui.checkBoxXlsSave.isChecked():
            # записываем принятые данные в XLS
            # self.SaveDataToXls()
        ChangeButtonsTCPServerDisconnected(self.ui)
        if self.STATUS_NEW == self.CUR_STATUS["TCP_ALL"]:
            self.STATUS_OLD = self.STATUS_NEW
            self.STATUS_NEW = self.CUR_STATUS["TCP_SEND"]
        elif self.STATUS_NEW == self.CUR_STATUS["TCP_RECIEVE"] or \
                        self.STATUS_NEW == self.CUR_STATUS["IDLE"]:
            self.STATUS_OLD = self.STATUS_NEW
            self.STATUS_NEW = self.CUR_STATUS["IDLE"]
            self.activeConnection = self.CUR_CONNECTION["IDLE"]
            EnableAllButtonsRS(self.ui)
            EnableAllButtonsUDP(self.ui)
        self.dataTx.clear()
        self.dataRx.clear()
        self.lastLengthRxData = 1
        self.dataRx.append(DEFAULT_RX_DATA)
        self.WriteSettings()

    # *********************************************************************
    def UdpServerCloseHendler(self):
        '''
        обработчик нажатия кнопки "Остановка UDP сервера"
        :return:
        '''
        self.udpServer.shutdown()
        self.udpServer.server_close()
        # if self.ui.checkBoxXlsSave.isChecked():
            # записываем принятые данные в XLS
            # self.SaveDataToXls()
        ChangeButtonsUDPServerDisconnected(self.ui)
        if self.STATUS_NEW == self.CUR_STATUS["UDP_ALL"]:
            self.STATUS_OLD = self.STATUS_NEW
            self.STATUS_NEW = self.CUR_STATUS["UDP_SEND"]
        elif self.STATUS_NEW == self.CUR_STATUS["UDP_RECIEVE"] or \
                self.STATUS_NEW == self.CUR_STATUS["IDLE"]:
            self.STATUS_OLD = self.STATUS_NEW
            self.STATUS_NEW = self.CUR_STATUS["IDLE"]
            self.activeConnection = self.CUR_CONNECTION["IDLE"]
            EnableAllButtonsRS(self.ui)
            EnableAllButtonsTCP(self.ui)
        self.dataTx.clear()
        self.dataRx.clear()
        self.lastLengthRxData = 1
        self.dataRx.append(DEFAULT_RX_DATA)
        self.WriteSettings()

    # *********************************************************************
    def UdpClientConnectHendler(self):
        if self.activeConnection == self.CUR_CONNECTION["IDLE"] or \
                        self.activeConnection == self.CUR_CONNECTION["UDP"]:
            try:
                self.sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.curClientAddress = self.ui.lineEdit_UDP_IP_Addr.text()
                self.curUDPClientPort = int(self.ui.lineEdit_UDP_Client_IP_Port.text())
            except:
                out_str = "Такого порта нет. Введите корректное значение."
                QMessageBox(QMessageBox.Warning, 'Сообщение', out_str, QMessageBox.Ok).exec()
                self.ui.lineEdit_UDP_Client_IP_Port.setText(str(DEFAULT_UDP_PORT))
                return
            # изменяем активность виджетов внешнего вида
            ChangeButtonsUDPClientConnected(self.ui)
            if self.activeConnection == self.CUR_CONNECTION["IDLE"]:
                self.STATUS_OLD = self.STATUS_NEW
                self.STATUS_NEW = self.CUR_STATUS["UDP_SEND"]
                # переходим в режим UDP если флаг установлен
                self.activeConnection = self.CUR_CONNECTION["UDP"]
            elif self.activeConnection == self.CUR_CONNECTION["UDP"]:
                self.STATUS_OLD = self.STATUS_NEW
                self.STATUS_NEW = self.CUR_STATUS["UDP_ALL"]
            DisableAllButtonsRS(self.ui)
            DisableAllButtonsTCP(self.ui)
            # запускаем обработку таймера
            self.mainTimer.start(DEFAULT_TIMER, self)

    # *********************************************************************
    def TcpClientConnectHendler(self):
        if self.activeConnection == self.CUR_CONNECTION["IDLE"] or \
                        self.activeConnection == self.CUR_CONNECTION["TCP"]:
            try:
                self.curClientAddress = self.ui.lineEdit_TCP_IP_Addr.text()
                self.curTCPClientPort = int(self.ui.lineEdit_TCP_Client_IP_Port.text())

            except:
                out_str = "Такого порта нет. Введите корректное значение."
                QMessageBox(QMessageBox.Warning, 'Сообщение', out_str, QMessageBox.Ok).exec()
                self.ui.lineEdit_UDP_Client_IP_Port.setText(str(DEFAULT_UDP_PORT))
                return
            # изменяем активность виджетов внешнего вида
            ChangeButtonsTCPClientConnected(self.ui)
            # тестовое подключение к sockTCP
            try:
                self.sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sockTCP.connect((self.curClientAddress, self.curTCPClientPort))
            except Exception as EXP:
                # изменяем активность виджетов внешнего вида
                ChangeButtonsTCPClientDisconnected(self.ui)
                out_str = "Невозможно подключиться по указанному адресу и порту: {}".format(str(EXP))
                QMessageBox(QMessageBox.Warning, 'Ошибка подключения.', out_str, QMessageBox.Ok).exec()
            finally:
                self.sockTCP.close()
            if self.activeConnection == self.CUR_CONNECTION["IDLE"]:
                self.STATUS_OLD = self.STATUS_NEW
                self.STATUS_NEW = self.CUR_STATUS["TCP_SEND"]
                # переходим в режим UDP если флаг установлен
                self.activeConnection = self.CUR_CONNECTION["TCP"]
            elif self.activeConnection == self.CUR_CONNECTION["TCP"]:
                self.STATUS_OLD = self.STATUS_NEW
                self.STATUS_NEW = self.CUR_STATUS["TCP_ALL"]
            DisableAllButtonsRS(self.ui)
            DisableAllButtonsUDP(self.ui)
            # запускаем обработку таймера
            self.mainTimer.start(DEFAULT_TIMER, self)

    # *********************************************************************
    def UdpClientDisconnectHendler(self):
        # изменяем активность виджетов внешнего вида
        ChangeButtonsUDPClientDisconnected(self.ui)
        if self.STATUS_NEW == self.CUR_STATUS["UDP_ALL"]:
            self.STATUS_OLD = self.STATUS_NEW
            self.STATUS_NEW = self.CUR_STATUS["UDP_RECIEVE"]
        elif self.STATUS_NEW == self.CUR_STATUS["UDP_SEND"] or \
                self.STATUS_NEW == self.CUR_STATUS["IDLE"]:
            self.STATUS_OLD = self.STATUS_NEW
            self.STATUS_NEW = self.CUR_STATUS["IDLE"]
            self.activeConnection = self.CUR_CONNECTION["IDLE"]
            EnableAllButtonsRS(self.ui)
            EnableAllButtonsTCP(self.ui)
        self.dataTx.clear()
        self.WriteSettings()

    # *********************************************************************
    def TcpClientDisconnectHendler(self):
        # изменяем активность виджетов внешнего вида
        ChangeButtonsTCPClientDisconnected(self.ui)
        if self.STATUS_NEW == self.CUR_STATUS["TCP_ALL"]:
            self.STATUS_OLD = self.STATUS_NEW
            self.STATUS_NEW = self.CUR_STATUS["TCP_RECIEVE"]
        elif self.STATUS_NEW == self.CUR_STATUS["TCP_SEND"] or \
                self.STATUS_NEW == self.CUR_STATUS["IDLE"]:
            self.STATUS_OLD = self.STATUS_NEW
            self.STATUS_NEW = self.CUR_STATUS["IDLE"]
            self.activeConnection = self.CUR_CONNECTION["IDLE"]
            EnableAllButtonsRS(self.ui)
            EnableAllButtonsUDP(self.ui)
        self.dataTx.clear()
        self.WriteSettings()

    # *********************************************************************
    def ClearTextHendler(self):
        self.ui.plainTextEdit.clear()

    #*********************************************************************
    def ReadSettings(self):
        '''
        чтение настроек из ini файла
        :return:
        '''
        #читаем переменные из файла настроек при первом входе
        try:
            # определяем парсер конфигурации из ini файла
            self.config = ConfigParser()
            # читаем конфигурацию
            self.config.read(DEFAULT_SETTINGS_FILENAME)
            # Читаем нужные значения
            self.xlsFilename = ['', '']
            self.xlsFilename[0] = self.config.get('main', 'filename')
            self.txtFilename = self.config.get('main', 'txt_filename')
            self.cntPosition = int(self.config.get('main', 'cnt_position'))
            self.maxRxLength = int(self.config.get('main', 'max_rx_length'))
            self.curClientAddress = self.config.get('main', 'last_client_address')
            self.curUDPClientPort = int(self.config.get('main', 'last_udp_client_port'))
            self.curUDPServerPort = int(self.config.get('main', 'last_udp_server_port'))
            self.curTCPClientPort = int(self.config.get('main', 'last_tcp_client_port'))
            self.curTCPServerPort = int(self.config.get('main', 'last_tcp_server_port'))
            #self.log = self.config.getboolean('main', 'log')
        except :
            # add a new section and some values
            try:
                self.config.add_section('main')
                # записываем настройки в ini
                self.WriteSettings()
            except:
                # записываем настройки в ini
                self.WriteSettings()

    # *********************************************************************
    def WriteSettings(self):
        '''
        # запись текущих настороек в ini
        :return:
        '''
        # изменяем запись в файле ini
        if self.xlsFilename != '':
            self.config.set('main', 'filename', self.xlsFilename[0])
        else:
            self.config.set('main', 'filename', '')
        self.config.set('main', 'cnt_position', str(self.cntPosition))
        self.config.set('main', 'max_rx_length', str(self.maxRxLength))
        self.config.set('main', 'txt_filename', DEFAULT_TXT_FILENAME)
        self.config.set('main', 'last_client_address', self.curClientAddress)
        self.config.set('main', 'last_udp_client_port', str(self.curUDPClientPort))
        self.config.set('main', 'last_udp_server_port', str(self.curUDPServerPort))
        self.config.set('main', 'last_tcp_client_port', str(self.curTCPClientPort))
        self.config.set('main', 'last_tcp_server_port', str(self.curTCPServerPort))
        # записываем изменения в файл
        with open(DEFAULT_SETTINGS_FILENAME, 'w') as configfile:
            self.config.write(configfile)

    # *********************************************************************
    def InitRS(self):
        '''
        первоначальная инициализация RS
        :return:
        '''
        list_com_ports = '' #перечень доступных портов
        #проверка какие порты свободны
        try:
            portList = self.ScanRsPorts()
            for s in portList:
                list_com_ports += s + ' '
        except Exception as EXP:
            QMessageBox(QMessageBox.Critical, 'Ошибка', str(EXP), QMessageBox.Ok).exec()

        finally:
            #настройка списка для выбора порта
            #добавляем свободные порты в comboBox_COM
            self.ui.comboBox_COM.clear()
            self.ui.comboBox_COM.addItems(list_com_ports.split())
            self.ui.comboBox_COM.setCurrentIndex(0)

    # *********************************************************************
    def EnableRxCheckboxHandler(self):
        '''
        включение / выключение записи принятых данных в файл
        :return:
        '''
        if self.activeConnection == self.CUR_CONNECTION["RS"]:
            if self.ui.checkBoxXlsSave.isChecked():
                self.STATUS_OLD = self.STATUS_NEW
                self.STATUS_NEW = self.CUR_STATUS["RS_RECIEVE"]
            else:
                self.STATUS_OLD = self.STATUS_NEW
                self.STATUS_NEW = self.CUR_STATUS["IDLE"]
                self.lastLengthRxData = 1
            self.mainTimer.start(DEFAULT_TIMER, self)  # запускаем обработку таймера

    #*********************************************************************
    def OpenRsHandler(self):
        '''
        обработчик открытия порта
        :return:
        '''
        if self.ui.comboBox_COM.currentText() != '':
            # проверяем текущее соединение
            if self.activeConnection == self.CUR_CONNECTION["IDLE"]:
                DisableAllButtonsUDP(self.ui)
                DisableAllButtonsTCP(self.ui)
                self.SerialConfig()    #инициализируем порт
                if self.ui.checkBoxXlsSave.isChecked():
                    # переходим в режим RS_RECIEVE если флаг установлен
                    self.STATUS_OLD = self.STATUS_NEW
                    self.STATUS_NEW = self.CUR_STATUS["RS_RECIEVE"]
                    self.mainTimer.start(DEFAULT_TIMER, self)  # запускаем обработку таймера
                ChangeRsButtonsIdle(self.ui, self.xlsFilename)  #активируем кнопки
                self.activeConnection = self.CUR_CONNECTION["RS"]  # Текущее соединение по RS
            else:
                out_str = "Соединение уже установлено. Для выполения подключения нужно закрыть текущее соединение."
                QMessageBox(QMessageBox.Warning, 'Сообщение', out_str, QMessageBox.Ok).exec()
        else:
            out_str = "Порт не выбран."
            QMessageBox(QMessageBox.Warning, 'Сообщение', out_str, QMessageBox.Ok).exec()

    #*********************************************************************
    def PreparationTxData(self):
        # читаем данные для отправки из xls файла
        try:
            self.dataTx = Del_Spaces(self.ReadXlsData(self.xlsFilename)[TX_DATA_PAGE])
        except KeyError:
            QMessageBox(QMessageBox.Critical, 'Ошибка', 'Нет такой страницы в файле',
                        QMessageBox.Ok).exec()
            return
        # обнуляем принятые данные
        self.dataRx.clear()
        self.dataRx.append(DEFAULT_RX_DATA)
        if self.activeConnection == self.CUR_CONNECTION["RS"]:
            self.STATUS_OLD = self.STATUS_NEW  # прошлое состояние
            self.STATUS_NEW = self.CUR_STATUS["RS_SEND"]  # текущее состояние
            ChangeButtonsRsSend(self.ui)
        elif self.activeConnection == self.CUR_CONNECTION["UDP"]:
            ChangeButtonsUDPSend(self.ui)
            if self.STATUS_NEW == self.CUR_STATUS["UDP_RECIEVE"]:
                # переходим в режим UDP_ALL
                self.STATUS_OLD = self.STATUS_NEW
                self.STATUS_NEW = self.CUR_STATUS["UDP_ALL"]
            elif self.STATUS_NEW == self.CUR_STATUS["IDLE"]:
                # переходим в режим UDP_SEND
                self.STATUS_OLD = self.STATUS_NEW
                self.STATUS_NEW = self.CUR_STATUS["UDP_SEND"]
        elif self.activeConnection == self.CUR_CONNECTION["TCP"]:
            ChangeButtonsTCPSend(self.ui)
            if self.STATUS_NEW == self.CUR_STATUS["TCP_RECIEVE"]:
                # переходим в режим UDP_ALL
                self.STATUS_OLD = self.STATUS_NEW
                self.STATUS_NEW = self.CUR_STATUS["TCP_ALL"]
            elif self.STATUS_NEW == self.CUR_STATUS["IDLE"]:
                # переходим в режим UDP_SEND
                self.STATUS_OLD = self.STATUS_NEW
                self.STATUS_NEW = self.CUR_STATUS["TCP_SEND"]
        self.cur_line = 1

    #*********************************************************************
    def ReturnUiIdle(self):
        if self.activeConnection == self.CUR_CONNECTION["RS"]:
            ChangeRsButtonsIdle(self.ui, self.xlsFilename)
        elif self.activeConnection == self.CUR_CONNECTION["UDP"]:
            ChangeUDPButtonsIdle(self.ui, self.xlsFilename)
        elif self.activeConnection == self.CUR_CONNECTION["TCP"]:
            ChangeTCPButtonsIdle(self.ui, self.xlsFilename)

    #*********************************************************************
    def SendStopAllPushButtonHandler(self):
        '''
        обработчик кнопки Отправить данные/Прервать
        :return:
        '''
        try:
            # изменяем состояние кнопок и запускаем передачу когда RS был открыт
            if self.activeConnection == self.CUR_CONNECTION["RS"] or \
                    self.activeConnection == self.CUR_CONNECTION["UDP"] or \
                    self.activeConnection == self.CUR_CONNECTION["TCP"]:
                if self.ui.pushButton_Send.text() == 'Отправить данные':
                    self.PreparationTxData()
                    self.sentOne = False
                    self.mainTimer.start(DEFAULT_TIMER, self)  # запускаем обработку таймера
                else:
                    # запись принятых данных в xls
                    self.SaveDataToXls()
                    # возвращаем кнопки в исходное состояние
                    self.ReturnUiIdle()
                    self.dataTx.clear()
                    self.dataRx.clear()
                    self.dataRx.append(DEFAULT_RX_DATA)
                    self.sentOne = False
                self.lastLengthRxData = 1
            else:
                QMessageBox(QMessageBox.Warning, 'Ошибка', 'Подключение отсутствует', QMessageBox.Ok).exec()
        except Exception as EXP:
            QMessageBox(QMessageBox.Critical, 'Ошибка', str(EXP), QMessageBox.Ok).exec()

    #*********************************************************************
    def SendStopOnePushButtonHandler(self):
        '''
        обработчик кнопки Отправить один пакет
        :return:
        '''
        try:
            # изменяем состояние кнопок и запускаем передачу когда RS был открыт
            if self.activeConnection == self.CUR_CONNECTION["RS"] or \
                    self.activeConnection == self.CUR_CONNECTION["UDP"] or \
                    self.activeConnection == self.CUR_CONNECTION["TCP"]:
                if self.sentOne == False:
                    self.PreparationTxData()
                    self.lastLengthRxData = 1
                    self.sentOne = True
                self.mainTimer.start(DEFAULT_TIMER, self)  # запускаем обработку таймера
            else:
                QMessageBox(QMessageBox.Warning, 'Ошибка', 'Подключение отсутствует', QMessageBox.Ok).exec()
        except Exception as EXP:
            QMessageBox(QMessageBox.Critical, 'Ошибка', str(EXP), QMessageBox.Ok).exec()

    #*********************************************************************
    def CloseRsPushButtonHandler(self):
        '''
        обработчик кнопки закрытия порта
        :return:
        '''
        # записываем принятые данные в XLS
        # self.SaveDataToXls()
        # закрываем порт
        self.ser.close()
        # активного соединения нет
        self.activeConnection = self.CUR_CONNECTION["IDLE"]
        # переходим в режим IDLE
        self.STATUS_OLD = self.STATUS_NEW
        self.STATUS_NEW = self.CUR_STATUS["IDLE"]
        self.lastLengthRxData = 1
        self.dataTx.clear()
        # выключаем все кнопки и элементы выбора
        #ChangeActiveButtonsRsClose(self.ui)
        EnableAllButtonsUDP(self.ui)
        EnableAllButtonsTCP(self.ui)
        ChangeActiveButtonsRsSelected(self.ui)  #изменяем кнопки для выбора порта и скорости        self.WriteSettings()
        self.WriteSettings()

    #*********************************************************************
    def ScanRsPorts(self):
        """scan for available ports. return a list of tuples (num, name)"""
        available = []
        for i in range(NUMBER_SCAN_PORTS):
            try:
                s = serial.Serial(i)
                available.append((s.portstr))
                s.close()   # explicit close 'cause of delayed GC in java
            except serial.SerialException:
                pass
        return available

    #*********************************************************************
    def SerialConfig(self):
        '''
        настройка порта со значением выбранным в comboBox_COM
        :return:
        '''
        baudrate = int(self.ui.comboBox_Baudrate.currentText())
        try:
            #проверяем есть ли порт
            if self.ser.isOpen() == False:#
                self.ser = serial.Serial(self.ui.comboBox_COM.currentText(),
                    baudrate=baudrate,#9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=0,
                    bytesize=serial.EIGHTBITS,
                    xonxoff=0)
        except:
            try:
                self.ser = serial.Serial(self.ui.comboBox_COM.currentText(),
                        baudrate=baudrate,#9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=0,
                        bytesize=serial.EIGHTBITS,
                        xonxoff=0)
                if baudrate == 115200:
                    self.TIME_TO_RX = 40#было 40
                elif baudrate == 57600:
                    self.TIME_TO_RX = 60#было 60
                elif baudrate == 38400:
                    self.TIME_TO_RX = 80#было 80
                elif baudrate == 19200:
                    self.TIME_TO_RX = 100#
                elif baudrate == 9600:
                    self.TIME_TO_RX = 150#
                elif baudrate == 1200:
                    self.TIME_TO_RX = 1200#
                elif baudrate == 230400:
                    self.TIME_TO_RX = 40#
                elif baudrate == 460800:
                    self.TIME_TO_RX = 40#
                elif baudrate == 921600:
                    pass
                self.TIME_TO_RX_DATA = 10#
            except:
                out_str = "Порт будет закрыт, повторите прошивку заново."
                QMessageBox(QMessageBox.Warning, 'Ошибка №2 работы с портом ',out_str , QMessageBox.Ok).exec()
                #Закрытие порта и выключение записи - переход в исходное состояние
                self.STATUS_OLD = self.STATUS_NEW
                self.STATUS_NEW = self.ID2["IDLE"]
                self.CloseRsPushButtonHandler()
                return

    #*********************************************************************
    def RecieveRsData (self):
        '''
        проверка наличия данных в буфере RS и получение данных из порта
        :return:
        '''
        RX_Data = ''  #данных нет
        while self.ser.inWaiting() > 0:
            RX_Data = self.ser.read(MAX_WAIT_BYTES)
        if LOG == True:
            self.string_Data = '<< ' + str(len(RX_Data)) + ' байт '
            for i in range(len(RX_Data)):
                self.string_Data = self.string_Data + ' ' + str(hex(RX_Data[i]))
            print (self.string_Data)
            # записываем в лог файл принятые данные
            self.logfile.write(self.string_Data + '\n')
        return RX_Data

    #*********************************************************************
    def SetCounter(self, data):
        '''
        автоматическое заполнение позиции счетчика пакетов
        :param data:
        :return:
        '''
        if len(data) > self.cntPosition:
            data[self.cntPosition] = self.counter
            self.counter += 1
            if self.counter == 256:
                self.counter = 0
            return True
        else:
            out_str = 'Длина данных меньше положенной в строке {0:d}'.format(self.cur_line + 1)
            QMessageBox(QMessageBox.Warning, 'Ошибка длины данных ', out_str, QMessageBox.Ok).exec()
            return False

    #*********************************************************************
    def TransmitListData (self, string_data):
        '''
        выполнить передачу данных
        :param string_data: данные для передачи
        :return:
        '''
        #установка начальног значения CRC16
        try:
            crc = INITIAL_MODBUS
            if self.activeConnection == self.CUR_CONNECTION["RS"]:
                #проверка открыт ли порт
                self.ser.isOpen()
            if self.cur_line < len(string_data):
                if len(string_data[self.cur_line]) > XLS_DATA["DATA"]:
                    dataToSend = string_data[self.cur_line][XLS_DATA["DATA"]]
                    if dataToSend != '':
                        try:
                            if string_data[self.cur_line][XLS_DATA["FORMAT"]] == 'HEX':
                                bin_data = Convert_HexStr_to_Bytearray(dataToSend)
                            else:
                                bin_data = Convert_Str_to_Bytearray(dataToSend)
                        except ValueError as EXP:
                            out_str = 'Ошибка преобразовани данных  в строке {0:d} "{1}"'.format ( self.cur_line + 1, str(EXP))
                            QMessageBox(QMessageBox.Warning, 'Ошибка преобразовани данных ',
                                                          out_str, QMessageBox.Ok).exec()
                            return False
                        # проверяем нужно ли автоматически проставлять счетчик непрерывности
                        if string_data[self.cur_line][XLS_DATA["CNT"]] == 'Y':
                            # выполняем замену позиции CNT в пакете
                            if not self.SetCounter(bin_data):
                                return False
                        if string_data[self.cur_line][XLS_DATA["CRC"]] == 'Y':
                            # производим рассчет CRC16 для self.rs_send_pack
                            for ch in bin_data:
                                crc = calcByte(ch, crc)
                            bin_data += crc.to_bytes(2, byteorder='little')
                        # записываем данные в ЛОГ файл и консоль
                        self.LogData()
                        self.dataRx.append(['Tx:>>>', Convert_ArrBite_to_ArrCharHex(bin_data),
                                            Convert_ArrBite_to_ArrChar(bin_data)])
                        if self.activeConnection == self.CUR_CONNECTION["RS"]:
                            # передаем данные в порт RS
                            self.ser.write(bin_data)
                        elif self.activeConnection == self.CUR_CONNECTION["UDP"]:
                            # передаем данные в sockUDP
                            self.sockUDP.sendto(bin_data, (self.curClientAddress, self.curUDPClientPort))
                        elif self.activeConnection == self.CUR_CONNECTION["TCP"]:
                            # передаем данные в sockTCP
                            try:
                                self.sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                self.sockTCP.connect((self.curClientAddress, self.curTCPClientPort))
                                self.sockTCP.sendall(bin_data)
                            except Exception as EXP:
                                self.ui.plainTextEdit.appendPlainText('Ошибка передачи пакета: {}'.format(str(EXP)))
                            finally:
                                self.sockTCP.close()
                # готовим следующие данные для передачи
                self.cur_line = self.IncLine(string_data, self.cur_line)
                return True
            else:
                if self.ui.checkBoxCiclicSend.isChecked():
                    # повторяем отправку данных
                    self.dataTx = Del_Spaces(
                        self.ReadXlsData(self.xlsFilename)[TX_DATA_PAGE])
                    self.cur_line = 1
                    return True
                else:
                    return False
        except Exception as EXP:
            print (EXP)

    #*********************************************************************
    def SaveDataToXls(self):
        '''
        запись принятых данных в xls
        :return:
        '''
        if len(self.dataRx) > 0:
            try:
                data_rx = get_data(self.xlsFilename[0])
                data_rx.update({"RX_Data": self.dataRx})
                if len(self.dataRx) < self.maxRxLength:
                    save_data(self.xlsFilename[0], data_rx)
                else:
                    self.SavedataToTxt(self.dataRx, self.txtFilename)
                return True
            except Exception as EXP:
                # останавливаем отправку данных
                ChangeRsButtonsIdle(self.ui, self.xlsFilename)
                self.STATUS_OLD = self.STATUS_NEW
                self.STATUS_NEW = self.CUR_STATUS["IDLE"]
                self.lastLengthRxData = 1
                QMessageBox(QMessageBox.Critical, 'Ошибка записи файла данных: ',
                            'Ошибка работы с файлом для записи: ' + str(EXP),
                                               QtWidgets.QMessageBox.Ok).exec()
        return False

    #*********************************************************************
    def SavedataToTxt(self, data,fileName):
        '''
        запись списка данных в текстовый файл
        :param data:
        :return:
        '''
        writeData = ''
        for d in data:
            writeData += str(d)[1:-1] + '\n'
        with open(fileName, 'w', encoding='utf-8') as f:
            f.write(writeData)
        QMessageBox(QMessageBox.Warning, 'Превышение длины данных',
                                       'Превышена длина данных для записи в xls. Данные были записаны в файл ' + self.txtFilename,
                                       QtWidgets.QMessageBox.Ok).exec()

    #*********************************************************************
    def LogData(self):
        if LOG == True:
            # записываем в лог файл пепелаееые алееые
            self.logfile.write(self.string_data + '\n')
            # выводим переданные данные в консоль
            print(self.string_data)

    #*********************************************************************
    def IncLine(self, string_data, cur_line):
        '''
        уменьшение количества повторений и переход на новую строку при количестве повторений 0
        :param string_data:
        :param cur_line:
        :return:
        '''
        try:
            repeat = int(string_data[cur_line][XLS_DATA["REPEAT"]])
            if repeat > 1:
                repeat -= 1
                string_data[cur_line][XLS_DATA["REPEAT"]] = str ( repeat )
            else:
                cur_line += 1
            return cur_line
        except Exception as EXP:
            cur_line += 1
            return cur_line

    #*********************************************************************
    def ShowDialog_Open_File(self):
        '''
        Обработка кнопки открытия файла
        :return:
        '''
        try:
            self.xlsFilename = QtWidgets.QFileDialog.getOpenFileName(
                   self, 'Open File', self.xlsFilename[0] , 'XLS файл (*.xls)',
                   None, QtWidgets.QFileDialog.DontUseNativeDialog)
        except:
            self.xlsFilename = QtWidgets.QFileDialog.getOpenFileName(
                self, 'Open File', '', 'XLS файл (*.xls)',
                None, QtWidgets.QFileDialog.DontUseNativeDialog)
        if self.xlsFilename[0] != '':
            self.ui.pushButton_Send.setEnabled(SET)  # активируем кнопку "Отправить данные"
            self.WriteSettings() # записать название файла в ini файл настроек
            # отображаем имя открытого файла
            ShowFileName(self.xlsFilename, self.ui)
        else:
            # читаем название файла из настроек
            self.ReadSettings()

    #*********************************************************************
    def ReadXlsData(self, file_name):
        '''
        Чтение данных для отправки из XLS файла
        :return: данные
        '''
        try:
            data_rx = None
            if file_name != None:
                data_rx = get_data(file_name[0])
            return data_rx

        except Exception as EXP:
            QMessageBox(QMessageBox.Critical, 'Ошибка обработки файла данных для передачи', str(EXP),
                                       QMessageBox.Ok).exec()

    #*********************************************************************
    def ParseData(self, data):
        '''
        парсинг пакетов позиционирования на основе стартовый байт RS_START
        :param data: данные для парсинга
        :return: returnData - список пакетов
        '''
        returnData = []
        if data != '':
            try:
                indexStart = 0
                indexStop = 0
                lenData = len(data)
                if lenData > 0:
                    for i in range(lenData - 1):
                       if data[i] == RS_START[0] and data[i+1] == RS_START[1]:
                           indexStop = i
                           if indexStop > indexStart:
                               returnData.append(data[indexStart:indexStop])
                               indexStart = i
                    if indexStart == indexStop:
                        returnData.append(data[indexStart:])
            except Exception as EXP:
                out_str = str(EXP)
                QMessageBox(QMessageBox.Warning, 'Ошибка.', out_str, QMessageBox.Ok).exec()
        return returnData


    #*********************************************************************
    def GetRsData(self):
        try:
            currentData = self.ParseData(self.RecieveRsData())
            if currentData != []:
                lenCurData = len(currentData)
                # проверяем установлена ли птичка записи в файл
                if self.ui.checkBoxXlsSave.isChecked():
                    if lenCurData > 0:
                        for d in currentData:
                                self.dataRx.append([Convert_ArrBite_to_ArrCharHex(d),
                                                    Convert_ArrBite_to_ArrChar(d)])
            else:
                pass
        except:
            pass

    #*********************************************************************
    def timerEvent(self, e):
        '''
        обработчик таймера
        :param e:
        :return:
        '''
        self.mainTimer.stop() #выключаем таймер
        try:
            if self.STATUS_NEW == self.CUR_STATUS["RS_SEND"] or \
                    self.STATUS_NEW == self.CUR_STATUS["UDP_SEND"] or \
                    self.STATUS_NEW == self.CUR_STATUS["UDP_ALL"] or \
                    self.STATUS_NEW == self.CUR_STATUS["TCP_SEND"] or \
                    self.STATUS_NEW == self.CUR_STATUS["TCP_ALL"]:
                if self.activeConnection == self.CUR_CONNECTION["RS"]:
                    # получаем принятые данные
                    self.GetRsData()
                curTimer = DEFAULT_TIMER
                if self.dataTx != []:
                    if self.TransmitListData(self.dataTx):
                        if self.cur_line < len(self.dataTx):
                            try:
                                curTimer = int(self.dataTx[self.cur_line][XLS_DATA["DELAY"]])
                                if curTimer < DEFAULT_TIMER:
                                    # если задана задержка меньше TIMER, используем TIMER
                                    curTimer = DEFAULT_TIMER
                            except:
                                curTimer = DEFAULT_TIMER
                        # if self.ui.checkBoxShowRxData.isChecked():
                            # if self.STATUS_NEW != self.CUR_STATUS["UDP_SEND"] or \
                            #                 self.STATUS_NEW != self.CUR_STATUS["UDP_ALL"] or \
                            #                 self.STATUS_NEW != self.CUR_STATUS["TCP_SEND"]:
                            # self.UpdateTextTextEdit()
                        # запускаем таймер только в режиме отправки всех данных
                        if self.sentOne == False:
                            self.mainTimer.start(curTimer, self) # запускаем обработку таймера
                    else:
                        if self.activeConnection == self.CUR_CONNECTION["RS"]:
                            # останавливаем отправку данных
                            ChangeRsButtonsIdle(self.ui, self.xlsFilename)
                            # запись принятых данных в xls
                            self.GetRsData()
                        elif self.activeConnection == self.CUR_CONNECTION["UDP"]:
                            ChangeUDPButtonsIdle(self.ui, self.xlsFilename)
                        elif self.activeConnection == self.CUR_CONNECTION["TCP"]:
                            ChangeTCPButtonsIdle(self.ui, self.xlsFilename)
                        # if self.ui.checkBoxShowRxData.isChecked():
                        #     self.UpdateTextTextEdit()
                        self.SaveDataToXls()
                        # self.lastLengthRxData = 1
                        self.dataTx.clear()
                        self.sentOne = False
                        QMessageBox(QMessageBox.Warning, 'Завершение ', "Все данные переданы.", QMessageBox.Ok).exec()
            elif self.STATUS_NEW == self.CUR_STATUS["RS_RECIEVE"]:
                # получаем данные
                self.GetRsData()
                if self.ui.checkBoxShowRxData.isChecked():
                    self.UpdateTextTextEdit()
                self.mainTimer.start(DEFAULT_TIMER, self)  # запускаем обработку таймера
            elif self.STATUS_NEW == self.CUR_STATUS["UDP_RECIEVE"]:
                self.mainTimer.start(DEFAULT_TIMER, self)  # запускаем обработку таймера
                if self.ui.checkBoxShowRxData.isChecked():
                    self.UpdateTextTextEdit()
            elif self.STATUS_NEW == self.CUR_STATUS["TCP_RECIEVE"]:
                self.mainTimer.start(DEFAULT_TIMER, self)  # запускаем обработку таймера
                if self.ui.checkBoxShowRxData.isChecked():
                    self.UpdateTextTextEdit()
        except Exception as EXP:
            out_str = str(EXP)
            QMessageBox(QMessageBox.Warning, 'Ошибка.',out_str , QMessageBox.Ok).exec()
            #Закрытие порта и выключение записи - переход в исходное состояние
            self.STATUS_OLD = self.STATUS_NEW
            self.STATUS_NEW = self.ID2["IDLE"]
            self.CloseRsPushButtonHandler()
            return

    #*********************************************************************
    def UpdateTextTextEdit(self):
        '''
        вывод принятых данных в TextEdit
        :return:
        '''
        lenData = len(self.dataRx)
        if self.lastLengthRxData != lenData:
            while self.lastLengthRxData < lenData:
                self.lastLengthRxData += 1
                self.ui.plainTextEdit.appendPlainText('{} Str: {}\nHex: {}'.format(
                    self.dataRx[self.lastLengthRxData - 1][0],
                    self.dataRx[self.lastLengthRxData - 1][2],
                    self.dataRx[self.lastLengthRxData - 1][1]))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = ETH_Tester()
    myapp.show()
    sys.exit(app.exec_())

