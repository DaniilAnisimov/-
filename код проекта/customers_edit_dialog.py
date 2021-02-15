# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'customers_edit_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(261, 217)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.le_email = QtWidgets.QLineEdit(Dialog)
        self.le_email.setObjectName("le_email")
        self.gridLayout.addWidget(self.le_email, 5, 0, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_error = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_error.setEnabled(False)
        self.lineEdit_error.setObjectName("lineEdit_error")
        self.gridLayout.addWidget(self.lineEdit_error, 7, 0, 1, 1)
        self.le_fio = QtWidgets.QLineEdit(Dialog)
        self.le_fio.setObjectName("le_fio")
        self.gridLayout.addWidget(self.le_fio, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.le_phone = QtWidgets.QLineEdit(Dialog)
        self.le_phone.setObjectName("le_phone")
        self.gridLayout.addWidget(self.le_phone, 3, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Ф.И.О.:"))
        self.label_2.setText(_translate("Dialog", "Телефон:"))
        self.label_4.setText(_translate("Dialog", "e-mail:"))
