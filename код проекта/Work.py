import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from work_ui import Ui_Form
from work_edit_dialog import Ui_Dialog


class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):       # Создан для запрета на редактирование таблицы
        return


class Work(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("database/production.db")
        self.cur = self.con.cursor()
        self.initUI()

    def initUI(self):
        # Подключаем сигнал зависящий от изменения текста lineEdit
        self.lineEdit.textChanged.connect(self.load_table)
        # Подключаем событие для кнопки pb_edit (pb от сокращения PushButon), pb_add соответственно
        self.pb_edit.clicked.connect(self.edit_elem)
        self.pb_add.clicked.connect(self.add_elem)
        self.load_table()

    def load_table(self):
        # Создаём запрос для сортировки tools (бд), начало Названия товара должно начинаться с self.lineEdit.text()
        result = self.cur.execute("""SELECT * FROM works WHERE Название like ?""",
                                  (self.lineEdit.text() + "%", )).fetchall()
        # Получаем список заголовков таблицы
        title_list = [i[1] for i in self.cur.execute("pragma table_info(works)").fetchall()]
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
        for i in range(4):   # Задаём свойства расширения для каждого столбца каждой таблицы
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)       # Stretch - максимально расшириться
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)  # ResizeToContents - минимально

    def add_elem(self):
        # Класс вызывает диалоговое окно и передаёт нужные параметры для работы.
        dialog = Editdialog("add", self.con, self.cur)
        dialog.show()
        # Отключаем основное окно до окончания работы диалогового окна
        self.setEnabled(False)
        dialog.exec()
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
        for i in range(4):
            select_row.append(self.tableWidget.item(rows[0], i).text())
        # Класс вызывает диалоговое окно и передаёт нужные параметры для работы.
        dialog = Editdialog("edit", self.con, self.cur, select_row)
        dialog.show()
        # Отключаем основное окно до окончания работы диалогового окна
        self.setEnabled(False)
        dialog.exec()
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
            self.le_ei.setText(self.select_row[2])
            self.dsb_price.setValue(float(self.select_row[3].replace(",", ".")))

    def acept_data(self):
        try:
            # Получаем введенные пользователем данные
            name = self.le_name.text()
            price = float(self.dsb_price.text().replace(",", "."))
            ei = self.le_ei.text()     # Единица измерения
            if name and ei and price:      # В случае правильно введённых данных
                if self.type == "add":
                    self.cur.execute("INSERT INTO works(Название, 'Ед. изм', 'Стоимость р')"
                                     "VALUES(?, ?, ?)", (name, ei, price))
                else:
                    self.cur.execute("UPDATE works SET 'Название' = ?, 'Ед. изм' = ?,"
                                     " 'Стоимость р' = ? WHERE id = ?", (name, ei, price, self.select_row[0]))
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
    ex = Work()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
