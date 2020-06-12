#coding: utf8

#class Config_Serial_Qt():
BAUDRATES = ['1200', '9600', '19200', '38400', '57600', '115200','230400','460800','921600']    #возможные значения скоростей для RS-232
DEFAULT_IP_ADDRESS = ['127.0.0.1']
MAX_WAIT_BYTES = 1000    #максимальное количество байт в буфере порта на прием
NUMBER_SCAN_PORTS = 30   #количество портов для сканирования 10
SET = 1
RESET = 0
CNT_POSITION = 9
MAX_NUMBER_CLEAR_RX = 100
DEFAULT_SETTINGS_FILENAME = 'settings.ini'
DEFAULT_LOG_FILENAME = 'log.txt'
DEFAULT_TXT_FILENAME = 'receive.txt'
TX_DATA_PAGE = 'TX_Data'
DEFAULT_RX_DATA = ['Hex', 'String', 'Address', 'Port']
MAX_RX_LENGTH = 20000
DEFAULT_TIMER = 10
DEFAULT_UI_TIMER = 200
LOG = False
RS_START = bytearray([0x55, 0xAA])  # стартовая последовательность для RS
DEFAULT_UDP_PORT = 7798
DEFAULT_TCP_PORT = 7700
XLS_DATA = {
            "DELAY": 0,
            "CNT": 1,
            "DATA": 2,
            "FORMAT": 3,
            "REPEAT": 4,
            "CRC": 5,
            }

