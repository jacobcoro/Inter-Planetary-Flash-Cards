# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'IPFC_Import_options.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ImportOptions(object):
    def setupUi(self, ImportOptions):
        ImportOptions.setObjectName("ImportOptions")
        ImportOptions.resize(353, 319)
        ImportOptions.setWindowTitle("")
        ImportOptions.setStyleSheet("#ImportOptions { border-image: url(split_grey_background.jpg) 0 0 0 0 stretch stretch;}")
        self.gridLayout = QtWidgets.QGridLayout(ImportOptions)
        self.gridLayout.setObjectName("gridLayout")
        self.radioButtonAlphabatize = QtWidgets.QRadioButton(ImportOptions)
        self.radioButtonAlphabatize.setObjectName("radioButtonAlphabatize")
        self.gridLayout.addWidget(self.radioButtonAlphabatize, 5, 0, 1, 1)
        self.label = QtWidgets.QLabel(ImportOptions)
        font = QtGui.QFont()
        font.setFamily("Menlo")
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.radioButtonQuizletTxt = QtWidgets.QRadioButton(ImportOptions)
        font = QtGui.QFont()
        font.setFamily("Menlo")
        self.radioButtonQuizletTxt.setFont(font)
        self.radioButtonQuizletTxt.setChecked(True)
        self.radioButtonQuizletTxt.setObjectName("radioButtonQuizletTxt")
        self.gridLayout.addWidget(self.radioButtonQuizletTxt, 0, 0, 1, 1)
        self.pushButtonConvert = QtWidgets.QPushButton(ImportOptions)
        self.pushButtonConvert.setMinimumSize(QtCore.QSize(0, 35))
        font = QtGui.QFont()
        font.setFamily("Menlo")
        self.pushButtonConvert.setFont(font)
        self.pushButtonConvert.setObjectName("pushButtonConvert")
        self.gridLayout.addWidget(self.pushButtonConvert, 6, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(ImportOptions)
        font = QtGui.QFont()
        font.setFamily("Menlo")
        self.label_2.setFont(font)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.lineEditFbSep = QtWidgets.QLineEdit(ImportOptions)
        font = QtGui.QFont()
        font.setFamily("Menlo")
        self.lineEditFbSep.setFont(font)
        self.lineEditFbSep.setObjectName("lineEditFbSep")
        self.gridLayout.addWidget(self.lineEditFbSep, 2, 1, 1, 1)
        self.lineEditCardSep = QtWidgets.QLineEdit(ImportOptions)
        font = QtGui.QFont()
        font.setFamily("Menlo")
        self.lineEditCardSep.setFont(font)
        self.lineEditCardSep.setText("")
        self.lineEditCardSep.setObjectName("lineEditCardSep")
        self.gridLayout.addWidget(self.lineEditCardSep, 4, 1, 1, 1)

        self.retranslateUi(ImportOptions)
        QtCore.QMetaObject.connectSlotsByName(ImportOptions)

    def retranslateUi(self, ImportOptions):
        _translate = QtCore.QCoreApplication.translate
        self.radioButtonAlphabatize.setText(_translate("ImportOptions", "Alphabatize"))
        self.label.setText(_translate("ImportOptions", "Seperator between cards. For quizlet default (New line) leave blank"))
        self.radioButtonQuizletTxt.setText(_translate("ImportOptions", "txt file from Quizlet export"))
        self.pushButtonConvert.setText(_translate("ImportOptions", "Convert"))
        self.label_2.setText(_translate("ImportOptions", "Seperator between term and definition. For quizlet default (Tab) leave blank"))
