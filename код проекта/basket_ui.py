# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Basket.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(512, 400)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.pb_ex_1 = QtWidgets.QPushButton(Form)
        self.pb_ex_1.setMinimumSize(QtCore.QSize(0, 30))
        self.pb_ex_1.setMaximumSize(QtCore.QSize(400, 16777215))
        self.pb_ex_1.setObjectName("pb_ex_1")
        self.gridLayout.addWidget(self.pb_ex_1, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.tw_tools = QtWidgets.QTableWidget(Form)
        self.tw_tools.setObjectName("tw_tools")
        self.tw_tools.setColumnCount(0)
        self.tw_tools.setRowCount(0)
        self.gridLayout.addWidget(self.tw_tools, 4, 0, 1, 2)
        self.pb_ex_2 = QtWidgets.QPushButton(Form)
        self.pb_ex_2.setMinimumSize(QtCore.QSize(0, 30))
        self.pb_ex_2.setMaximumSize(QtCore.QSize(400, 16777215))
        self.pb_ex_2.setObjectName("pb_ex_2")
        self.gridLayout.addWidget(self.pb_ex_2, 3, 1, 1, 1)
        self.tw_warehouse = QtWidgets.QTableWidget(Form)
        self.tw_warehouse.setObjectName("tw_warehouse")
        self.tw_warehouse.setColumnCount(0)
        self.tw_warehouse.setRowCount(0)
        self.gridLayout.addWidget(self.tw_warehouse, 2, 0, 1, 2)
        self.le_error = QtWidgets.QLineEdit(Form)
        self.le_error.setEnabled(False)
        self.le_error.setObjectName("le_error")
        self.gridLayout.addWidget(self.le_error, 5, 0, 1, 2)
        self.pb_update = QtWidgets.QPushButton(Form)
        self.pb_update.setMinimumSize(QtCore.QSize(0, 30))
        self.pb_update.setMaximumSize(QtCore.QSize(400, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../pictures/update.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_update.setIcon(icon)
        self.pb_update.setObjectName("pb_update")
        self.gridLayout.addWidget(self.pb_update, 1, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Инструменты на замену:"))
        self.pb_ex_1.setText(_translate("Form", "Сохранить в Exсel"))
        self.label.setText(_translate("Form", "Корзина покупок:"))
        self.pb_ex_2.setText(_translate("Form", "Сохранить в Exсel "))
        self.pb_update.setText(_translate("Form", "Обновить"))
