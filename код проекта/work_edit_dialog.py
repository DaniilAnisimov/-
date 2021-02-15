# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'work_edit_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(255, 202)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.le_ei = QtWidgets.QLineEdit(Dialog)
        self.le_ei.setObjectName("le_ei")
        self.gridLayout.addWidget(self.le_ei, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.le_name = QtWidgets.QLineEdit(Dialog)
        self.le_name.setObjectName("le_name")
        self.gridLayout.addWidget(self.le_name, 1, 0, 1, 1)
        self.dsb_price = QtWidgets.QDoubleSpinBox(Dialog)
        self.dsb_price.setMaximum(1e+34)
        self.dsb_price.setObjectName("dsb_price")
        self.gridLayout.addWidget(self.dsb_price, 5, 0, 1, 1)
        self.lineEdit_error = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_error.setEnabled(False)
        self.lineEdit_error.setObjectName("lineEdit_error")
        self.gridLayout.addWidget(self.lineEdit_error, 7, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Название:"))
        self.label_3.setText(_translate("Dialog", "Стоимость р.:"))
        self.label_2.setText(_translate("Dialog", "Ед. изм.:"))
