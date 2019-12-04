# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'IPFC_Start_menu.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_StartMenu(object):
    def setupUi(self, StartMenu):
        StartMenu.setObjectName("StartMenu")
        StartMenu.resize(380, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(StartMenu.sizePolicy().hasHeightForWidth())
        StartMenu.setSizePolicy(sizePolicy)
        StartMenu.setStyleSheet("#StartMenu { border-image: url(split_grey_background.jpg) 0 0 0 0 stretch stretch;}")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(StartMenu)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelChooseDeck = QtWidgets.QLabel(StartMenu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelChooseDeck.sizePolicy().hasHeightForWidth())
        self.labelChooseDeck.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Menlo")
        font.setPointSize(24)
        self.labelChooseDeck.setFont(font)
        self.labelChooseDeck.setObjectName("labelChooseDeck")
        self.verticalLayout.addWidget(self.labelChooseDeck)
        self.listWidgetDecks = QtWidgets.QListWidget(StartMenu)
        font = QtGui.QFont()
        font.setFamily("Menlo")
        self.listWidgetDecks.setFont(font)
        self.listWidgetDecks.setAlternatingRowColors(True)
        self.listWidgetDecks.setProperty("isWrapping", True)
        self.listWidgetDecks.setWordWrap(True)
        self.listWidgetDecks.setObjectName("listWidgetDecks")
        self.verticalLayout.addWidget(self.listWidgetDecks)
        self.pushButtonUseDeck = QtWidgets.QPushButton(StartMenu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonUseDeck.sizePolicy().hasHeightForWidth())
        self.pushButtonUseDeck.setSizePolicy(sizePolicy)
        self.pushButtonUseDeck.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Menlo")
        self.pushButtonUseDeck.setFont(font)
        self.pushButtonUseDeck.setAutoDefault(False)
        self.pushButtonUseDeck.setObjectName("pushButtonUseDeck")
        self.verticalLayout.addWidget(self.pushButtonUseDeck)
        self.pushButtonDeckImporter = QtWidgets.QPushButton(StartMenu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonDeckImporter.sizePolicy().hasHeightForWidth())
        self.pushButtonDeckImporter.setSizePolicy(sizePolicy)
        self.pushButtonDeckImporter.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Menlo")
        self.pushButtonDeckImporter.setFont(font)
        self.pushButtonDeckImporter.setAutoDefault(False)
        self.pushButtonDeckImporter.setObjectName("pushButtonDeckImporter")
        self.verticalLayout.addWidget(self.pushButtonDeckImporter)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(StartMenu)
        QtCore.QMetaObject.connectSlotsByName(StartMenu)

    def retranslateUi(self, StartMenu):
        _translate = QtCore.QCoreApplication.translate
        StartMenu.setWindowTitle(_translate("StartMenu", "Inter Planetary Flash Cards"))
        self.labelChooseDeck.setText(_translate("StartMenu", "Choose Deck"))
        self.pushButtonUseDeck.setText(_translate("StartMenu", "Use selected deck"))
        self.pushButtonDeckImporter.setText(_translate("StartMenu", "Deck importer exporter"))
