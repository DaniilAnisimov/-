import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import xlsxwriter
from basket_ui import Ui_Form


class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):       # Создан для запрета на редактирование таблицы
        return


class ShoppingCart(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("database/production.db")
        self.cur = self.con.cursor()
        self.initUI()

    def initUI(self):
        # Подключаем сигналы от кнопок
        self.pb_update.clicked.connect(self.load_table)
        self.pb_ex_1.clicked.connect(self.print_shopping_list)
        self.pb_ex_2.clicked.connect(self.print_shopping_list)
        self.load_table()

    def load_table(self):
        table_data = []       # Список с данными таблиц
        list_of_data = []
        # Сначала загружаем список покупок и добавляем его в список n
        shoppinglist = list(self.cur.execute(f"""SELECT * FROM shopping_list_warehouse""").fetchall())
        for i in shoppinglist:
            warehouse = list(self.cur.execute(f"""SELECT * FROM warehouse WHERE id = {i[0]}""").fetchall()[0])
            warehouse[3] = i[1]
            list_of_data.append(warehouse)
        table_data.append([self.tw_warehouse, list_of_data,
                           [i[1] for i in self.cur.execute("pragma table_info(warehouse)").fetchall()]])

        # Загружаем данные израсходовавших свой ресурс инструментов
        list_of_data = []
        shoppinglist = list(self.cur.execute(f"""SELECT * FROM shopping_list_tools""").fetchall())
        for i in shoppinglist:
            tools = list(self.cur.execute(f"""SELECT id, "Название", 
                "Мощность Вт", "Цена" FROM tools WHERE id = {i[0]}""").fetchall()[0])
            tools += [i[1]]
            list_of_data.append(tools)
        table_data.append([self.tw_tools, list_of_data, ["id", "Название", "Мощность Вт", "Цена", "Кол-во"]])

        for table in table_data:
            # Заполняем обе таблицы данными из n
            tablewidget = table[0]
            header = tablewidget.horizontalHeader()
            result = table[1]
            title_list = table[2]
            tablewidget.setColumnCount(len(title_list))
            tablewidget.setHorizontalHeaderLabels(title_list)
            tablewidget.setRowCount(0)
            delegate = ReadOnlyDelegate(tablewidget)
            for i, elem in enumerate(result):
                tablewidget.setRowCount(i + 1)
                tablewidget.setItemDelegateForRow(i, delegate)
                for j, elem1 in enumerate(elem):
                    tablewidget.setItem(i, j, QTableWidgetItem(str(elem1)))
            tablewidget.resizeColumnsToContents()
            # Задаём свойства расширения для каждого столбца каждой таблицы
            if len(table[2]) == 6:
                for i in range(6):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            else:
                for i in range(5):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

    def print_shopping_list(self):   # Функция переносящая таблицы в Excel
        button = self.sender()
        if button.text()[-1] == " ":      # Распознаём для какой таблицы нам нужно создать Excel копию
            # Примечание: на одной из кнопок есть лишний пробел
            data = [["id", "Название", "Мощность Вт", "Цена", "Кол-во"]]
            for i in range(self.tw_tools.rowCount()):
                line = []
                for j in range(self.tw_tools.columnCount()):
                    line.append(self.tw_tools.item(i, j).text())
                data.append(line)
            # Создаём и заполняем Excel файл
            workbook = xlsxwriter.Workbook('documents/Инструменты на замену.xlsx')
            worksheet = workbook.add_worksheet()
            for row, elem in enumerate(data):
                for col, elem1 in enumerate(elem):
                    worksheet.write(row, col, elem1)
            workbook.close()
        else:
            data = [[i[1] for i in self.cur.execute("pragma table_info(warehouse)")]]
            for i in range(self.tw_warehouse.rowCount()):
                line = []
                for j in range(self.tw_warehouse.columnCount()):
                    line.append(self.tw_warehouse.item(i, j).text())
                data.append(line)
            # Создаём и заполняем Excel файл
            workbook = xlsxwriter.Workbook('documents/Список покупок.xlsx')
            worksheet = workbook.add_worksheet()
            for row, elem in enumerate(data):
                for col, elem1 in enumerate(elem):
                    worksheet.write(row, col, elem1)
            workbook.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ShoppingCart()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
