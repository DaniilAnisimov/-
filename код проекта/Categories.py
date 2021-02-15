import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from categories_edit_dialog import Ui_Dialog
from Сategories_ui import Ui_Form


class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):       # Создан для запрета на редактирование таблицы
        return


class Categories(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Подключаем бд
        self.con = sqlite3.connect("database/production.db")
        self.cur = self.con.cursor()
        self.initUI()

    def initUI(self):
        # Подключаем сигналы от изменения текста lineEdit
        self.lineEdit.textChanged.connect(self.load_table)
        # Подключаем событие для кнопки pb_edit (pb от сокращения PushButon), pb_add соответственно
        self.pb_edit.clicked.connect(self.edit_elem)
        self.pb_add.clicked.connect(self.add_elem)
        self.load_table()

    def load_table(self):
        # Создаём запрос для сортировки tools (бд), начало Названия товара должно начинаться с self.lineEdit.text()
        result = self.cur.execute("""SELECT * FROM categories WHERE Категория like ?""",
                                  (self.lineEdit.text() + "%", )).fetchall()
        # Получаем список заголовков таблицы
        title_list = [i[1] for i in self.cur.execute("pragma table_info(categories)").fetchall()]
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
        # Задаём свойства расширения для каждого столбца каждой таблицы
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

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
        for i in range(2):
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
            self.le_category.setText(self.select_row[1])

    def acept_data(self):
        try:
            # Получаем введенные пользователем данные
            name = self.le_category.text()
            if name:      # В случае правильно введённых данных
                if self.type == "add":
                    self.cur.execute("INSERT INTO categories(Категория)"
                                     "VALUES(?)", (name, ))
                else:
                    self.cur.execute("UPDATE categories SET Категория = ? WHERE id = ?", (name, self.select_row[0]))
                self.con.commit()
                self.close()
            else:
                self.lineEdit_error.setText("Поле не заполнено")
        except ValueError:
            self.lineEdit_error.setText("Некорректные значения полей")
        except sqlite3.IntegrityError:
            self.lineEdit_error.setText("Категория занята")

    def reject_data(self):
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Categories()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
