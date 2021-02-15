# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Production.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(489, 498)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.le_error = QtWidgets.QLineEdit(Form)
        self.le_error.setEnabled(False)
        self.le_error.setObjectName("le_error")
        self.gridLayout.addWidget(self.le_error, 12, 0, 1, 2)
        self.tb_tools = QtWidgets.QTableWidget(Form)
        self.tb_tools.setObjectName("tb_tools")
        self.tb_tools.setColumnCount(0)
        self.tb_tools.setRowCount(0)
        self.gridLayout.addWidget(self.tb_tools, 9, 0, 1, 2)
        self.tw_warehouse = QtWidgets.QTableWidget(Form)
        self.tw_warehouse.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tw_warehouse.setObjectName("tw_warehouse")
        self.tw_warehouse.setColumnCount(0)
        self.tw_warehouse.setRowCount(0)
        self.gridLayout.addWidget(self.tw_warehouse, 5, 0, 1, 2)
        self.l_cost_price = QtWidgets.QLabel(Form)
        self.l_cost_price.setObjectName("l_cost_price")
        self.gridLayout.addWidget(self.l_cost_price, 10, 0, 1, 1)
        self.pb_production = QtWidgets.QPushButton(Form)
        self.pb_production.setObjectName("pb_production")
        self.gridLayout.addWidget(self.pb_production, 11, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 2)
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 8, 0, 1, 2)
        self.tw_works = QtWidgets.QTableWidget(Form)
        self.tw_works.setObjectName("tw_works")
        self.tw_works.setColumnCount(0)
        self.tw_works.setRowCount(0)
        self.gridLayout.addWidget(self.tw_works, 7, 0, 1, 2)
        self.l_total = QtWidgets.QLabel(Form)
        self.l_total.setObjectName("l_total")
        self.gridLayout.addWidget(self.l_total, 10, 1, 1, 1)
        self.l_size = QtWidgets.QLabel(Form)
        self.l_size.setObjectName("l_size")
        self.gridLayout.addWidget(self.l_size, 4, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.l_name = QtWidgets.QLabel(Form)
        self.l_name.setObjectName("l_name")
        self.gridLayout.addWidget(self.l_name, 0, 0, 2, 1)
        self.l_picture = QtWidgets.QLabel(Form)
        self.l_picture.setMinimumSize(QtCore.QSize(100, 100))
        self.l_picture.setMaximumSize(QtCore.QSize(100, 100))
        self.l_picture.setText("")
        self.l_picture.setObjectName("l_picture")
        self.gridLayout.addWidget(self.l_picture, 0, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.l_cost_price.setText(_translate("Form", "Себестоимость:"))
        self.pb_production.setText(_translate("Form", "Добавить в производство"))
        self.label_5.setText(_translate("Form", "Работы:"))
        self.label_6.setText(_translate("Form", "Инструменты:"))
        self.l_total.setText(_translate("Form", "Итого:"))
        self.l_size.setText(_translate("Form", "Габариты:"))
        self.label_4.setText(_translate("Form", "Элементы склада:"))
        self.l_name.setText(_translate("Form", "Название:"))
