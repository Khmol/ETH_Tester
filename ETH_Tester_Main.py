# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ETH_Tester_Main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ETH_Tester_Main(object):
    def setupUi(self, ETH_Tester_Main):
        ETH_Tester_Main.setObjectName("ETH_Tester_Main")
        ETH_Tester_Main.resize(635, 455)
        ETH_Tester_Main.setMinimumSize(QtCore.QSize(635, 455))
        ETH_Tester_Main.setMaximumSize(QtCore.QSize(635, 455))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../Users/Users/Users/Users/Users/Users/Users/Users/User/.designer/backup/touchscreen.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap("../../../Users/Users/Users/Users/Users/Users/Users/Users/User/.designer/backup/touchscreen.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        ETH_Tester_Main.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(ETH_Tester_Main)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_Choice_File = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Choice_File.setEnabled(True)
        self.pushButton_Choice_File.setGeometry(QtCore.QRect(460, 215, 171, 23))
        self.pushButton_Choice_File.setObjectName("pushButton_Choice_File")
        self.label_File_Name = QtWidgets.QLabel(self.centralwidget)
        self.label_File_Name.setGeometry(QtCore.QRect(14, 220, 441, 16))
        self.label_File_Name.setObjectName("label_File_Name")
        self.pushButton_Send = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Send.setEnabled(False)
        self.pushButton_Send.setGeometry(QtCore.QRect(400, 380, 201, 23))
        self.pushButton_Send.setStyleSheet("")
        self.pushButton_Send.setObjectName("pushButton_Send")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(9, 270, 384, 131))
        self.plainTextEdit.setMinimumSize(QtCore.QSize(10, 10))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 621, 201))
        self.tabWidget.setObjectName("tabWidget")
        self.RS = QtWidgets.QWidget()
        self.RS.setObjectName("RS")
        self.groupBox = QtWidgets.QGroupBox(self.RS)
        self.groupBox.setGeometry(QtCore.QRect(0, 10, 461, 80))
        self.groupBox.setObjectName("groupBox")
        self.pushButton_close_COM = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_close_COM.setEnabled(False)
        self.pushButton_close_COM.setGeometry(QtCore.QRect(340, 40, 111, 23))
        self.pushButton_close_COM.setObjectName("pushButton_close_COM")
        self.pushButton_open_COM = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_open_COM.setGeometry(QtCore.QRect(222, 40, 111, 23))
        self.pushButton_open_COM.setAutoFillBackground(False)
        self.pushButton_open_COM.setObjectName("pushButton_open_COM")
        self.comboBox_Baudrate = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_Baudrate.setGeometry(QtCore.QRect(113, 41, 101, 20))
        self.comboBox_Baudrate.setObjectName("comboBox_Baudrate")
        self.comboBox_COM = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_COM.setGeometry(QtCore.QRect(9, 41, 91, 20))
        self.comboBox_COM.setObjectName("comboBox_COM")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(9, 22, 171, 16))
        self.label_2.setObjectName("label_2")
        self.tabWidget.addTab(self.RS, "")
        self.TCP = QtWidgets.QWidget()
        self.TCP.setObjectName("TCP")
        self.groupBox_TCP_Server = QtWidgets.QGroupBox(self.TCP)
        self.groupBox_TCP_Server.setGeometry(QtCore.QRect(10, 10, 601, 80))
        self.groupBox_TCP_Server.setObjectName("groupBox_TCP_Server")
        self.label_port_TCP_server = QtWidgets.QLabel(self.groupBox_TCP_Server)
        self.label_port_TCP_server.setGeometry(QtCore.QRect(9, 20, 61, 16))
        self.label_port_TCP_server.setObjectName("label_port_TCP_server")
        self.pushButton_open_TCP_Server = QtWidgets.QPushButton(self.groupBox_TCP_Server)
        self.pushButton_open_TCP_Server.setGeometry(QtCore.QRect(255, 40, 171, 23))
        self.pushButton_open_TCP_Server.setObjectName("pushButton_open_TCP_Server")
        self.pushButton_close_TCP_Server = QtWidgets.QPushButton(self.groupBox_TCP_Server)
        self.pushButton_close_TCP_Server.setEnabled(False)
        self.pushButton_close_TCP_Server.setGeometry(QtCore.QRect(430, 40, 161, 23))
        self.pushButton_close_TCP_Server.setObjectName("pushButton_close_TCP_Server")
        self.lineEdit_TCP_Server_IP_port = QtWidgets.QLineEdit(self.groupBox_TCP_Server)
        self.lineEdit_TCP_Server_IP_port.setGeometry(QtCore.QRect(10, 40, 91, 22))
        self.lineEdit_TCP_Server_IP_port.setObjectName("lineEdit_TCP_Server_IP_port")
        self.comboBox_IP_Address_TCP_Server = QtWidgets.QComboBox(self.groupBox_TCP_Server)
        self.comboBox_IP_Address_TCP_Server.setGeometry(QtCore.QRect(110, 40, 141, 22))
        self.comboBox_IP_Address_TCP_Server.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.comboBox_IP_Address_TCP_Server.setObjectName("comboBox_IP_Address_TCP_Server")
        self.label_7 = QtWidgets.QLabel(self.groupBox_TCP_Server)
        self.label_7.setGeometry(QtCore.QRect(110, 20, 91, 16))
        self.label_7.setObjectName("label_7")
        self.groupBox_TCP_Client = QtWidgets.QGroupBox(self.TCP)
        self.groupBox_TCP_Client.setEnabled(True)
        self.groupBox_TCP_Client.setGeometry(QtCore.QRect(10, 90, 461, 80))
        self.groupBox_TCP_Client.setObjectName("groupBox_TCP_Client")
        self.label_port_TCP_server_2 = QtWidgets.QLabel(self.groupBox_TCP_Client)
        self.label_port_TCP_server_2.setGeometry(QtCore.QRect(170, 20, 61, 16))
        self.label_port_TCP_server_2.setObjectName("label_port_TCP_server_2")
        self.pushButton_open_TCP_Client = QtWidgets.QPushButton(self.groupBox_TCP_Client)
        self.pushButton_open_TCP_Client.setGeometry(QtCore.QRect(280, 40, 171, 23))
        self.pushButton_open_TCP_Client.setObjectName("pushButton_open_TCP_Client")
        self.pushButton_close_TCP_Client = QtWidgets.QPushButton(self.groupBox_TCP_Client)
        self.pushButton_close_TCP_Client.setEnabled(False)
        self.pushButton_close_TCP_Client.setGeometry(QtCore.QRect(280, 13, 171, 23))
        self.pushButton_close_TCP_Client.setObjectName("pushButton_close_TCP_Client")
        self.label_port_TCP_server_3 = QtWidgets.QLabel(self.groupBox_TCP_Client)
        self.label_port_TCP_server_3.setGeometry(QtCore.QRect(10, 20, 131, 16))
        self.label_port_TCP_server_3.setObjectName("label_port_TCP_server_3")
        self.lineEdit_TCP_IP_Addr = QtWidgets.QLineEdit(self.groupBox_TCP_Client)
        self.lineEdit_TCP_IP_Addr.setGeometry(QtCore.QRect(10, 40, 151, 22))
        self.lineEdit_TCP_IP_Addr.setObjectName("lineEdit_TCP_IP_Addr")
        self.lineEdit_TCP_Client_IP_Port = QtWidgets.QLineEdit(self.groupBox_TCP_Client)
        self.lineEdit_TCP_Client_IP_Port.setGeometry(QtCore.QRect(170, 40, 91, 22))
        self.lineEdit_TCP_Client_IP_Port.setObjectName("lineEdit_TCP_Client_IP_Port")
        self.tabWidget.addTab(self.TCP, "")
        self.UDP = QtWidgets.QWidget()
        self.UDP.setObjectName("UDP")
        self.groupBox_UDP_Server = QtWidgets.QGroupBox(self.UDP)
        self.groupBox_UDP_Server.setGeometry(QtCore.QRect(10, 10, 601, 80))
        self.groupBox_UDP_Server.setObjectName("groupBox_UDP_Server")
        self.pushButton_close_UDP_Server = QtWidgets.QPushButton(self.groupBox_UDP_Server)
        self.pushButton_close_UDP_Server.setEnabled(False)
        self.pushButton_close_UDP_Server.setGeometry(QtCore.QRect(430, 40, 161, 23))
        self.pushButton_close_UDP_Server.setObjectName("pushButton_close_UDP_Server")
        self.label_4 = QtWidgets.QLabel(self.groupBox_UDP_Server)
        self.label_4.setGeometry(QtCore.QRect(9, 20, 91, 16))
        self.label_4.setObjectName("label_4")
        self.pushButton_open_UDP_Server = QtWidgets.QPushButton(self.groupBox_UDP_Server)
        self.pushButton_open_UDP_Server.setGeometry(QtCore.QRect(255, 40, 171, 23))
        self.pushButton_open_UDP_Server.setObjectName("pushButton_open_UDP_Server")
        self.lineEdit_UDP_Server_IP_port = QtWidgets.QLineEdit(self.groupBox_UDP_Server)
        self.lineEdit_UDP_Server_IP_port.setGeometry(QtCore.QRect(10, 40, 91, 22))
        self.lineEdit_UDP_Server_IP_port.setObjectName("lineEdit_UDP_Server_IP_port")
        self.comboBox_IP_Address_UDP_Server = QtWidgets.QComboBox(self.groupBox_UDP_Server)
        self.comboBox_IP_Address_UDP_Server.setGeometry(QtCore.QRect(110, 40, 141, 22))
        self.comboBox_IP_Address_UDP_Server.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.comboBox_IP_Address_UDP_Server.setObjectName("comboBox_IP_Address_UDP_Server")
        self.label_5 = QtWidgets.QLabel(self.groupBox_UDP_Server)
        self.label_5.setGeometry(QtCore.QRect(110, 20, 91, 16))
        self.label_5.setObjectName("label_5")
        self.groupBox_UDP_Server_2 = QtWidgets.QGroupBox(self.UDP)
        self.groupBox_UDP_Server_2.setGeometry(QtCore.QRect(10, 90, 461, 80))
        self.groupBox_UDP_Server_2.setObjectName("groupBox_UDP_Server_2")
        self.pushButton_close_UDP_Client = QtWidgets.QPushButton(self.groupBox_UDP_Server_2)
        self.pushButton_close_UDP_Client.setEnabled(False)
        self.pushButton_close_UDP_Client.setGeometry(QtCore.QRect(280, 13, 171, 23))
        self.pushButton_close_UDP_Client.setObjectName("pushButton_close_UDP_Client")
        self.label_6 = QtWidgets.QLabel(self.groupBox_UDP_Server_2)
        self.label_6.setGeometry(QtCore.QRect(170, 20, 71, 16))
        self.label_6.setObjectName("label_6")
        self.pushButton_open_UDP_Client = QtWidgets.QPushButton(self.groupBox_UDP_Server_2)
        self.pushButton_open_UDP_Client.setGeometry(QtCore.QRect(280, 40, 171, 23))
        self.pushButton_open_UDP_Client.setObjectName("pushButton_open_UDP_Client")
        self.lineEdit_UDP_Client_IP_Port = QtWidgets.QLineEdit(self.groupBox_UDP_Server_2)
        self.lineEdit_UDP_Client_IP_Port.setGeometry(QtCore.QRect(171, 40, 91, 22))
        self.lineEdit_UDP_Client_IP_Port.setObjectName("lineEdit_UDP_Client_IP_Port")
        self.label_port_TCP_server_4 = QtWidgets.QLabel(self.groupBox_UDP_Server_2)
        self.label_port_TCP_server_4.setGeometry(QtCore.QRect(10, 20, 131, 16))
        self.label_port_TCP_server_4.setObjectName("label_port_TCP_server_4")
        self.lineEdit_UDP_IP_Addr = QtWidgets.QLineEdit(self.groupBox_UDP_Server_2)
        self.lineEdit_UDP_IP_Addr.setGeometry(QtCore.QRect(10, 40, 151, 22))
        self.lineEdit_UDP_IP_Addr.setObjectName("lineEdit_UDP_IP_Addr")
        self.tabWidget.addTab(self.UDP, "")
        self.checkBoxCiclicSend = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxCiclicSend.setGeometry(QtCore.QRect(400, 337, 171, 20))
        self.checkBoxCiclicSend.setObjectName("checkBoxCiclicSend")
        self.checkBoxXlsSave = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxXlsSave.setGeometry(QtCore.QRect(400, 316, 221, 20))
        self.checkBoxXlsSave.setChecked(True)
        self.checkBoxXlsSave.setObjectName("checkBoxXlsSave")
        self.pushButtonClearText = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonClearText.setEnabled(True)
        self.pushButtonClearText.setGeometry(QtCore.QRect(400, 270, 201, 23))
        self.pushButtonClearText.setStyleSheet("")
        self.pushButtonClearText.setObjectName("pushButtonClearText")
        self.label_Rx_Data = QtWidgets.QLabel(self.centralwidget)
        self.label_Rx_Data.setGeometry(QtCore.QRect(14, 250, 381, 16))
        self.label_Rx_Data.setObjectName("label_Rx_Data")
        self.checkBoxShowRxData = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxShowRxData.setGeometry(QtCore.QRect(400, 295, 221, 20))
        self.checkBoxShowRxData.setChecked(True)
        self.checkBoxShowRxData.setObjectName("checkBoxShowRxData")
        self.pushButton_Send_One_Pack = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Send_One_Pack.setEnabled(False)
        self.pushButton_Send_One_Pack.setGeometry(QtCore.QRect(400, 357, 201, 23))
        self.pushButton_Send_One_Pack.setStyleSheet("")
        self.pushButton_Send_One_Pack.setObjectName("pushButton_Send_One_Pack")
        ETH_Tester_Main.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ETH_Tester_Main)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 635, 26))
        self.menubar.setObjectName("menubar")
        ETH_Tester_Main.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ETH_Tester_Main)
        self.statusbar.setObjectName("statusbar")
        ETH_Tester_Main.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(ETH_Tester_Main)
        self.action.setObjectName("action")

        self.retranslateUi(ETH_Tester_Main)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ETH_Tester_Main)

    def retranslateUi(self, ETH_Tester_Main):
        _translate = QtCore.QCoreApplication.translate
        ETH_Tester_Main.setWindowTitle(_translate("ETH_Tester_Main", "Тетировщик ETH/RS"))
        self.pushButton_Choice_File.setText(_translate("ETH_Tester_Main", "Выбрать файл"))
        self.label_File_Name.setText(_translate("ETH_Tester_Main", "Файл:"))
        self.pushButton_Send.setText(_translate("ETH_Tester_Main", "Отправить данные"))
        self.groupBox.setTitle(_translate("ETH_Tester_Main", "Параметры RS/USB"))
        self.pushButton_close_COM.setText(_translate("ETH_Tester_Main", "Закрыть порт"))
        self.pushButton_open_COM.setText(_translate("ETH_Tester_Main", "Открыть порт"))
        self.label_2.setText(_translate("ETH_Tester_Main", "Выбор RS/USB порта"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.RS), _translate("ETH_Tester_Main", "RS/USB"))
        self.groupBox_TCP_Server.setTitle(_translate("ETH_Tester_Main", "Сервер TCP"))
        self.label_port_TCP_server.setText(_translate("ETH_Tester_Main", "Порт"))
        self.pushButton_open_TCP_Server.setText(_translate("ETH_Tester_Main", "Запуск TCP сервера"))
        self.pushButton_close_TCP_Server.setText(_translate("ETH_Tester_Main", "Остановка TCP сервера"))
        self.label_7.setText(_translate("ETH_Tester_Main", "Адрес"))
        self.groupBox_TCP_Client.setTitle(_translate("ETH_Tester_Main", "Клиент TCP"))
        self.label_port_TCP_server_2.setText(_translate("ETH_Tester_Main", "Порт"))
        self.pushButton_open_TCP_Client.setText(_translate("ETH_Tester_Main", "Подключиться к серверу"))
        self.pushButton_close_TCP_Client.setText(_translate("ETH_Tester_Main", "Разрыв соединения"))
        self.label_port_TCP_server_3.setText(_translate("ETH_Tester_Main", "IP адрес сервера"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TCP), _translate("ETH_Tester_Main", "TCP"))
        self.groupBox_UDP_Server.setTitle(_translate("ETH_Tester_Main", "Сервер UDP"))
        self.pushButton_close_UDP_Server.setText(_translate("ETH_Tester_Main", "Остановка UDP сервера"))
        self.label_4.setText(_translate("ETH_Tester_Main", "Порт"))
        self.pushButton_open_UDP_Server.setText(_translate("ETH_Tester_Main", "Запуск UDP сервера"))
        self.label_5.setText(_translate("ETH_Tester_Main", "Адрес"))
        self.groupBox_UDP_Server_2.setTitle(_translate("ETH_Tester_Main", "Клиент UDP"))
        self.pushButton_close_UDP_Client.setText(_translate("ETH_Tester_Main", "Разрыв соединения"))
        self.label_6.setText(_translate("ETH_Tester_Main", "Порт"))
        self.pushButton_open_UDP_Client.setText(_translate("ETH_Tester_Main", "Подключиться к серверу"))
        self.label_port_TCP_server_4.setText(_translate("ETH_Tester_Main", "IP адрес сервера"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.UDP), _translate("ETH_Tester_Main", "UDP"))
        self.checkBoxCiclicSend.setText(_translate("ETH_Tester_Main", "Циклическая отправка"))
        self.checkBoxXlsSave.setText(_translate("ETH_Tester_Main", "Запись принятых данных в xls"))
        self.pushButtonClearText.setText(_translate("ETH_Tester_Main", "Очистить принятые данные"))
        self.label_Rx_Data.setText(_translate("ETH_Tester_Main", "Принятые данные"))
        self.checkBoxShowRxData.setText(_translate("ETH_Tester_Main", "Отображать принятые данные"))
        self.pushButton_Send_One_Pack.setText(_translate("ETH_Tester_Main", "Отправить один пакет"))
        self.action.setText(_translate("ETH_Tester_Main", "Закрыть"))
