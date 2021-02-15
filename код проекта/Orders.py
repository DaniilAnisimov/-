import sys
import sqlite3
from PyQt5.QtCore import QDate
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import datetime
from PyQt5.QtGui import *
from orders_ui import Ui_Form
from order_edit_dialog import Ui_Dialog as Ui_Dialog1
from production_ui import Ui_Form as Ui_form_1


class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):       # Создан для запрета на редактирование таблицы
        return


class Orders(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("database/production.db")
        self.cur = self.con.cursor()
        self.initUI()

    def initUI(self):
        self.pb_complete_order.clicked.connect(self.complete_order)
        self.pb_new_order.clicked.connect(self.new_order)
        self.pb_production.clicked.connect(self.production)
        self.comboBox.addItem("Текущие")
        self.comboBox.addItem("Завершённые")
        self.comboBox.activated.connect(self.load_table)
        self.load_table()

    def production(self):
        # Получаем список выделенных элементов
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        if len(rows) != 1:
            return 0
        if self.tableWidget.item(rows[0], 5).text() == "Завершён":
            self.le_error.setText("Нельзя пустить в производство завершённый заказ")
        elif self.tableWidget.item(rows[0], 5).text() == "В производстве":
            self.le_error.setText("Этот заказ уже находится в производстве")
        elif len(rows) == 1:
            name = int(self.tableWidget.item(rows[0], 0).text())
            # Запускаем диалоговое окно с номером продукта
            dialogue = Production(int(self.tableWidget.item(rows[0], 4).text()))
            dialogue.show()
            # Отключаем основное окно до окончания работы диалогового окна
            self.setEnabled(False)
            dialogue.exec()
            self.setEnabled(True)
            if dialogue.otv:         # Если человек пустил продукт в производство: меняем значения поля
                self.cur.execute("UPDATE orders SET 'Текущее состояние' = ? WHERE id = ?", ("В производстве", name))
                self.con.commit()
                self.load_table()
        elif len(rows) > 1:
            self.le_error.setText("Можно выбирать только 1 элемент")
        else:
            self.le_error.setText("Ни один элемент не выбран")

    def complete_order(self):      # Функция завершающая заказы
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        if len(rows) != 1:
            return 0
        if self.tableWidget.item(rows[0], 5).text() == "Завершён":
            self.le_error.setText("Нельзя завершить завершённое")
        elif len(rows) == 1:
            name = int(self.tableWidget.item(rows[0], 0).text())
            valid = QMessageBox.question(self, '', "Действительно завершить заказ с id =" + str(name),
                                         QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                self.cur.execute("UPDATE orders SET 'Текущее состояние' = ? WHERE id = ?", ("Завершён", name))
                self.con.commit()
                self.load_table()
        elif len(rows) > 1:
            self.le_error.setText("Можно выбирать только 1 элемент")
        else:
            self.le_error.setText("Ни один элемент не выбран")

    def load_table(self):
        header = self.tableWidget.horizontalHeader()
        if self.comboBox.currentText() == "Текущие":
            order_type = ("В производстве", "Ожидание")
        else:
            order_type = ("Завершён", "")
        # Получаем данные
        result = self.cur.execute(f"""SELECT * FROM orders WHERE "Текущее состояние"
            IN {order_type}""").fetchall()
        # Меняем значение столбца 1 на ФИО клиента
        for i in range(len(result)):
            result[i] = list(result[i])
            result[i][1] = self.cur.execute(f"""SELECT "Ф.И.О" FROM 
                customers WHERE id = {result[i][1]}""").fetchall()[0][0]
        title_list = [i[1] for i in self.cur.execute("pragma table_info(orders)").fetchall()]
        # Заполняем tableWidget
        self.tableWidget.setColumnCount(len(title_list))
        self.tableWidget.setHorizontalHeaderLabels(title_list)
        self.tableWidget.setRowCount(0)
        self.tableWidget.resizeColumnsToContents()
        delegate = ReadOnlyDelegate(self.tableWidget)
        for i, elem in enumerate(result):
            self.tableWidget.setRowCount(i + 1)
            self.tableWidget.setItemDelegateForRow(i, delegate)
            for j, elem1 in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem1)))
        for i in range(6):   # Задаём свойства расширения для каждого столбца каждой таблицы
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        # Запускаем функцию для подсветки активных заказов
        self.deadline(self.tableWidget.rowCount())

    def deadline(self, k):    # Функция которая подсвечивает все активные заказы
        for i in range(k):
            if self.tableWidget.item(i, 5).text() != "Завершён":
                # Получаем и обрабатываем дату заказа
                date_today = self.tableWidget.item(i, 2).text().split(":")
                date_today = datetime.date(int(date_today[2]), int(date_today[1]), int(date_today[0]))
                date_deadline = self.tableWidget.item(i, 3).text().split(":")
                date_deadline = datetime.date(int(date_deadline[2]), int(date_deadline[1]), int(date_deadline[0]))
                date = date_deadline - date_today
                if date.days <= 3:       # Если до дедлайна осталось 3 дня то строка подсвечивается жёлтым
                    self.color_row(i, QColor(255, 232, 20))
                elif date.days < 0:      # Если дедлайн прошёл - красным
                    self.color_row(i, QColor(255, 26, 26))
                else:                    # Иначе зелёным
                    self.color_row(i, QColor(8, 224, 4))
                # Кстати отличный сайт для подбора HTML CSS Палитр цветов - CSSCOLOR.RU

    def color_row(self, row, color):
        for i in range(self.tableWidget.columnCount()):
            self.tableWidget.item(row, i).setBackground(color)

    def new_order(self):
        dialogue = AddDialog(self.con, self.cur)
        dialogue.show()
        # Отключаем основное окно до окончания работы диалогового окна
        self.setEnabled(False)
        dialogue.exec()
        self.setEnabled(True)
        # После изменений обновляем таблицу
        self.load_table()


class AddDialog(QDialog, Ui_Dialog1):      # Обычный диалог для добавления новых элементов
    def __init__(self, con, cur):
        super(AddDialog, self).__init__()
        self.setupUi(self)
        self.con = con
        self.cur = cur
        self.cast = {}
        self.initUI()

    def initUI(self):
        result = self.cur.execute("""SELECT id, "Ф.И.О" FROM customers""").fetchall()
        self.dateEdit.setMinimumDate(QDate().currentDate())
        self.dateEdit.setCalendarPopup(True)
        for i in result:
            self.cast[i[1]] = i[0]
            self.comboBox.addItem(i[1])
        self.buttonBox.accepted.connect(self.acept_data)
        self.lineEdit.textChanged.connect(self.load_table)
        self.buttonBox.rejected.connect(self.reject_data)
        self.load_table()

    def load_table(self):
        # Подгружаем данные
        result = self.cur.execute(f"""SELECT * FROM product WHERE Название like ?""",
                                  (self.lineEdit.text() + "%", )).fetchall()
        new_result = []
        for i in result:
            n = [j for j in i]
            new_result.append(n[:3] + n[4:])
        result = new_result
        # Получаем заголовки
        title_list = [i[1] for i in self.cur.execute(f"pragma table_info(product)").fetchall()]
        title_list = title_list[:3] + title_list[4:]
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

    def acept_data(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))  # Получаем введенные пользователем данные
        if len(rows) == 1:
            name = self.cur.execute("""SELECT id FROM customers WHERE "Ф.И.О" = ?""",
                                    (self.comboBox.currentText(),)).fetchall()[0][0]
            date_t = self.dateEdit.date()
            date_today = QDate().currentDate()
            order = self.tableWidget.item(rows[0], 0).text()
            date_not_today = str(date_today.day()) + ":" + str(date_today.month()) + ":" + str(date_today.year())
            date_not_not_today = str(date_t.day()) + ":" + str(date_t.month()) + ":" + str(date_t.year())
            self.cur.execute("INSERT INTO orders('ФИО заказчика', 'Дата начала', "          # Добавляем новый элемент
                             "'Дата сдачи', 'Номер в каталоге', 'Текущее состояние') VALUES(?, ?, ?, ?, ?)",
                             (name, date_not_today, date_not_not_today, int(order), "Ожидание"))
            self.con.commit()
            self.close()
        elif len(rows) > 1:
            self.le_error.setText("Можно выбирать только 1 элемент")
        else:
            self.le_error.setText("Ни один элемент не выбран")

    def reject_data(self):
        self.close()


class Production(QDialog, Ui_form_1):      # Класс списывающий элементы со склада и амортизирующая инструменты
    def __init__(self, number):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("database/production.db")
        self.namber = number
        self.otv = 0        # 1 если пользователь пустил элемент в производство
        self.cur = self.con.cursor()
        self.initUI()

    def initUI(self):
        table_data = []             # Добавляем в n списки элементов склада, инструменты и работы
        list_of_data = []
        result = list(self.cur.execute(f"""SELECT "Элемент склада", "Кол-во" FROM \
            warehouse_used WHERE Продукт = {self.namber}""").fetchall())
        for i in result:
            list_of_data.append(list(self.cur.execute(f"""SELECT * FROM warehouse WHERE id = {i[0]}""").fetchall()[0]))
            list_of_data[-1][3] = i[1]
        table_data.append([self.tw_warehouse, list_of_data,
                           [i[1] for i in self.cur.execute("pragma table_info(warehouse)").fetchall()]])

        list_of_data = []
        result = list(self.cur.execute(f"""SELECT Работа, "Кол-во" FROM \
                    works_used WHERE Продукт = {self.namber}""").fetchall())
        for i in result:
            list_of_data.append(list(self.cur.execute(f"""SELECT * FROM works WHERE id = {i[0]}""").fetchall()[0])
                                + [i[1]])
        table_data.append([self.tw_works, list_of_data,
                           [i[1] for i in self.cur.execute("pragma table_info(works)").fetchall()] + ["Кол-во работ:"]])

        list_of_data = []
        result = list(self.cur.execute(f"""SELECT Инструмент, "Кол-во" FROM \
                            tools_used WHERE Продукт = {self.namber}""").fetchall())
        for i in result:
            list_of_data.append(list(self.cur.execute(f"""SELECT * FROM tools WHERE id = {i[0]}""").fetchall()[0])
                                + [i[1]])
        table_data.append([self.tb_tools, list_of_data,
                           [i[1] for i in self.cur.execute("pragma table_info(tools)").fetchall()] +
                           ["Кол-во производимых операций:"]])
        for table in table_data:        # Проходясь по n заполняем 3 таблицы
            tablewidget = table[0]
            header = tablewidget.horizontalHeader()
            result = table[1]
            title_list = table[2]
            tablewidget.setColumnCount(len(title_list))
            tablewidget.setHorizontalHeaderLabels(title_list)
            tablewidget.setRowCount(0)
            tablewidget.resizeColumnsToContents()
            delegate = ReadOnlyDelegate(tablewidget)
            for i, elem in enumerate(result):
                tablewidget.setRowCount(i + 1)
                tablewidget.setItemDelegateForRow(i, delegate)
                for j, elem1 in enumerate(elem):
                    header.setSectionResizeMode(j, QtWidgets.QHeaderView.Stretch)
                    tablewidget.setItem(i, j, QTableWidgetItem(str(elem1)))
        result = self.cur.execute(f"""SELECT * FROM product WHERE id = {self.namber}""").fetchall()[0]
        # записываем остальную информацию
        self.l_name.setText(self.l_name.text() + " " + result[1])
        self.l_size.setText(self.l_size.text() + " " + result[2])
        self.l_cost_price.setText(self.l_cost_price.text() + " " + str(result[4]))
        self.l_total.setText(self.l_total.text() + " " + str(result[5]))
        # Подружаем картинку
        pixmap = QPixmap(result[3])
        pixmap = pixmap.scaled(100, 100, QtCore.Qt.IgnoreAspectRatio)
        self.l_picture.setPixmap(pixmap)
        self.pb_production.clicked.connect(self.into_production)

    def into_production(self):          # Функция элементы со склада и амортизирующая инструменты
        for i in range(self.tw_warehouse.rowCount()):
            id = int(self.tw_warehouse.item(i, 0).text())
            result = self.cur.execute(f"""SELECT "кол-во" FROM warehouse
                WHERE id = {id}""").fetchall()[0][0]
            k = int(self.tw_warehouse.item(i, 3).text())      # Кол-во элементов на складе
            if result - k <= 0:      # Если элементов не хвадает работаем с корзиной
                self.cur.execute("UPDATE warehouse SET 'кол-во' = ? WHERE id = ?", (0, id))
                result1 = self.cur.execute(f"""SELECT "кол-во" FROM shopping_list_warehouse
                                    WHERE "id продукта" = {id}""").fetchall()   # Количество элементов в корзине
                if result1:
                    self.cur.execute("""UPDATE shopping_list_warehouse SET "кол-во" = ? WHERE "id продукта" = ?""",
                                     (k - result + result1[0][0], id))
                    self.con.commit()
                else:        # Добавляем в корзину новые элементы
                    self.cur.execute("INSERT INTO shopping_list_warehouse('id продукта', 'кол-во') VALUES(?, ?)",
                                     (id, k - result))
                    self.con.commit()
            else:
                self.cur.execute("UPDATE warehouse SET 'кол-во' = ? WHERE id = ?", (result - k, id))
                self.con.commit()

        for i in range(self.tb_tools.rowCount()):       # Амортизируем все инструменты
            id = int(self.tb_tools.item(i, 0).text())
            result = self.cur.execute(f"""SELECT "Кол-во операций" FROM tools WHERE id = {id}""").fetchall()[0][0]
            k = int(self.tb_tools.item(i, 11).text())
            n = list(self.cur.execute(f"""SELECT * FROM tools WHERE id = {id}""").fetchall())[0]
            if result - k <= 0:
                self.cur.execute("UPDATE tools SET 'Кол-во операций' = ?, "
                                 "'Остаточная стоимость р' = ?, '%  износа' = ? WHERE id = ?", (0, 0, 0, id))
                result = self.cur.execute(f"""SELECT "Кол-во" FROM shopping_list_tools 
                    WHERE "id Инструмента" = {id}""").fetchall()
                if not result:         # Если инструмент израсходовал свой ресурс добавляем его в корзину
                    self.cur.execute("INSERT INTO shopping_list_tools('id Инструмента', 'Кол-во') VALUES(?, ?)",
                                     (id, 1))
                self.con.commit()
            else:
                kn = result - k                   # Рассчитываем амортизацию
                self.cur.execute("UPDATE tools SET 'Кол-во операций' = ?, 'Остаточная стоимость р' = ?,"
                                 " '%  износа' = ? WHERE id = ?", (kn, (kn / n[-1]) * n[2], (kn / n[-1]) * 100, id))
                self.con.commit()
        self.otv = 1              # строка 213
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Orders()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
