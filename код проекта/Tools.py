import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from tools_ui import Ui_Form
from tools_edit_dialog import Ui_Dialog


class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):       # Создан для запрета на редактирование таблицы
        return


class Tools(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Подключаем бд
        self.con = sqlite3.connect("database/production.db")
        self.cur = self.con.cursor()
        self.initUI()

    def initUI(self):
        self.comboBox.addItem("Инвентарный номер")
        self.comboBox.addItem("Наименование")
        # Подключаем сигналы от изменения значения comboBox, текста lineEdit соответственно
        self.lineEdit.textChanged.connect(self.load_table)
        # Подключаем событие для кнопки pb_edit (pb от сокращения PushButon), pb_add, pb_update соответственно
        self.pb_edit.clicked.connect(self.edit_elem)
        self.pb_add.clicked.connect(self.add_elem)
        self.pb_update.clicked.connect(self.load_table)
        self.pb_new.clicked.connect(self.new)
        self.load_table()

    def load_table(self):
        # Создаём запрос для сортировки tools (бд), начало Названия товара должно начинаться с self.lineEdit.text()
        if self.comboBox.currentText() == "Инвентарный номер":
            result = self.cur.execute("""SELECT * FROM tools WHERE "Инвентарный номер" like ?""",
                                      (self.lineEdit.text() + "%", )).fetchall()
        else:
            result = self.cur.execute("""SELECT * FROM tools WHERE Название like ?""",
                                      (self.lineEdit.text() + "%", )).fetchall()
        # Получаем список заголовков таблицы
        for i in range(len(result)):
            result[i] = list(result[i])[:-1]
        title_list = [i[1] for i in self.cur.execute("pragma table_info(tools)").fetchall()][:-1]
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
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem1)))
        # Задаём свойства расширения для каждого столбца
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        for i in range(2, 10):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

    def new(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        # Получаем список выделенных строк
        if len(rows) != 1:  # Строка обязательно должна быть одна
            return 0
        rows = rows[0]
        # Получаем id
        id_tools = int(self.tableWidget.item(rows, 0).text())
        valid = QMessageBox.question(self, '', "Действительно заменить элемент с id " + str(id_tools) + " на новый",
                                     QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            # Заменяем инструмент на новый, если он есть в корзине удаляем из корзины.
            result = self.cur.execute(f"""SELECT "кол-во" FROM "shopping_list_tools"
                            WHERE "id Инструмента" = {id_tools}""").fetchall()
            if result:
                self.cur.execute(f"""DELETE FROM "shopping_list_tools" WHERE "id Инструмента" = {id_tools}""")
                self.con.commit()
            # Обновляем настройки инструмента
            result = self.cur.execute(f"""SELECT * FROM "tools"
                                        WHERE "id" = {id_tools}""").fetchall()[0]
            self.cur.execute("""UPDATE tools SET "Кол-во операций" = ?, "Остаточная стоимость р" = ?,
                "%  износа" = ? WHERE id = ?""", (result[-1], result[2], 100, id_tools))
            self.con.commit()
        self.load_table()

    def add_elem(self):
        # Класс вызывает диалоговое окно и передаёт нужные параметры для работы.
        dialogue = Editdialog("add", self.con, self.cur)
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
        for i in range(10):
            select_row.append(self.tableWidget.item(rows[0], i).text())
        # Класс вызывает диалоговое окно и передаёт нужные параметры для работы.
        dialogue = Editdialog("edit", self.con, self.cur, select_row)
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
        self.con = args[0]
        self.cur = args[1]
        self.select_row = args[-1]
        self.initUI()

    def initUI(self):
        self.buttonBox.accepted.connect(self.acept_data)
        self.buttonBox.rejected.connect(self.reject_data)
        if self.type == "edit":          # Если диалог направлен на редактирование данных - вбиваем данные в форму
            self.le_name.setText(self.select_row[1])
            self.dsb_price.setValue(float(self.select_row[2].replace(",", ".")))
            self.sb_quantity.setValue(int(self.select_row[3]))
            self.le_ei.setText(self.select_row[4])
            self.le_inventory_number.setText(self.select_row[6])
            self.sb_power.setValue(int(self.select_row[7]))

    def acept_data(self):
        try:
            # Получаем введенные пользователем данные
            name = self.le_name.text()
            price = float(self.dsb_price.text().replace(",", "."))
            quantity = int(self.sb_quantity.text())
            ei = self.le_ei.text()
            inventory_number = self.le_inventory_number.text()
            power = int(self.sb_power.text())
            if name and ei and inventory_number and price > 0 and quantity >= 0:
                # В случае правильно введённых данных
                if self.type == "add":
                    depreciation = float(price / quantity) + float(price / quantity) * 0.1
                    residual_value = price
                    wear = 100
                    list_of_values = [name, price, quantity, ei, depreciation,
                                      inventory_number, power, residual_value, wear, quantity]
                    self.cur.execute("INSERT INTO tools(Название, Цена, 'Кол-во операций',"
                                     "'Ед. изм', Амортизация, 'Инвентарный номер',"
                                     "'Мощность Вт', 'Остаточная стоимость р', '%  износа', '100%  операций')"
                                     "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", list_of_values)
                else:
                    result = self.cur.execute("""SELECT "100%  операций" FROM tools"
                                              " WHERE id = ?""", (self.select_row[0],)).fetchall()[0][0]
                    depreciation = float(price / result)
                    residual_value = (quantity / result) * price
                    wear = (quantity / result) * 100
                    list_of_values = [name, price, quantity, ei, depreciation,
                                      inventory_number, power, residual_value, wear, result]
                    self.cur.execute("UPDATE tools SET Название = ?, Цена = ?,"
                                     "'Кол-во операций' = ?, 'Ед. изм' = ?, Амортизация = ?,"
                                     "'Инвентарный номер' = ?, 'Мощность Вт' = ?,"
                                     "'Остаточная стоимость р' = ?, '%  износа' = ?, '100%  операций' = ? WHERE id = ?",
                                     list_of_values + [self.select_row[0]])
                self.con.commit()
                self.close()
            else:
                self.lineEdit_error.setText("Некоторые поля не заполнены")
        except ValueError:
            self.lineEdit_error.setText("Некорректные значения полей")
        except sqlite3.IntegrityError as f:
            if "Название" in str(f):
                self.lineEdit_error.setText("Название занято")
            else:
                self.lineEdit_error.setText("Инвентарный номер занят")

    def reject_data(self):
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Tools()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
