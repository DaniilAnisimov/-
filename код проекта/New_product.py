import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from new_product_ui import Ui_Form as Ui_main
from product_add_dialog import Ui_Dialog


class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):       # Создан для запрета на редактирование таблицы
        return


class NewProduct(QWidget, Ui_main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.warehouse_list = {}    # словари с элементами
        self.works_list = {}
        self.tools_list = {}
        self.flag_photo = True
        self.fname = "pictures/no_img.png"
        self.con = sqlite3.connect("database/production.db")
        self.cur = self.con.cursor()
        self.sum = 0
        self.initUI()

    def initUI(self):
        self.pb_add_photo.clicked.connect(self.add_photo)
        self.pb_add_wh.clicked.connect(self.add_elem)
        self.pb_add_w.clicked.connect(self.add_elem)
        self.pb_add_t.clicked.connect(self.add_elem)
        self.pb_delete_wh.clicked.connect(self.delete_elem)
        self.pb_delete_w.clicked.connect(self.delete_elem)
        self.pb_delete_t.clicked.connect(self.delete_elem)
        self.pb_save.clicked.connect(self.save)

    def load_table(self):
        self.sum = 0
        if len(self.warehouse_list):
            n = tuple([i for i in self.warehouse_list])
            if len(self.warehouse_list) == 1:
                result = self.cur.execute(f"""SELECT * FROM warehouse WHERE id = {n[0]}""").fetchall()
            else:
                result = self.cur.execute(f"""SELECT * FROM warehouse WHERE id in {n}""").fetchall()
            for i in range(len(result)):
                result[i] = list(result[i])
                result[i][3] = self.warehouse_list[result[i][0]]
            title_list = [i[1] for i in self.cur.execute("pragma table_info(warehouse)").fetchall()]
            title_list += ["Итого:"]
            # Заполняем tableWidget
            header = self.tw_wh.horizontalHeader()
            self.tw_wh.setColumnCount(len(title_list))
            self.tw_wh.setHorizontalHeaderLabels(title_list)
            self.tw_wh.setRowCount(0)
            delegate = ReadOnlyDelegate(self.tw_wh)
            for i, elem in enumerate(result):
                self.tw_wh.setRowCount(i + 1)
                # Используем класс delegate (10) для запрета на редактирования столбца i
                self.tw_wh.setItemDelegateForRow(i, delegate)
                for j, elem1 in enumerate(elem):
                    if j == len(elem) - 1:
                        self.tw_wh.setItem(i, j + 1, QTableWidgetItem(str(elem[-3] * elem[-2])))
                        self.sum += elem[-3] * elem[-2]
                    self.tw_wh.setItem(i, j, QTableWidgetItem(str(elem1)))
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        else:
            self.tw_wh.setRowCount(0)
        if len(self.works_list):
            n = tuple([i for i in self.works_list])
            if len(self.works_list) == 1:
                result = self.cur.execute(f"""SELECT * FROM works WHERE id = {n[0]}""").fetchall()
            else:
                result = self.cur.execute(f"""SELECT * FROM works WHERE id in {n}""").fetchall()
            for i in range(len(result)):
                result[i] = list(result[i])
                result[i].append(self.works_list[result[i][0]])
            title_list = [i[1] for i in self.cur.execute("pragma table_info(works)").fetchall()]
            title_list += ["Кол-во работ:", "Итого:"]
            # Заполняем tableWidget
            header = self.tw_w.horizontalHeader()
            self.tw_w.setColumnCount(len(title_list))
            self.tw_w.setHorizontalHeaderLabels(title_list)
            self.tw_w.setRowCount(0)
            delegate = ReadOnlyDelegate(self.tw_w)
            for i, elem in enumerate(result):
                self.tw_w.setRowCount(i + 1)
                # Используем класс delegate (10) для запрета на редактирования столбца i
                self.tw_w.setItemDelegateForRow(i, delegate)
                for j, elem1 in enumerate(elem):
                    if j == len(elem) - 1:
                        self.tw_w.setItem(i, j + 1, QTableWidgetItem(str(elem[-2] * elem[-1])))
                        self.sum += elem[-2] * elem[-1]
                    self.tw_w.setItem(i, j, QTableWidgetItem(str(elem1)))
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        else:
            self.tw_w.setRowCount(0)
        if len(self.tools_list):
            n = tuple([i for i in self.tools_list])
            if len(self.tools_list) == 1:
                result = self.cur.execute(f"""SELECT * FROM tools WHERE id = {n[0]}""").fetchall()
            else:
                result = self.cur.execute(f"""SELECT * FROM tools WHERE id in {n}""").fetchall()
            for i in range(len(result)):
                result[i] = list(result[i])
                result[i].append(self.tools_list[result[i][0]])
            title_list = [i[1] for i in self.cur.execute("pragma table_info(tools)").fetchall()]
            title_list += ["Кол-во работ:", "Итого:"]
            # Заполняем tableWidget
            header = self.tw_t.horizontalHeader()
            self.tw_t.setColumnCount(len(title_list))
            self.tw_t.setHorizontalHeaderLabels(title_list)
            self.tw_t.setRowCount(0)
            delegate = ReadOnlyDelegate(self.tw_t)
            for i, elem in enumerate(result):
                self.tw_t.setRowCount(i + 1)
                # Используем класс delegate (10) для запрета на редактирования столбца i
                self.tw_t.setItemDelegateForRow(i, delegate)
                for j, elem1 in enumerate(elem):
                    if j == len(elem) - 1:
                        self.tw_t.setItem(i, j + 1, QTableWidgetItem(str(elem[5] * elem[-1])))
                        self.sum += elem[5] * elem[-1]
                    self.tw_t.setItem(i, j, QTableWidgetItem(str(elem1)))
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            for i in range(2, 13):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        else:
            self.tw_t.setRowCount(0)
        # Подсчитываем себестоимость
        self.le_cost_price.setText(str(self.sum))
        self.le_total.setText(str(self.sum))

    def add_photo(self):         # Можно добавить новое фото, иначе будет стандартное
        photo = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '', "Изображения (*.png *.jpg)")[0]
        if photo:
            self.fname = photo
            if self.flag_photo:
                self.pb_add_photo.setText("Изменить фотографию")
                self.flag_photo = False

    def add_elem(self):
        # Запускаем диалоговое окно для добавления новых элементов
        button_number = self.sender().text().count(" ")
        x = AddDialog(button_number, self.con, self.cur)
        x.show()
        # Отключаем основное окно до окончания работы диалогового окна
        self.setEnabled(False)
        x.exec()
        self.setEnabled(True)
        n = x.answer
        if n:
            if n[0] == "warehouse":
                if n[1] in self.warehouse_list:
                    self.warehouse_list[n[1]] += n[2]
                else:
                    self.warehouse_list[n[1]] = n[2]
            elif n[0] == "works":
                if n[1] in self.works_list:
                    self.works_list[n[1]] += n[2]
                else:
                    self.works_list[n[1]] = n[2]
            else:
                if n[1] in self.tools_list:
                    self.tools_list[n[1]] += n[2]
                else:
                    self.tools_list[n[1]] = n[2]
            self.load_table()

    def delete_elem(self):
        n = {1: self.tw_wh, 2: self.tw_w, 3: self.tw_t}
        button_number = self.sender().text().count(" ")
        rows = list(set([i.row() for i in n[button_number].selectedItems()]))
        if not rows:
            return 0
        ids = [n[button_number].item(i, 0).text() for i in rows]
        # Спрашиваем у пользователя подтверждение на удаление элементов
        valid = QMessageBox.question(self, '', "Действительно удалить элементы с id " + ",".join(ids),
                                     QMessageBox.Yes, QMessageBox.No)
        # Если пользователь ответил утвердительно, удаляем элементы.
        m = {1: (self.warehouse_list, 6), 2: (self.works_list, 5), 3: (self.tools_list, 5)}
        if valid == QMessageBox.Yes:
            for i in range(len(ids)):
                self.sum -= float(n[button_number].item(rows[i], m[button_number][1]).text())
                del m[button_number][0][int(ids[i])]
            self.load_table()

    def save(self):      # Сохраняем все полученные данные от пользователя в бд
        try:
            name = self.le_name.text()
            file_path = self.fname
            size = self.le_size.text()
            cost_price = float(self.le_cost_price.text())
            total = float(self.le_total.text())
            if name and size and cost_price and total and\
                    self.warehouse_list and self.works_list and self.tools_list:
                self.cur.execute("INSERT INTO product(Название, Габариты, Фото,"
                                 "'Себестоимость р', 'Цена р') VALUES(?, ?, ?, ?, ?)",
                                 (name, size, file_path, cost_price, total))
                self.con.commit()
                result = self.cur.execute("SELECT id FROM product WHERE Название = ?", (name,)).fetchall()
                for i in self.warehouse_list:
                    self.cur.execute("INSERT INTO warehouse_used('Элемент склада', Продукт, 'Кол-во') VALUES(?, ?, ?)",
                                     [i, result[0][0], self.warehouse_list[i]])
                    self.con.commit()
                for i in self.works_list:
                    self.cur.execute("INSERT INTO works_used(Работа, Продукт, 'Кол-во') VALUES(?, ?, ?)",
                                     (i, result[0][0], self.works_list[i]))
                    self.con.commit()
                for i in self.tools_list:
                    self.cur.execute("INSERT INTO tools_used(Инструмент, Продукт, 'Кол-во') VALUES(?, ?, ?)",
                                     (i, result[0][0], self.tools_list[i]))
                    self.con.commit()
                self.le_error.setText("Данные успешно сохранены")
            else:
                self.le_error.setText("Некоторые поля не заполнены")
        except sqlite3.IntegrityError as f:
            print(f)
            self.le_error.setText("Название продукта занято")


class AddDialog(QDialog, Ui_Dialog):
    def __init__(self, type, con, cur):
        super(AddDialog, self).__init__()
        self.setupUi(self)
        self.list_of_tables = {1: "warehouse", 2: "works", 3: "tools"}
        self.type = self.list_of_tables[type]
        self.answer = []
        self.con = con
        self.cur = cur
        self.initUI()

    def initUI(self):
        self.pb_end.clicked.connect(self.end)
        self.pb_add.clicked.connect(self.add)
        self.lineEdit.textChanged.connect(self.load_table)
        self.load_table()

    def load_table(self):
        result = self.cur.execute(f"""SELECT * FROM {self.type} WHERE Название like ?""",
                                  (self.lineEdit.text() + '%', )).fetchall()
        title_list = [i[1] for i in self.cur.execute(f"pragma table_info({self.type})").fetchall()]
        self.tableWidget.setColumnCount(len(title_list))
        self.tableWidget.setHorizontalHeaderLabels(title_list)
        self.tableWidget.setRowCount(0)
        header = self.tableWidget.horizontalHeader()
        delegate = ReadOnlyDelegate(self.tableWidget)
        for i, elem in enumerate(result):
            self.tableWidget.setRowCount(i + 1)
            # Используем класс delegate (10) для запрета на редактирования столбца i
            self.tableWidget.setItemDelegateForRow(i, delegate)
            for j, elem1 in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem1)))
        for i in range(self.tableWidget.columnCount()):   # Задаём свойства расширения для
            # каждого столбца каждой таблицы
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

    def add(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        if len(rows) == 1:
            id_el = int(self.tableWidget.item(rows[0], 0).text())
            k = int(self.spinBox.text())
            if k:
                self.answer = [self.type, id_el, k]
                self.close()
            else:
                self.le_error.setText("Кол-во должно быть > 0")
        elif len(rows) > 1:
            self.le_error.setText("Можно выбирать только 1 элемент")
        else:
            self.le_error.setText("Ни один элемент не выбран")

    def end(self):
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NewProduct()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
