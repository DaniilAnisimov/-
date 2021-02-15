import sys
import sqlite3
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from catalog_ui import Ui_Form


class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):       # Создан для запрета на редактирование таблицы
        return


class Catalog(QWidget, Ui_Form):          # Класс Склада
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("database/production.db")
        self.cur = self.con.cursor()
        self.initUI()

    def initUI(self):
        self.lineEdit.textChanged.connect(self.load_table)
        self.pb_image.clicked.connect(self.show_image)
        self.load_table()

    def load_table(self):
        header = self.tableWidget.horizontalHeader()
        result = self.cur.execute(f"""SELECT * FROM product WHERE Название like ?""",
                                  (self.lineEdit.text() + "%",)).fetchall()
        new_result = []
        for i in result:
            n = [j for j in i]
            new_result.append(n[:3] + [n[-1]])
        result = new_result
        # Получаем заголовки
        title_list = [i[1] for i in self.cur.execute(f"pragma table_info(product)").fetchall()]
        title_list = title_list[:3] + title_list[5:]
        # Заполняем таблицу
        self.tableWidget.setColumnCount(len(title_list))
        self.tableWidget.setHorizontalHeaderLabels(title_list)
        self.tableWidget.setRowCount(0)
        delegate = ReadOnlyDelegate(self.tableWidget)
        for i, elem in enumerate(result):
            self.tableWidget.setRowCount(i + 1)
            # Используем класс delegate (10) для запрета на редактирования столбца i
            self.tableWidget.setItemDelegateForRow(i, delegate)
            for j, elem1 in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem1)))
        for i in range(4):   # Задаём свойства расширения для каждого столбца каждой таблицы
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

    def show_image(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        # Получаем список выделенных строк
        if len(rows) != 1:  # Строка обязательно должна быть одна
            return 0
        way = self.cur.execute(f"""SELECT Фото FROM product WHERE
            id = {int(self.tableWidget.item(rows[0], 0).text())}""").fetchall()[0][0]
        x = App(way)
        x.show()
        # Отключаем основное окно до окончания работы диалогового окна
        self.setEnabled(False)
        x.exec()
        self.setEnabled(True)


class App(QDialog):
    def __init__(self, way):
        super().__init__()
        self.way = way
        self.l_picture = QLabel()
        self.main_layout = QHBoxLayout(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('картинка')
        self.main_layout.addWidget(self.l_picture)
        pixmap = QPixmap(self.way)
        pixmap = pixmap.scaled(640, 480, QtCore.Qt.IgnoreAspectRatio)
        self.l_picture.setPixmap(pixmap)
        self.setGeometry(100, 100, 640, 480)
        self.setLayout(self.main_layout)
        self.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Catalog()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())


