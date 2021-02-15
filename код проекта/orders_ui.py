# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Orders.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(568, 519)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.pb_complete_order = QtWidgets.QPushButton(Form)
        self.pb_complete_order.setMinimumSize(QtCore.QSize(0, 30))
        self.pb_complete_order.setObjectName("pb_complete_order")
        self.gridLayout.addWidget(self.pb_complete_order, 4, 4, 1, 1)
        self.pb_production = QtWidgets.QPushButton(Form)
        self.pb_production.setMinimumSize(QtCore.QSize(0, 30))
        self.pb_production.setObjectName("pb_production")
        self.gridLayout.addWidget(self.pb_production, 4, 5, 1, 1)
        self.pb_new_order = QtWidgets.QPushButton(Form)
        self.pb_new_order.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.pb_new_order.setFont(font)
        self.pb_new_order.setObjectName("pb_new_order")
        self.gridLayout.addWidget(self.pb_new_order, 4, 3, 1, 1)
        self.le_error = QtWidgets.QLineEdit(Form)
        self.le_error.setEnabled(False)
        self.le_error.setObjectName("le_error")
        self.gridLayout.addWidget(self.le_error, 9, 0, 1, 6)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.gridLayout.addWidget(self.tableWidget, 6, 0, 3, 6)
        self.label = QtWidgets.QLabel(Form)
        self.label.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 25))
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 4, 1, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pb_complete_order.setText(_translate("Form", "Завершить заказ"))
        self.pb_production.setText(_translate("Form", "Пустить в производство"))
        self.pb_new_order.setText(_translate("Form", "  Новый заказ  "))
        self.label.setText(_translate("Form", "Заказы:"))
