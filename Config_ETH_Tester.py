#coding: utf8

#class Config_Serial_Qt():
BAUDRATES = ['1200', '9600', '19200', '38400', '57600', '115200','230400','460800','921600']    #возможные значения скоростей для RS-232
RESET_TIME = [str(x) for x in range(1000, 4001, 100)]    #возможные задержки для времени перезагрузки
ERASE_TIME = [str(x) for x in range(5000, 50001, 5000)]    #возможные задержки для времени очистки памяти
READ_BYTES = 100
OK_ANSWER = bytearray('OK'.encode('latin-1')) #OK
ERR_ANSWER = bytearray('Err'.encode('latin-1')) #Err
MAX_WAIT_BYTES = 200    #максимальное количество байт в буфере порта на прием
NUMBER_SCAN_PORTS = 30   #количество портов для сканирования 10
SET = 1
RESET = 0
MAX_NUMBER_CLEAR_RX = 100
SETTINGS_FILENAME = 'settings.ini'
CNT_POSITION = '9'
LOG_FILENAME = 'log.txt'
TX_DATA_PAGE = 'TX_Data'
TIMER = 10
LOG = 'False'
RS_START = bytearray([0x55, 0xAA])  # стартовая последовательность для RS

XLS_DATA = {
            "DELAY": 0,
            "CNT": 1,
            "DATA": 2,
            "FORMAT": 3,
            "REPEAT": 4,
            "CRC": 5,
            }

