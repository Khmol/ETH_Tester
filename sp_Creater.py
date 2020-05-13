#coding: utf8
import sys, os
from UI_sp_Creater import *
from PyQt5 import QtCore, QtGui, QtWidgets
from pyexcel_xls import save_data
from pyexcel_xls import get_data

class SP_Creater(QtWidgets.QMainWindow):
    #инициализация окна
    # pyuic5 UI_sp_Creater.ui -o UI_sp_Creater.py
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        #инициализация интерфейса
        self.ui = Ui_sp_Creator()
        self.ui.setupUi(self)
        # установка начальных значений виджетов
        self.ui.spinBox_Pos.setValue(2)
        self.ui.spinBox_Name.setValue(3)
        self.ui.spinBox_Count.setValue(4)
        self.ui.lineEdit_Page_Name.setText('Перечень элементов')
        #настройка действий по кнопкам
        self.ui.pushButton_Create.clicked.connect(self.pb_Create_Header)        # формирование спецификации
        self.ui.pushButton_Choice_File.clicked.connect(self.showDialog_Open_File)   # выбрать файл


    def pb_Create_Header (self):
        '''
        обработчик нажатия кнопки "Сформировать спецификацию"
        :return:
        '''
        pos = self.ui.spinBox_Pos.value() - 1
        name = self.ui.spinBox_Name.value() - 1
        cnt = self.ui.spinBox_Count.value() - 1
        if pos == name or pos == cnt or name == cnt:
            QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Номера страниц должны быть разные', QtWidgets.QMessageBox.Ok)
        else:
            page = self.ui.lineEdit_Page_Name.text()
            self.Create_Specification(self.fileName, pos, name, cnt, page)


    def showDialog_Open_File(self):
        '''
        #*********************************************************************
        # открытие файла xls
        #*********************************************************************
        :return:
        '''
        self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Открыть файл xls", str(os.getcwd()),
                                                  "XLS файл (*.xls)")
        if self.fileName:
            self.ui.pushButton_Create.setEnabled(1)   # активируем кнопку "Сформировать спецификацию"
            self.ui.label_File_Name.setText("Файл: " + self.fileName)  # выводим название файла
        return


    def Del_Spaces(self, data):
        data_out = []
        for row in data:
            row_out = []
            for pos in row:
                if isinstance(pos, str) and pos != '':
                    while pos[-1] == ' ':
                        pos = pos[:-1]
                        if len(pos) == 0:
                            break
                row_out.append(pos)
            data_out.append(row_out)
        return data_out


    def Create_Specification(self, file_name, mark_pos = 1, name_pos = 2, cnt_pos = 3, page_name = 'Перечень элементов'):
        '''
        Создание спецификации по файлу перечня элементов
        :return:
        '''
        try:
            data_rx = get_data(file_name)
            try:
                elements_list = self.Del_Spaces(data_rx[page_name])
            except KeyError:
                QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Нет такой страницы в файле', QtWidgets.QMessageBox.Ok)
                return
            Spec = []
            scan_pos = 0
            # перебираем все строки таблицы
            for row_to_scan in elements_list:
                # проверяем длину строки на минимальную длину
                # max_pos = max([mark_pos, name_pos, cnt_pos])
                if len(row_to_scan) > name_pos:
                    Name = row_to_scan[name_pos]
                    if Name != '':
                        # просматриваем все оставшиеся строки
                        for row in elements_list[scan_pos + 1:]:
                            # находим максимальную длину строки
                            if len(row) > name_pos:
                                if row[name_pos] == Name:
                                    row_to_scan[mark_pos] += ',' + row[mark_pos]
                                    row_to_scan[cnt_pos] += row[cnt_pos]
                                    row.clear()
                        if row_to_scan:
                            Spec.append(row_to_scan)
                else:
                    if len(elements_list[scan_pos - 1]):
                        Spec.append(row_to_scan)
                scan_pos += 1
            # читаем файл заново и добавляем лист со спецификацией
            data_rx = get_data(file_name)
            data_rx.update({"Спецификация": Spec})
            save_data(file_name, data_rx)
            QtWidgets.QMessageBox.information(self, 'Информация', 'Спецификация успешно сформирована', QtWidgets.QMessageBox.Ok)
        except Exception as EXP:
            QtWidgets.QMessageBox.critical(self, 'Ошибка обработки перечня элементов', str(EXP), QtWidgets.QMessageBox.Ok)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = SP_Creater()
    myapp.show()
    sys.exit(app.exec_())
