# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Work.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(634, 452)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 4)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 3, 0, 1, 4)
        self.pb_edit = QtWidgets.QPushButton(Form)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pictures/Edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_edit.setIcon(icon)
        self.pb_edit.setObjectName("pb_edit")
        self.gridLayout.addWidget(self.pb_edit, 2, 3, 1, 1)
        self.pb_add = QtWidgets.QPushButton(Form)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("pictures/Add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_add.setIcon(icon1)
        self.pb_add.setObjectName("pb_add")
        self.gridLayout.addWidget(self.pb_add, 2, 2, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Виды работ:"))
        self.label.setText(_translate("Form", "Подстрока для поиска:"))
        self.pb_edit.setText(_translate("Form", "Редактировать"))
        self.pb_add.setText(_translate("Form", "Добавить"))
