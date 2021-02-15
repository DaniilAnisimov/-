import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from warehouse_ui import Ui_Form
from warehouse_edit_dialog import Ui_Dialog


class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):   # Класс относящийся к Warehouse (15)
    def createEditor(self, parent, option, index):       # Создан для запрета на редактирование таблицы
        return


class Warehouse(QWidget, Ui_Form):          # Класс Склада
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("database/production.db")
        self.cur = self.con.cursor()
        self.result_category = self.cur.execute("""SELECT Категория FROM categories""").fetchall()
        self.categories = []
        self.initUI()

    def initUI(self):
        # Подключаем бд warehouse
        # Подключаем сигналы от изменения значения comboBox, текста lineEdit соответственно
        self.comboBox.activated.connect(self.load_table)
        self.lineEdit.textChanged.connect(self.load_table)
        # Подключаем событие для кнопки pb_replenish (pb от сокращения PushButon), pb_edit, pb_add соответственно
        self.pb_replenish.clicked.connect(self.replenish)
        self.pb_edit.clicked.connect(self.edit_elem)
        self.pb_add.clicked.connect(self.add_elem)
        self.pb_update.clicked.connect(self.load_table)
        self.load_table()

    def load_table(self):
        # Ищем категории товаров
        self.result_category = self.cur.execute("""SELECT Категория FROM categories""").fetchall()
        result_category_list = [str(i[0]) for i in self.result_category]
        if not self.categories or result_category_list != self.categories:
            # Добавляем в comboBox все категории товаров
            self.comboBox.clear()
            self.comboBox.addItem("Всё")
            for i in self.result_category:
                self.comboBox.addItem(str(i[0]))
            self.categories = result_category_list
        # Создаём запрос для сортировки Warehouse (бд), начало Названия товара должно начинаться с self.lineEdit.text()
        request = """SELECT * FROM warehouse WHERE Название like ?"""
        # Создаём список для подстановки в запрос
        list_of_requests = [self.lineEdit.text() + "%"]
        if self.comboBox.currentText() != "Всё":
            # Добавляем новое условие для запроса
            request += " AND категория = (SELECT id FROM categories WHERE Категория = ?)"
            list_of_requests += [self.comboBox.currentText()]
        # Производим запрос
        result = self.cur.execute(request, list_of_requests).fetchall()
        # Получаем список заголовков таблицы warehouselist
        title_list = [i[1] for i in self.cur.execute("pragma table_info(warehouse)").fetchall()]
        title_list += ["Итого:"]
        # Заполняем tableWidget
        header = self.tableWidget.horizontalHeader()
        self.tableWidget.setColumnCount(len(title_list))
        self.tableWidget.setHorizontalHeaderLabels(title_list)
        self.tableWidget.setRowCount(0)
        delegate = ReadOnlyDelegate(self.tableWidget)
        for i, elem in enumerate(result):
            self.tableWidget.setRowCount(i + 1)
            # Используем класс delegate (10) для запрета на редактирования столбца i
            self.tableWidget.setItemDelegateForRow(i, delegate)
            for j, elem1 in enumerate(elem):
                if j == len(elem) - 1:
                    self.tableWidget.setItem(i, j + 1, QTableWidgetItem(str(elem[-3] * elem[-2])))
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem1)))
        # Задаём свойства расширения для каждого столбца
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)

    def replenish(self):     # функция для пополнения запасов
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        if len(rows) != 1:   # Строка обязательно должна быть одна
            return 0
        # вызываем диалоговое окно
        replenishment, ok_pressed = QInputDialog.getInt(self, "Введите кол-во", "Кол-во:", 1, 1, 100, 1)
        if ok_pressed:
            id_warehouse = int(self.tableWidget.item(rows[0], 0).text())
            result = self.cur.execute(f"""SELECT "кол-во" FROM "shopping_list_warehouse"
                WHERE "id продукта" = {id_warehouse}""").fetchall()
            # Кол-во на складе
            quantity_in_warehouse = self.cur.execute(f"""SELECT "кол-во" FROM
                warehouse WHERE "id" = {id_warehouse}""").fetchall()[0][0]
            if result:
                quantity_in_shopping = result[0][0]      # Кол-во в корзине
                # Сначала удаляем элементы с корзины а только потом добавляем в склад
                if replenishment > quantity_in_shopping:
                    self.cur.execute(f"""DELETE FROM "shopping_list_warehouse"
                        WHERE "id продукта" = {id_warehouse}""")
                    self.cur.execute("""UPDATE warehouse SET "кол-во" = ? WHERE id = ?""",
                                     (quantity_in_warehouse + replenishment - quantity_in_shopping, id_warehouse))
                    self.con.commit()
                elif replenishment == quantity_in_shopping:
                    self.cur.execute(f"""DELETE FROM "shopping_list_warehouse" WHERE "id продукта" = {id_warehouse}""")
                    self.con.commit()
                else:
                    self.cur.execute("""UPDATE "shopping_list_warehouse" SET "кол-во" = ? WHERE "id продукта" = ?""",
                                     (quantity_in_shopping - replenishment, id_warehouse))
                    self.con.commit()
            else:
                self.cur.execute("""UPDATE warehouse SET "кол-во" = ? WHERE id = ?""",
                                 (quantity_in_warehouse + replenishment, id_warehouse))
                self.con.commit()
            self.load_table()

    def add_elem(self):
        # Класс вызывает диалоговое окно и передаёт нужные параметры для работы.
        dialogue = Editdialog("add", self.con, self.cur, self.result_category)
        dialogue.show()
        # Отключаем основное окно до окончания работы диалогового окна
        self.setEnabled(False)
        dialogue.exec()
        self.setEnabled(True)
        # После изменений обновляем таблицу
        self.load_table()

    def edit_elem(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        # Получаем список выделенных строк
        if len(rows) != 1:  # Строка обязательно должна быть одна
            return 0
        # Создаём и заполняем список с данными о выделенной строке
        select_row = []
        for i in range(6):
            select_row.append(self.tableWidget.item(rows[0], i).text())
        # Класс вызывает диалоговое окно и передаёт нужные параметры для работы.
        dialogue = Editdialog("edit", self.con, self.cur, self.result_category, select_row)
        dialogue.show()
        # Отключаем основное окно до окончания работы диалогового окна
        self.setEnabled(False)
        dialogue.exec()
        self.setEnabled(True)
        # После изменений обновляем таблицу
        self.load_table()


class Editdialog(QDialog, Ui_Dialog):         # Диалог используемый для добавления и редактирования элементов склада
    def __init__(self, type_dialog, *args):
        super().__init__()
        self.setupUi(self)
        self.type = type_dialog
        self.properties = args
        self.con = args[0]
        self.cur = args[1]
        self.initUI()

    def initUI(self):
        for i in self.properties[2]:     # Заполняем comboBox данными из бд
            self.comboBox.addItem(i[0])
        self.buttonBox.accepted.connect(self.acept_data)
        self.buttonBox.rejected.connect(self.reject_data)
        if self.type == "edit":          # Если диалог направлен на редактирование данных - вбиваем данные в форму
            self.lineEdit_name.setText(self.properties[-1][1])
            self.lineEdit_ei.setText(self.properties[-1][2])
            self.spinBoxQuantity.setValue(int(self.properties[-1][3]))
            self.doubleSpinBoxPrice.setValue(float(self.properties[-1][4]))
            self.comboBox.setCurrentIndex(int(self.properties[-1][5]) - 1)

    def acept_data(self):
        try:
            # Получаем введенные пользователем данные
            name = self.lineEdit_name.text()
            ei = self.lineEdit_ei.text()
            k = int(self.spinBoxQuantity.text())
            price = float(self.doubleSpinBoxPrice.text().replace(",", "."))
            category = self.comboBox.currentText()
            if name and ei and price:      # В случае правильно введённых данных
                result = self.cur.execute("SELECT id FROM categories WHERE Категория = ?", (category,)).fetchall()
                if self.type == "add":
                    self.cur.execute("INSERT INTO warehouse(Название, 'ед.изм',"
                                     "'кол-во', 'цена р', категория) VALUES(?, ?, ?, ?, ?)",
                                     (name, ei, str(k), str(price), str(result[0][0])))
                else:
                    self.cur.execute("UPDATE warehouse SET Название = ?, 'ед.изм' = ?, 'кол-во' = ?,"
                                     " 'цена р' = ?, категория = ? WHERE id = ?",
                                     (name, ei, str(k), str(price), str(result[0][0]), self.properties[-1][0]))
                self.con.commit()
                self.close()
            else:
                self.lineEdit_error.setText("Некоторые поля не заполнены")
        except ValueError:
            self.lineEdit_error.setText("Некорректные значения полей")
        except sqlite3.IntegrityError:
            self.lineEdit_error.setText("Название занято")

    def reject_data(self):
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Warehouse()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
