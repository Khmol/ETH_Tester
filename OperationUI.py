from Config_ETH_Tester import SET

# *********************************************************************
def ChangeRsButtonsIdle(ui, xls_filename):
    '''
    # активация кнопок после выбора порта и скорости
    :param ui:
    :param xls_filename:
    :return:
    '''
    # изменяем назначение кнопки прошить
    ui.pushButton_Send.setText("Отправить данные")
    ui.pushButton_Choice_File.setEnabled(SET)      #активируем кнопку выбор файла
    ui.pushButton_open_COM.setDisabled(SET)        #де-активируем кнопку открытие порта
    ui.pushButton_close_COM.setEnabled(SET)        #активируем кнопку закрытие порта
    ui.comboBox_COM.setDisabled(SET)               #де-активируем выбор порта
    ui.comboBox_Baudrate.setDisabled(SET)          #де-активируем выбор скорости
    ui.checkBoxXlsSave.setEnabled(SET)
    if xls_filename and xls_filename[0] != '':
        ui.pushButton_Send.setEnabled(SET)
        ui.pushButton_Send_One_Pack.setEnabled(SET)

#*********************************************************************
def ChangeActiveButtonsRsClose(ui):
    '''
    де-активация всех кнопок
    :param ui:
    :return:
    '''
    ui.pushButton_Choice_File.setDisabled(SET)        #де-активируем кнопку выбор файла
    ui.pushButton_open_COM.setDisabled(SET)           #де-активируем кнопку открытие порта
    ui.pushButton_close_COM.setDisabled(SET)          #де-активируем кнопку закрытие порта
    ui.comboBox_COM.setDisabled(SET)                  #де-активируем выбор порта
    ui.comboBox_Baudrate.setDisabled(SET)             #де-активируем выбор скорости
    ui.pushButton_Send.setDisabled(SET)               #де-активируем кнопку "Прошить"
    ui.pushButton_Send_One_Pack.setDisabled(SET)
    ui.checkBoxXlsSave.setDisabled(SET)

#*********************************************************************
def ChangeActiveButtonsRsSelected(ui):
    '''
    де-активация кнопок после выбора порта
    :param ui:
    :return:
    '''
    ui.pushButton_Choice_File.setEnabled(SET)        #де-активируем кнопку выбор файла
    ui.pushButton_open_COM.setEnabled(SET)            #активируем кнопку открытие порта
    ui.pushButton_close_COM.setDisabled(SET)          #де-активируем кнопку закрытие порта
    ui.comboBox_COM.setEnabled(SET)                   #активируем выбор порта
    ui.comboBox_Baudrate.setEnabled(SET)              #активируем выбор скорости
    ui.pushButton_Send.setDisabled(SET)               #де-активируем кнопку "Прошить"
    ui.pushButton_Send_One_Pack.setDisabled(SET)
    ui.checkBoxXlsSave.setEnabled(SET)

#*********************************************************************
def ChangeButtonsRsSend(ui):
    '''
    # изменить значение кнопок для передачи
    :param ui:
    :return:
    '''
    # изменяем назначение кнопки прошить
    ui.pushButton_Send.setText("Прервать отправку")
    #настраиваем видимость кнопок
    ui.pushButton_Choice_File.setDisabled(SET)   #де-активируем кнопку выбор файла
    ui.pushButton_open_COM.setDisabled(SET)      #де-активируем кнопку открытие порта
    ui.pushButton_close_COM.setDisabled(SET)     #де-активируем кнопку закрытие порта
    ui.comboBox_COM.setDisabled(SET)             #де-активируем выбор порта
    ui.comboBox_Baudrate.setDisabled(SET)        #де-активируем выбор скорости
    ui.checkBoxXlsSave.setDisabled(SET)

# *********************************************************************
def ShowFileName(xls_filename, ui):
    '''
    # отобразить имя открытого файла
    :return:
    '''
    if xls_filename != '':
        if xls_filename[0]!= '':
            ui.label_File_Name.setText("Файл: " + xls_filename[0])

# *********************************************************************
def ChangeButtonsUDPServerConnected(ui):
    '''
    активируем и деактивируем кнопки для открытого UDP сервера
    :param ui:
    :return:
    '''
    ui.pushButton_open_UDP_Server.setDisabled(SET)
    ui.pushButton_close_UDP_Server.setEnabled(SET)
    ui.lineEdit_UDP_Server_IP_port.setDisabled(SET)
    ui.comboBox_IP_Address_UDP_Server.setDisabled(SET)

# *********************************************************************
def ChangeButtonsTCPServerConnected(ui):
    '''
    активируем и деактивируем кнопки для открытого TCP сервера
    :param ui:
    :return:
    '''
    ui.pushButton_open_TCP_Server.setDisabled(SET)
    ui.pushButton_close_TCP_Server.setEnabled(SET)
    ui.lineEdit_TCP_Server_IP_port.setDisabled(SET)
    ui.comboBox_IP_Address_TCP_Server.setDisabled(SET)

# *********************************************************************
def ChangeButtonsUDPServerDisconnected(ui):
    '''
    активируем и деактивируем кнопки для закрытого UDP сервера
    :param ui:
    :return:
    '''
    ui.pushButton_open_UDP_Server.setEnabled(SET)
    ui.pushButton_close_UDP_Server.setDisabled(SET)
    ui.lineEdit_UDP_Server_IP_port.setEnabled(SET)
    ui.comboBox_IP_Address_UDP_Server.setEnabled(SET)

# *********************************************************************
def ChangeButtonsTCPServerDisconnected(ui):
    '''
    активируем и деактивируем кнопки для закрытого UDP сервера
    :param ui:
    :return:
    '''
    ui.pushButton_open_TCP_Server.setEnabled(SET)
    ui.pushButton_close_TCP_Server.setDisabled(SET)
    ui.lineEdit_TCP_Server_IP_port.setEnabled(SET)
    ui.comboBox_IP_Address_TCP_Server.setEnabled(SET)

# *********************************************************************
def ChangeButtonsUDPClientConnected(ui):
    '''
    активируем и деактивируем кнопки при подключении клиентом по UDP к серверу
    :param ui:
    :return:
    '''
    ui.pushButton_open_UDP_Client.setDisabled(SET)
    ui.pushButton_close_UDP_Client.setEnabled(SET)
    ui.lineEdit_UDP_IP_Addr.setDisabled(SET)
    ui.lineEdit_UDP_Client_IP_Port.setDisabled(SET)
    ui.pushButton_Send.setEnabled(SET)
    ui.pushButton_Send_One_Pack.setEnabled(SET)

# *********************************************************************
def ChangeButtonsTCPClientConnected(ui):
    '''
    активируем и деактивируем кнопки при подключении клиентом по TCP к серверу
    :param ui:
    :return:
    '''
    ui.pushButton_open_TCP_Client.setDisabled(SET)
    ui.pushButton_close_TCP_Client.setEnabled(SET)
    ui.lineEdit_TCP_IP_Addr.setDisabled(SET)
    ui.lineEdit_TCP_Client_IP_Port.setDisabled(SET)
    ui.pushButton_Send.setEnabled(SET)
    ui.pushButton_Send_One_Pack.setEnabled(SET)

#*********************************************************************
def ChangeButtonsUDPClientDisconnected(ui):
    '''
    активируем и деактивируем кнопки при отключении клиента по UDP от сервера
    :param ui:
    :return:
    '''
    ui.pushButton_open_UDP_Client.setEnabled(SET)
    ui.pushButton_close_UDP_Client.setDisabled(SET)
    ui.lineEdit_UDP_IP_Addr.setEnabled(SET)
    ui.lineEdit_UDP_Client_IP_Port.setEnabled(SET)
    ui.pushButton_Send.setDisabled(SET)
    ui.pushButton_Send_One_Pack.setDisabled(SET)

#*********************************************************************
def ChangeButtonsTCPClientDisconnected(ui):
    '''
    активируем и деактивируем кнопки при отключении клиента по TCP от сервера
    :param ui:
    :return:
    '''
    ui.pushButton_open_TCP_Client.setEnabled(SET)
    ui.pushButton_close_TCP_Client.setDisabled(SET)
    ui.lineEdit_TCP_IP_Addr.setEnabled(SET)
    ui.lineEdit_TCP_Client_IP_Port.setEnabled(SET)
    ui.pushButton_Send.setDisabled(SET)
    ui.pushButton_Send_One_Pack.setDisabled(SET)

# *********************************************************************
def ChangeUDPButtonsIdle(ui, xls_filename):
    '''
    # активация кнопок после выбора порта и скорости
    :param ui:
    :param xls_filename:
    :return:
    '''
    # изменяем назначение кнопки прошить
    ui.pushButton_Send.setText("Отправить данные")
    ui.pushButton_Choice_File.setEnabled(SET)      #активируем кнопку выбор файла
    ui.pushButton_close_UDP_Client.setEnabled(SET)        #де-активируем кнопку открытие порта
    ui.checkBoxXlsSave.setEnabled(SET)
    if xls_filename and xls_filename[0] != '':
        ui.pushButton_Send.setEnabled(SET)
        ui.pushButton_Send_One_Pack.setEnabled(SET)

# *********************************************************************
def ChangeTCPButtonsIdle(ui, xls_filename):
    '''
    # активация кнопок после нажатия кнопки отправить
    :param ui:
    :param xls_filename:
    :return:
    '''
    # изменяем назначение кнопки прошить
    ui.pushButton_Send.setText("Отправить данные")
    ui.pushButton_Choice_File.setEnabled(SET)      #активируем кнопку выбор файла
    ui.pushButton_close_TCP_Client.setEnabled(SET)        #де-активируем кнопку открытие порта
    ui.checkBoxXlsSave.setEnabled(SET)
    if xls_filename and xls_filename[0] != '':
        ui.pushButton_Send.setEnabled(SET)
        ui.pushButton_Send_One_Pack.setEnabled(SET)

#*********************************************************************
def ChangeButtonsUDPSend(ui):
    '''
    # изменить значение кнопок для передачи
    :param ui:
    :return:
    '''
    # изменяем назначение кнопки прошить
    ui.pushButton_Send.setText("Прервать отправку")
    #настраиваем видимость кнопок
    ui.pushButton_Choice_File.setDisabled(SET)   #де-активируем кнопку выбор файла
    ui.pushButton_close_UDP_Client.setDisabled(SET)      #де-активируем кнопку открытие порта
    ui.pushButton_open_UDP_Client.setDisabled(SET)     #де-активируем кнопку закрытие порта
    ui.checkBoxXlsSave.setDisabled(SET)

#*********************************************************************
def ChangeButtonsTCPSend(ui):
    '''
    # изменить значение кнопок для передачи
    :param ui:
    :return:
    '''
    # изменяем назначение кнопки прошить
    ui.pushButton_Send.setText("Прервать отправку")
    #настраиваем видимость кнопок
    ui.pushButton_Choice_File.setDisabled(SET)   #де-активируем кнопку выбор файла
    ui.pushButton_close_TCP_Client.setDisabled(SET)      #де-активируем кнопку открытие порта
    ui.pushButton_open_TCP_Client.setDisabled(SET)     #де-активируем кнопку закрытие порта
    ui.checkBoxXlsSave.setDisabled(SET)

#*********************************************************************
def EnableAllButtonsRS(ui):
    '''
    деактивируем все кнопки в RS
    :param ui:
    :return:
    '''
    ui.pushButton_open_COM.setEnabled(SET)
    ui.pushButton_close_COM.setDisabled(SET)

#*********************************************************************
def DisableAllButtonsRS(ui):
    '''
    деактивируем все кнопки в RS
    :param ui:
    :return:
    '''
    ui.pushButton_open_COM.setDisabled(SET)
    ui.pushButton_close_COM.setDisabled(SET)

#*********************************************************************
def DisableAllButtonsUDP(ui):
    '''
    деактивируем все кнопки в UDP
    :param ui:
    :return:
    '''
    ui.pushButton_open_UDP_Server.setDisabled(SET)
    ui.pushButton_close_UDP_Server.setDisabled(SET)
    ui.pushButton_open_UDP_Client.setDisabled(SET)
    ui.pushButton_close_UDP_Client.setDisabled(SET)

#*********************************************************************
def EnableAllButtonsUDP(ui):
    '''
    деактивируем все кнопки в UDP
    :param ui:
    :return:
    '''
    ui.pushButton_open_UDP_Server.setEnabled(SET)
    ui.pushButton_close_UDP_Server.setDisabled(SET)
    ui.pushButton_open_UDP_Client.setEnabled(SET)
    ui.pushButton_close_UDP_Client.setDisabled(SET)

#*********************************************************************
def DisableAllButtonsTCP(ui):
    '''
    деактивируем все кнопки в UDP
    :param ui:
    :return:
    '''
    ui.pushButton_open_TCP_Server.setDisabled(SET)
    ui.pushButton_close_TCP_Server.setDisabled(SET)
    ui.pushButton_open_TCP_Client.setDisabled(SET)
    ui.pushButton_close_TCP_Client.setDisabled(SET)

#*********************************************************************
def EnableAllButtonsTCP(ui):
    '''
    деактивируем все кнопки в UDP
    :param ui:
    :return:
    '''
    ui.pushButton_open_TCP_Server.setEnabled(SET)
    ui.pushButton_close_TCP_Server.setDisabled(SET)
    ui.pushButton_open_TCP_Client.setEnabled(SET)
    ui.pushButton_close_TCP_Client.setDisabled(SET)

