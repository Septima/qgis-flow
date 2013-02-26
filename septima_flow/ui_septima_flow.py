# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'septima_flow\ui_septima_flow.ui'
#
# Created: Mon Feb 25 15:42:19 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_septima_flow(object):
    def setupUi(self, septima_flow):
        septima_flow.setObjectName(_fromUtf8("septima_flow"))
        septima_flow.resize(437, 215)
        self.verticalLayoutWidget = QtGui.QWidget(septima_flow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 421, 201))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.inputGroupBox = QtGui.QGroupBox(self.verticalLayoutWidget)
        self.inputGroupBox.setObjectName(_fromUtf8("inputGroupBox"))
        self.inputLagLabel = QtGui.QLabel(self.inputGroupBox)
        self.inputLagLabel.setGeometry(QtCore.QRect(10, 20, 43, 20))
        self.inputLagLabel.setObjectName(_fromUtf8("inputLagLabel"))
        self.lagComboBox = QtGui.QComboBox(self.inputGroupBox)
        self.lagComboBox.setGeometry(QtCore.QRect(70, 20, 287, 20))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lagComboBox.sizePolicy().hasHeightForWidth())
        self.lagComboBox.setSizePolicy(sizePolicy)
        self.lagComboBox.setMinimumSize(QtCore.QSize(200, 0))
        self.lagComboBox.setObjectName(_fromUtf8("lagComboBox"))
        self.onlySelectedCheckBox = QtGui.QCheckBox(self.inputGroupBox)
        self.onlySelectedCheckBox.setGeometry(QtCore.QRect(70, 50, 121, 17))
        self.onlySelectedCheckBox.setObjectName(_fromUtf8("onlySelectedCheckBox"))
        self.verticalLayout.addWidget(self.inputGroupBox)
        self.outputGroupBox = QtGui.QGroupBox(self.verticalLayoutWidget)
        self.outputGroupBox.setObjectName(_fromUtf8("outputGroupBox"))
        self.resultatLagLineEdit = QtGui.QLineEdit(self.outputGroupBox)
        self.resultatLagLineEdit.setGeometry(QtCore.QRect(90, 20, 287, 20))
        self.resultatLagLineEdit.setObjectName(_fromUtf8("resultatLagLineEdit"))
        self.resultatLagLabel = QtGui.QLabel(self.outputGroupBox)
        self.resultatLagLabel.setGeometry(QtCore.QRect(8, 20, 76, 20))
        self.resultatLagLabel.setObjectName(_fromUtf8("resultatLagLabel"))
        self.verticalLayout.addWidget(self.outputGroupBox)
        self.buttonBox = QtGui.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(septima_flow)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), septima_flow.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), septima_flow.reject)
        QtCore.QMetaObject.connectSlotsByName(septima_flow)

    def retranslateUi(self, septima_flow):
        septima_flow.setWindowTitle(QtGui.QApplication.translate("septima_flow", "septima_flow", None, QtGui.QApplication.UnicodeUTF8))
        self.inputGroupBox.setTitle(QtGui.QApplication.translate("septima_flow", "Input", None, QtGui.QApplication.UnicodeUTF8))
        self.inputLagLabel.setText(QtGui.QApplication.translate("septima_flow", "Lag", None, QtGui.QApplication.UnicodeUTF8))
        self.onlySelectedCheckBox.setText(QtGui.QApplication.translate("septima_flow", "Kun valgte features", None, QtGui.QApplication.UnicodeUTF8))
        self.outputGroupBox.setTitle(QtGui.QApplication.translate("septima_flow", "Output", None, QtGui.QApplication.UnicodeUTF8))
        self.resultatLagLabel.setText(QtGui.QApplication.translate("septima_flow", "Navn på nyt lag", None, QtGui.QApplication.UnicodeUTF8))

