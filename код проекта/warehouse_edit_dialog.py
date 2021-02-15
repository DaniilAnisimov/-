# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'warehouse_edit_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(312, 292)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 1)
        self.lineEdit_ei = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_ei.setObjectName("lineEdit_ei")
        self.gridLayout.addWidget(self.lineEdit_ei, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 8, 0, 1, 1)
        self.doubleSpinBoxPrice = QtWidgets.QDoubleSpinBox(Dialog)
        self.doubleSpinBoxPrice.setMaximum(1000000.0)
        self.doubleSpinBoxPrice.setObjectName("doubleSpinBoxPrice")
        self.gridLayout.addWidget(self.doubleSpinBoxPrice, 7, 0, 1, 1)
        self.lineEdit_name = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.gridLayout.addWidget(self.lineEdit_name, 1, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 9, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.lineEdit_error = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_error.setEnabled(False)
        self.lineEdit_error.setObjectName("lineEdit_error")
        self.gridLayout.addWidget(self.lineEdit_error, 11, 0, 1, 1)
        self.spinBoxQuantity = QtWidgets.QSpinBox(Dialog)
        self.spinBoxQuantity.setObjectName("spinBoxQuantity")
        self.gridLayout.addWidget(self.spinBoxQuantity, 5, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 10, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "название:"))
        self.label_3.setText(_translate("Dialog", "кол-во:"))
        self.label_4.setText(_translate("Dialog", "цена р:"))
        self.label_5.setText(_translate("Dialog", "категория:"))
        self.label_2.setText(_translate("Dialog", "ед. изм.:"))
