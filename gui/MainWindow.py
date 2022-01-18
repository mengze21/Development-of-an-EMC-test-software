# -*- coding: utf-8 -*-

# This script defines widgets and related windows of the MainWindow.

import sys

# from Calibration import Ui_Calibration
from Calibration import Ui_Calibration

sys.path.append('gui')
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import cv2 as cv


# This class defines the "Software Optionen" window, which is used for setting the software.
# The functions are not completed and activated.
# It's Qt-Designer file is "SoftwareOptions.ui" in folder "uifiles"
# This window can be opend by clicking "Security -> Software option" in the menu bar of the MainWindow
class Ui_SoftwareOptionen(object):
    def setupUi(self, SoftwareOptionen):
        SoftwareOptionen.setObjectName("SoftwareOptionen")
        SoftwareOptionen.resize(998, 671)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        SoftwareOptionen.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon_materials/22.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        SoftwareOptionen.setWindowIcon(icon)

        self.OptionTabWidget = QtWidgets.QTabWidget(SoftwareOptionen)
        self.OptionTabWidget.setGeometry(QtCore.QRect(20, 50, 960, 551))
        self.OptionTabWidget.setMinimumSize(QtCore.QSize(960, 551))
        self.OptionTabWidget.setMaximumSize(QtCore.QSize(960, 551))
        self.OptionTabWidget.setObjectName("OptionTabWidget")

        self.DuringTest = QtWidgets.QWidget()
        self.DuringTest.setObjectName("DuringTest")

        self.WarmUpAmplifierCheckBox = QtWidgets.QCheckBox(self.DuringTest)
        self.WarmUpAmplifierCheckBox.setGeometry(QtCore.QRect(40, 60, 211, 31))
        self.WarmUpAmplifierCheckBox.setMinimumSize(QtCore.QSize(211, 31))
        self.WarmUpAmplifierCheckBox.setMaximumSize(QtCore.QSize(211, 31))
        self.WarmUpAmplifierCheckBox.setChecked(True)
        self.WarmUpAmplifierCheckBox.setObjectName("WarmUpAmplifierCheckBox")

        self.AmplifierDeaktivierungLabel = QtWidgets.QCheckBox(self.DuringTest)
        self.AmplifierDeaktivierungLabel.setGeometry(QtCore.QRect(40, 170, 621, 31))
        self.AmplifierDeaktivierungLabel.setMinimumSize(QtCore.QSize(621, 31))
        self.AmplifierDeaktivierungLabel.setMaximumSize(QtCore.QSize(621, 31))
        self.AmplifierDeaktivierungLabel.setObjectName("AmplifierDeaktivierungLabel")

        self.MaximalIterationCheckBox = QtWidgets.QCheckBox(self.DuringTest)
        self.MaximalIterationCheckBox.setGeometry(QtCore.QRect(40, 280, 821, 31))
        self.MaximalIterationCheckBox.setMinimumSize(QtCore.QSize(821, 31))
        self.MaximalIterationCheckBox.setMaximumSize(QtCore.QSize(821, 31))
        self.MaximalIterationCheckBox.setAutoExclusive(False)
        self.MaximalIterationCheckBox.setObjectName("MaximalIterationCheckBox")

        self.MaximalLaufwerkstufeCheckBox = QtWidgets.QCheckBox(self.DuringTest)
        self.MaximalLaufwerkstufeCheckBox.setGeometry(QtCore.QRect(40, 390, 871, 31))
        self.MaximalLaufwerkstufeCheckBox.setMinimumSize(QtCore.QSize(871, 31))
        self.MaximalLaufwerkstufeCheckBox.setMaximumSize(QtCore.QSize(871, 31))
        self.MaximalLaufwerkstufeCheckBox.setObjectName("MaximalLaufwerkstufeCheckBox")

        self.WarmUpAmplifierLineEdit = QtWidgets.QLineEdit(self.DuringTest)
        self.WarmUpAmplifierLineEdit.setGeometry(QtCore.QRect(750, 100, 161, 31))
        self.WarmUpAmplifierLineEdit.setMinimumSize(QtCore.QSize(161, 31))
        self.WarmUpAmplifierLineEdit.setMaximumSize(QtCore.QSize(161, 31))
        self.WarmUpAmplifierLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.WarmUpAmplifierLineEdit.setObjectName("WarmUpAmplifierLineEdit")

        self.MaximalIterationLineEdit = QtWidgets.QLineEdit(self.DuringTest)
        self.MaximalIterationLineEdit.setGeometry(QtCore.QRect(750, 320, 161, 31))
        self.MaximalIterationLineEdit.setMinimumSize(QtCore.QSize(161, 31))
        self.MaximalIterationLineEdit.setMaximumSize(QtCore.QSize(161, 31))
        self.MaximalIterationLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.MaximalIterationLineEdit.setObjectName("MaximalIterationLineEdit")

        self.WarmUpAmplifierLabel = QtWidgets.QLabel(self.DuringTest)
        self.WarmUpAmplifierLabel.setGeometry(QtCore.QRect(230, 100, 341, 31))
        self.WarmUpAmplifierLabel.setMinimumSize(QtCore.QSize(341, 31))
        self.WarmUpAmplifierLabel.setMaximumSize(QtCore.QSize(341, 31))
        self.WarmUpAmplifierLabel.setObjectName("WarmUpAmplifierLabel")

        self.MaximalIterationLabel = QtWidgets.QLabel(self.DuringTest)
        self.MaximalIterationLabel.setGeometry(QtCore.QRect(230, 320, 401, 31))
        self.MaximalIterationLabel.setMinimumSize(QtCore.QSize(401, 31))
        self.MaximalIterationLabel.setMaximumSize(QtCore.QSize(401, 31))
        self.MaximalIterationLabel.setObjectName("MaximalIterationLabel")

        self.OptionTabWidget.addTab(self.DuringTest, "")
        self.delays = QtWidgets.QWidget()
        self.delays.setObjectName("delays")
        self.DelaysToolButton = QtWidgets.QToolButton(self.delays)
        self.DelaysToolButton.setGeometry(QtCore.QRect(710, 430, 161, 31))
        self.DelaysToolButton.setMinimumSize(QtCore.QSize(161, 31))
        self.DelaysToolButton.setMaximumSize(QtCore.QSize(161, 31))
        self.DelaysToolButton.setObjectName("DelaysToolButton")

        self.DelaysLabel_10 = QtWidgets.QLabel(self.delays)
        self.DelaysLabel_10.setGeometry(QtCore.QRect(70, 380, 311, 31))
        self.DelaysLabel_10.setMinimumSize(QtCore.QSize(311, 31))
        self.DelaysLabel_10.setMaximumSize(QtCore.QSize(311, 31))
        self.DelaysLabel_10.setObjectName("DelaysLabel_10")

        self.DelaysLabel_7 = QtWidgets.QLabel(self.delays)
        self.DelaysLabel_7.setGeometry(QtCore.QRect(70, 260, 381, 31))
        self.DelaysLabel_7.setMinimumSize(QtCore.QSize(381, 31))
        self.DelaysLabel_7.setMaximumSize(QtCore.QSize(381, 31))
        self.DelaysLabel_7.setObjectName("DelaysLabel_7")

        self.DelaysLabel_5 = QtWidgets.QLabel(self.delays)
        self.DelaysLabel_5.setGeometry(QtCore.QRect(70, 180, 281, 31))
        self.DelaysLabel_5.setMinimumSize(QtCore.QSize(281, 31))
        self.DelaysLabel_5.setMaximumSize(QtCore.QSize(281, 31))
        self.DelaysLabel_5.setObjectName("DelaysLabel_5")

        self.DelaysLineEdit_5 = QtWidgets.QLineEdit(self.delays)
        self.DelaysLineEdit_5.setGeometry(QtCore.QRect(710, 180, 161, 31))
        self.DelaysLineEdit_5.setMinimumSize(QtCore.QSize(161, 31))
        self.DelaysLineEdit_5.setMaximumSize(QtCore.QSize(161, 31))
        self.DelaysLineEdit_5.setAlignment(QtCore.Qt.AlignCenter)
        self.DelaysLineEdit_5.setObjectName("DelaysLineEdit_5")

        self.DelaysLineEdit_8 = QtWidgets.QLineEdit(self.delays)
        self.DelaysLineEdit_8.setGeometry(QtCore.QRect(710, 300, 161, 31))
        self.DelaysLineEdit_8.setMinimumSize(QtCore.QSize(161, 31))
        self.DelaysLineEdit_8.setMaximumSize(QtCore.QSize(161, 31))
        self.DelaysLineEdit_8.setAlignment(QtCore.Qt.AlignCenter)
        self.DelaysLineEdit_8.setObjectName("DelaysLineEdit_8")

        self.DelaysLabel_4 = QtWidgets.QLabel(self.delays)
        self.DelaysLabel_4.setGeometry(QtCore.QRect(70, 140, 331, 31))
        self.DelaysLabel_4.setMinimumSize(QtCore.QSize(331, 31))
        self.DelaysLabel_4.setMaximumSize(QtCore.QSize(331, 31))
        self.DelaysLabel_4.setObjectName("DelaysLabel_4")

        self.DelaysLineEdit_10 = QtWidgets.QLineEdit(self.delays)
        self.DelaysLineEdit_10.setGeometry(QtCore.QRect(710, 380, 161, 31))
        self.DelaysLineEdit_10.setMinimumSize(QtCore.QSize(161, 31))
        self.DelaysLineEdit_10.setMaximumSize(QtCore.QSize(161, 31))
        self.DelaysLineEdit_10.setAlignment(QtCore.Qt.AlignCenter)
        self.DelaysLineEdit_10.setObjectName("DelaysLineEdit_10")

        self.DelaysLineEdit_4 = QtWidgets.QLineEdit(self.delays)
        self.DelaysLineEdit_4.setGeometry(QtCore.QRect(710, 140, 161, 31))
        self.DelaysLineEdit_4.setMinimumSize(QtCore.QSize(161, 31))
        self.DelaysLineEdit_4.setMaximumSize(QtCore.QSize(161, 31))
        self.DelaysLineEdit_4.setAlignment(QtCore.Qt.AlignCenter)
        self.DelaysLineEdit_4.setObjectName("DelaysLineEdit_4")

        self.DelaysLabel_9 = QtWidgets.QLabel(self.delays)
        self.DelaysLabel_9.setGeometry(QtCore.QRect(70, 340, 441, 31))
        self.DelaysLabel_9.setMinimumSize(QtCore.QSize(441, 31))
        self.DelaysLabel_9.setMaximumSize(QtCore.QSize(441, 31))
        self.DelaysLabel_9.setObjectName("DelaysLabel_9")

        self.DelaysLineEdit_9 = QtWidgets.QLineEdit(self.delays)
        self.DelaysLineEdit_9.setGeometry(QtCore.QRect(710, 340, 161, 31))
        self.DelaysLineEdit_9.setMinimumSize(QtCore.QSize(161, 31))
        self.DelaysLineEdit_9.setMaximumSize(QtCore.QSize(161, 31))
        self.DelaysLineEdit_9.setAlignment(QtCore.Qt.AlignCenter)
        self.DelaysLineEdit_9.setObjectName("DelaysLineEdit_9")

        self.DelaysLabel_2 = QtWidgets.QLabel(self.delays)
        self.DelaysLabel_2.setGeometry(QtCore.QRect(60, 60, 421, 31))
        self.DelaysLabel_2.setMinimumSize(QtCore.QSize(421, 31))
        self.DelaysLabel_2.setMaximumSize(QtCore.QSize(421, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.DelaysLabel_2.setFont(font)
        self.DelaysLabel_2.setObjectName("DelaysLabel_2")

        self.DelaysLineEdit_2 = QtWidgets.QLineEdit(self.delays)
        self.DelaysLineEdit_2.setGeometry(QtCore.QRect(710, 60, 161, 31))
        self.DelaysLineEdit_2.setMinimumSize(QtCore.QSize(161, 31))
        self.DelaysLineEdit_2.setMaximumSize(QtCore.QSize(161, 31))
        self.DelaysLineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.DelaysLineEdit_2.setObjectName("DelaysLineEdit_2")

        self.DelaysLabel_3 = QtWidgets.QLabel(self.delays)
        self.DelaysLabel_3.setGeometry(QtCore.QRect(70, 100, 321, 31))
        self.DelaysLabel_3.setMinimumSize(QtCore.QSize(321, 31))
        self.DelaysLabel_3.setMaximumSize(QtCore.QSize(321, 31))
        self.DelaysLabel_3.setObjectName("DelaysLabel_3")

        self.DelaysLineEdit_6 = QtWidgets.QLineEdit(self.delays)
        self.DelaysLineEdit_6.setGeometry(QtCore.QRect(710, 220, 161, 31))
        self.DelaysLineEdit_6.setMinimumSize(QtCore.QSize(161, 31))
        self.DelaysLineEdit_6.setMaximumSize(QtCore.QSize(161, 31))
        self.DelaysLineEdit_6.setAlignment(QtCore.Qt.AlignCenter)
        self.DelaysLineEdit_6.setObjectName("DelaysLineEdit_6")

        self.DelaysLabel_8 = QtWidgets.QLabel(self.delays)
        self.DelaysLabel_8.setGeometry(QtCore.QRect(70, 300, 371, 31))
        self.DelaysLabel_8.setMinimumSize(QtCore.QSize(371, 31))
        self.DelaysLabel_8.setMaximumSize(QtCore.QSize(371, 31))
        self.DelaysLabel_8.setObjectName("DelaysLabel_8")

        self.DelaysLabel_11 = QtWidgets.QLabel(self.delays)
        self.DelaysLabel_11.setGeometry(QtCore.QRect(10, 470, 941, 31))
        self.DelaysLabel_11.setMinimumSize(QtCore.QSize(941, 31))
        self.DelaysLabel_11.setMaximumSize(QtCore.QSize(941, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.DelaysLabel_11.setFont(font)
        self.DelaysLabel_11.setObjectName("DelaysLabel_11")

        self.DelaysLineEdit_7 = QtWidgets.QLineEdit(self.delays)
        self.DelaysLineEdit_7.setGeometry(QtCore.QRect(710, 260, 161, 31))
        self.DelaysLineEdit_7.setMinimumSize(QtCore.QSize(161, 31))
        self.DelaysLineEdit_7.setMaximumSize(QtCore.QSize(161, 31))
        self.DelaysLineEdit_7.setAlignment(QtCore.Qt.AlignCenter)
        self.DelaysLineEdit_7.setObjectName("DelaysLineEdit_7")

        self.DelaysLineEdit_3 = QtWidgets.QLineEdit(self.delays)
        self.DelaysLineEdit_3.setGeometry(QtCore.QRect(710, 100, 161, 31))
        self.DelaysLineEdit_3.setMinimumSize(QtCore.QSize(161, 31))
        self.DelaysLineEdit_3.setMaximumSize(QtCore.QSize(161, 31))
        self.DelaysLineEdit_3.setAlignment(QtCore.Qt.AlignCenter)
        self.DelaysLineEdit_3.setObjectName("DelaysLineEdit_3")

        self.DelaysLabel_6 = QtWidgets.QLabel(self.delays)
        self.DelaysLabel_6.setGeometry(QtCore.QRect(70, 220, 421, 31))
        self.DelaysLabel_6.setMinimumSize(QtCore.QSize(421, 31))
        self.DelaysLabel_6.setMaximumSize(QtCore.QSize(421, 31))
        self.DelaysLabel_6.setObjectName("DelaysLabel_6")

        self.DelaysLineEdit_1 = QtWidgets.QLineEdit(self.delays)
        self.DelaysLineEdit_1.setGeometry(QtCore.QRect(710, 20, 161, 31))
        self.DelaysLineEdit_1.setMinimumSize(QtCore.QSize(161, 31))
        self.DelaysLineEdit_1.setMaximumSize(QtCore.QSize(161, 31))
        self.DelaysLineEdit_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.DelaysLineEdit_1.setAlignment(QtCore.Qt.AlignCenter)
        self.DelaysLineEdit_1.setObjectName("DelaysLineEdit_1")

        self.DelaysLabel_1 = QtWidgets.QLabel(self.delays)
        self.DelaysLabel_1.setGeometry(QtCore.QRect(60, 20, 371, 31))
        self.DelaysLabel_1.setMinimumSize(QtCore.QSize(371, 31))
        self.DelaysLabel_1.setMaximumSize(QtCore.QSize(371, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.DelaysLabel_1.setFont(font)
        self.DelaysLabel_1.setObjectName("DelaysLabel_1")

        self.OptionTabWidget.addTab(self.delays, "")
        self.Security = QtWidgets.QWidget()
        self.Security.setObjectName("Security")
        self.SecurityCheckBox_1 = QtWidgets.QCheckBox(self.Security)
        self.SecurityCheckBox_1.setGeometry(QtCore.QRect(100, 60, 771, 31))
        self.SecurityCheckBox_1.setMinimumSize(QtCore.QSize(771, 31))
        self.SecurityCheckBox_1.setMaximumSize(QtCore.QSize(771, 31))
        self.SecurityCheckBox_1.setObjectName("SecurityCheckBox_1")

        self.SecurityCheckBox_2 = QtWidgets.QCheckBox(self.Security)
        self.SecurityCheckBox_2.setGeometry(QtCore.QRect(100, 170, 221, 31))
        self.SecurityCheckBox_2.setMinimumSize(QtCore.QSize(221, 31))
        self.SecurityCheckBox_2.setMaximumSize(QtCore.QSize(221, 31))
        self.SecurityCheckBox_2.setObjectName("SecurityCheckBox_2")

        self.SecurityLineEdit = QtWidgets.QLineEdit(self.Security)
        self.SecurityLineEdit.setEnabled(False)
        self.SecurityLineEdit.setGeometry(QtCore.QRect(370, 170, 481, 31))
        self.SecurityLineEdit.setMinimumSize(QtCore.QSize(481, 31))
        self.SecurityLineEdit.setMaximumSize(QtCore.QSize(481, 31))
        self.SecurityLineEdit.setObjectName("SecurityLineEdit")

        self.SecurityToolButton_1 = QtWidgets.QToolButton(self.Security)
        self.SecurityToolButton_1.setEnabled(False)
        self.SecurityToolButton_1.setGeometry(QtCore.QRect(100, 240, 191, 31))
        self.SecurityToolButton_1.setMinimumSize(QtCore.QSize(191, 31))
        self.SecurityToolButton_1.setMaximumSize(QtCore.QSize(191, 31))
        self.SecurityToolButton_1.setObjectName("SecurityToolButton_1")

        self.SecurityToolButton_2 = QtWidgets.QToolButton(self.Security)
        self.SecurityToolButton_2.setEnabled(False)
        self.SecurityToolButton_2.setGeometry(QtCore.QRect(380, 240, 191, 31))
        self.SecurityToolButton_2.setMinimumSize(QtCore.QSize(191, 31))
        self.SecurityToolButton_2.setMaximumSize(QtCore.QSize(191, 31))
        self.SecurityToolButton_2.setObjectName("SecurityToolButton_2")

        self.SecurityToolButton_3 = QtWidgets.QToolButton(self.Security)
        self.SecurityToolButton_3.setEnabled(False)
        self.SecurityToolButton_3.setGeometry(QtCore.QRect(660, 240, 191, 31))
        self.SecurityToolButton_3.setMinimumSize(QtCore.QSize(191, 31))
        self.SecurityToolButton_3.setMaximumSize(QtCore.QSize(191, 41))
        self.SecurityToolButton_3.setObjectName("SecurityToolButton_3")

        self.OptionTabWidget.addTab(self.Security, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.EUTLabel = QtWidgets.QLabel(self.tab_5)
        self.EUTLabel.setGeometry(QtCore.QRect(30, 60, 711, 31))
        self.EUTLabel.setMinimumSize(QtCore.QSize(711, 31))
        self.EUTLabel.setMaximumSize(QtCore.QSize(711, 31))
        self.EUTLabel.setObjectName("EUTLabel")

        self.EUTComboBox = QtWidgets.QComboBox(self.tab_5)
        self.EUTComboBox.setGeometry(QtCore.QRect(740, 60, 181, 31))
        self.EUTComboBox.setMinimumSize(QtCore.QSize(181, 31))
        self.EUTComboBox.setMaximumSize(QtCore.QSize(181, 31))
        self.EUTComboBox.setEditable(True)
        self.EUTComboBox.setObjectName("EUTComboBox")

        self.EUTCheckBox = QtWidgets.QCheckBox(self.tab_5)
        self.EUTCheckBox.setGeometry(QtCore.QRect(60, 150, 841, 31))
        self.EUTCheckBox.setMinimumSize(QtCore.QSize(841, 31))
        self.EUTCheckBox.setMaximumSize(QtCore.QSize(841, 31))
        self.EUTCheckBox.setChecked(True)
        self.EUTCheckBox.setObjectName("EUTCheckBox")

        self.OptionTabWidget.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.OptionTabWidget.addTab(self.tab_6, "")
        self.HilfeToolButton = QtWidgets.QToolButton(SoftwareOptionen)
        self.HilfeToolButton.setGeometry(QtCore.QRect(20, 620, 121, 31))
        self.HilfeToolButton.setMinimumSize(QtCore.QSize(121, 31))
        self.HilfeToolButton.setMaximumSize(QtCore.QSize(121, 31))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon_materials/9.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.HilfeToolButton.setIcon(icon1)
        self.HilfeToolButton.setIconSize(QtCore.QSize(31, 31))
        self.HilfeToolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.HilfeToolButton.setObjectName("HilfeToolButton")

        self.AnwendungPushButton = QtWidgets.QPushButton(SoftwareOptionen)
        self.AnwendungPushButton.setGeometry(QtCore.QRect(670, 620, 131, 31))
        self.AnwendungPushButton.setMinimumSize(QtCore.QSize(131, 31))
        self.AnwendungPushButton.setMaximumSize(QtCore.QSize(131, 31))
        self.AnwendungPushButton.setDefault(True)
        self.AnwendungPushButton.setObjectName("AnwendungPushButton")

        self.StornierenPushButton = QtWidgets.QPushButton(SoftwareOptionen)
        self.StornierenPushButton.setGeometry(QtCore.QRect(820, 620, 131, 31))
        self.StornierenPushButton.setMinimumSize(QtCore.QSize(131, 31))
        self.StornierenPushButton.setMaximumSize(QtCore.QSize(131, 31))
        self.StornierenPushButton.setObjectName("StornierenPushButton")

        self.retranslateUi(SoftwareOptionen)
        self.OptionTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SoftwareOptionen)

        # Definition of signals
        self.SecurityCheckBox_2.clicked['bool'].connect(self.Creation_password_open)
        self.StornierenPushButton.clicked['bool'].connect(SoftwareOptionen.close)
        self.HilfeToolButton.clicked.connect(self.help_doc)
        self.DelaysToolButton.clicked.connect(self.function_info)
        self.AnwendungPushButton.clicked.connect(self.function_info)

        # Setting up the background color of this window
        pale = QtGui.QPalette()
        pale.setColor(QtGui.QPalette.Background, QtGui.QColor(248, 248, 248))
        SoftwareOptionen.setPalette(pale)

    def retranslateUi(self, SoftwareOptionen):
        _translate = QtCore.QCoreApplication.translate
        SoftwareOptionen.setWindowTitle(_translate("SoftwareOptionen", "Software Optionen"))
        self.WarmUpAmplifierCheckBox.setText(_translate("SoftwareOptionen", "Warm-up Verstärker"))
        self.AmplifierDeaktivierungLabel.setText(
            _translate("SoftwareOptionen", "Verstärker deaktivieren, während der Signalgenerator deaktiviert ist."))
        self.MaximalIterationCheckBox.setText(_translate("SoftwareOptionen",
                                                         "Wenn die maximale Iteration erreicht ist, wird sie automatisch akzeptiert und fortgefahren."))
        self.MaximalLaufwerkstufeCheckBox.setText(_translate("SoftwareOptionen",
                                                             "Wenn die maximale Laufwerksstufe erreicht ist, wird sie automatisch akzeptiert und fortgefahren."))
        self.WarmUpAmplifierLineEdit.setText(_translate("SoftwareOptionen", "15 Minuten"))
        self.MaximalIterationLineEdit.setText(_translate("SoftwareOptionen", "24"))
        self.WarmUpAmplifierLabel.setText(_translate("SoftwareOptionen", "Zeit für den Verstärker zum Warm-up:"))
        self.MaximalIterationLabel.setText(
            _translate("SoftwareOptionen", "Maximale Iteration der Nivellierungsschleife:"))
        self.OptionTabWidget.setTabText(self.OptionTabWidget.indexOf(self.DuringTest),
                                        _translate("SoftwareOptionen", "Während des Tests"))
        self.DelaysToolButton.setText(_translate("SoftwareOptionen", "Standardwerte"))
        self.DelaysLabel_10.setText(_translate("SoftwareOptionen", "Nach dem Zurücksetzen des EUT:"))
        self.DelaysLabel_7.setText(_translate("SoftwareOptionen", "Vor der aktuellen Monitormessung:"))
        self.DelaysLabel_5.setText(_translate("SoftwareOptionen", "Vor der Feldmonitormessung:"))
        self.DelaysLineEdit_5.setText(_translate("SoftwareOptionen", "0ms"))
        self.DelaysLineEdit_8.setText(_translate("SoftwareOptionen", "0ms"))
        self.DelaysLabel_4.setText(_translate("SoftwareOptionen", "Vor der Rückwärtsleistungsmessung:"))
        self.DelaysLineEdit_10.setText(_translate("SoftwareOptionen", "500ms"))
        self.DelaysLineEdit_4.setText(_translate("SoftwareOptionen", "0ms"))
        self.DelaysLabel_9.setText(_translate("SoftwareOptionen", "Nach dem Wechsel des HF-Schalters CI00402:"))
        self.DelaysLineEdit_9.setText(_translate("SoftwareOptionen", "0ms"))
        self.DelaysLabel_2.setText(_translate("SoftwareOptionen", "*Nach der Änderung des Signalgenerators:"))
        self.DelaysLineEdit_2.setText(_translate("SoftwareOptionen", "250ms"))
        self.DelaysLabel_3.setText(_translate("SoftwareOptionen", "Vor der Vorwärtsleistungsmessung:"))
        self.DelaysLineEdit_6.setText(_translate("SoftwareOptionen", "250ms"))
        self.DelaysLabel_8.setText(_translate("SoftwareOptionen", "Vor der Messung der Kalibriervorrichtung:"))
        self.DelaysLabel_11.setText(_translate("SoftwareOptionen",
                                               "*Warnung: Die Verringerung dieser Verzögerungen kann zu einer Instabilität der Messung führen."))
        self.DelaysLineEdit_7.setText(_translate("SoftwareOptionen", "0ms"))
        self.DelaysLineEdit_3.setText(_translate("SoftwareOptionen", "0ms"))
        self.DelaysLabel_6.setText(_translate("SoftwareOptionen", "Nach der Änderung des Vorverstärkerzustands:"))
        self.DelaysLineEdit_1.setText(_translate("SoftwareOptionen", "1000ms"))
        self.DelaysLabel_1.setText(_translate("SoftwareOptionen", "*Nach der Änderung des HF-Zustands:"))
        self.OptionTabWidget.setTabText(self.OptionTabWidget.indexOf(self.delays),
                                        _translate("SoftwareOptionen", "Verzögerungen"))
        self.SecurityCheckBox_1.setText(_translate("SoftwareOptionen",
                                                   "Informationen zum automatischen Vervollständigen vom Text beim Beenden löschen."))
        self.SecurityCheckBox_2.setText(_translate("SoftwareOptionen", "Sicherheit aktivieren:"))
        self.SecurityLineEdit.setText(_translate("SoftwareOptionen", "deaktiviert"))
        self.SecurityToolButton_1.setText(_translate("SoftwareOptionen", "Einloggen"))
        self.SecurityToolButton_2.setText(_translate("SoftwareOptionen", "Passwort ändern"))
        self.SecurityToolButton_3.setText(_translate("SoftwareOptionen", "Passwort löschen"))
        self.OptionTabWidget.setTabText(self.OptionTabWidget.indexOf(self.Security),
                                        _translate("SoftwareOptionen", "Sicherheit"))
        self.EUTLabel.setText(_translate("SoftwareOptionen",
                                         "Wenn die maximale Aktuellbegrenzung erreicht wird, während der Schwellenwert"))
        self.EUTComboBox.setCurrentText(_translate("SoftwareOptionen", "Prompt Benutzer"))
        self.EUTCheckBox.setText(_translate("SoftwareOptionen",
                                            "Warnen, wenn das EUT nicht zurückgesetzt werden kann, nachdem ein Fehler erkannt wurde."))
        self.OptionTabWidget.setTabText(self.OptionTabWidget.indexOf(self.tab_5),
                                        _translate("SoftwareOptionen", "EUT Überwachung"))
        self.OptionTabWidget.setTabText(self.OptionTabWidget.indexOf(self.tab_6),
                                        _translate("SoftwareOptionen", "Aktualisierung"))
        self.HilfeToolButton.setText(_translate("SoftwareOptionen", "  Hilfe"))
        self.AnwendungPushButton.setText(_translate("SoftwareOptionen", "Anwenden"))
        self.StornierenPushButton.setText(_translate("SoftwareOptionen", "Stornieren"))

    # open the "Erstellung des Administratorpasswortes" window by clicking the "Sicherheit aktivieren" CheckBox on the
    # "Software Optionen" window
    def Creation_password_open(self):
        if self.SecurityCheckBox_2.isChecked():
            widget = QtWidgets.QDialog()
            ui = Ui_PasswordWindow()
            ui.setupUi(widget)
            widget.exec_()

    # open the "help document" of the software by clicking the "Hilfe" button on this window.
    # But the hel document is not written yet. So if users click this button, a information messageBox will show up
    # and say: "The help document is not finished yet, please wait"
    def help_doc(self):
        messageBox = QtWidgets.QMessageBox()
        messageBox.setWindowTitle('Hinweis')
        messageBox.setIcon(QtWidgets.QMessageBox.Information)
        messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/22.png'))
        messageBox.setText('Das Hilfedokument wird bald verfasst.')
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
        buttonY.setText('Ok')
        messageBox.exec_()

    # information messageBox for telling users that the function of "Standardwerte" is not implemented.
    def function_info(self):
        messageBox = QtWidgets.QMessageBox()
        messageBox.setWindowTitle('Hinweis')
        messageBox.setIcon(QtWidgets.QMessageBox.Information)
        messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/22.png'))
        messageBox.setText('Diese Funtionalität ist noch nicht implementiert.')
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
        buttonY.setText('Ok')
        messageBox.exec_()


# This class defines the "Erstellung des Administratorpasswortes" window, which is used for setting administrator password for this software.
# The functions are not completed and activated.
# It's Qt-Designer file is "CreatAdministratorPassword.ui" in folder "uifiles"
# This window can be opend by clicking "Sicherheit -> Aktivieren" in the menu bar of the MainWindow
class Ui_PasswordWindow(object):
    def setupUi(self, PasswordWindow):
        PasswordWindow.setObjectName("PasswordWindow")
        PasswordWindow.setWindowModality(QtCore.Qt.NonModal)
        PasswordWindow.resize(640, 256)
        PasswordWindow.setMinimumSize(QtCore.QSize(640, 256))
        PasswordWindow.setMaximumSize(QtCore.QSize(640, 256))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        PasswordWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon_materials/23.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        PasswordWindow.setWindowIcon(icon)
        PasswordWindow.setModal(True)

        self.PasswordLabel = QtWidgets.QLabel(PasswordWindow)
        self.PasswordLabel.setGeometry(QtCore.QRect(40, 80, 151, 31))
        self.PasswordLabel.setMinimumSize(QtCore.QSize(151, 31))
        self.PasswordLabel.setMaximumSize(QtCore.QSize(151, 31))
        self.PasswordLabel.setObjectName("PasswordLabel")

        self.passwordRepeatLabel = QtWidgets.QLabel(PasswordWindow)
        self.passwordRepeatLabel.setGeometry(QtCore.QRect(40, 130, 231, 31))
        self.passwordRepeatLabel.setMinimumSize(QtCore.QSize(231, 31))
        self.passwordRepeatLabel.setMaximumSize(QtCore.QSize(231, 31))
        self.passwordRepeatLabel.setObjectName("passwordRepeatLabel")

        self.PasswordRepeatlineEdit = QtWidgets.QLineEdit(PasswordWindow)
        self.PasswordRepeatlineEdit.setGeometry(QtCore.QRect(320, 130, 281, 31))
        self.PasswordRepeatlineEdit.setMinimumSize(QtCore.QSize(281, 31))
        self.PasswordRepeatlineEdit.setMaximumSize(QtCore.QSize(281, 31))
        self.PasswordRepeatlineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PasswordRepeatlineEdit.setMaxLength(20)
        self.PasswordRepeatlineEdit.setObjectName("PasswordRepeatlineEdit")

        self.PasswordLineedit = QtWidgets.QLineEdit(PasswordWindow)
        self.PasswordLineedit.setGeometry(QtCore.QRect(320, 80, 281, 31))
        self.PasswordLineedit.setMinimumSize(QtCore.QSize(281, 31))
        self.PasswordLineedit.setMaximumSize(QtCore.QSize(281, 31))
        self.PasswordLineedit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PasswordLineedit.setMaxLength(20)
        self.PasswordLineedit.setObjectName("PasswordLineedit")

        self.ShowTextcheckBox = QtWidgets.QCheckBox(PasswordWindow)
        self.ShowTextcheckBox.setGeometry(QtCore.QRect(40, 200, 131, 31))
        self.ShowTextcheckBox.setMinimumSize(QtCore.QSize(131, 31))
        self.ShowTextcheckBox.setMaximumSize(QtCore.QSize(131, 31))
        self.ShowTextcheckBox.setObjectName("ShowTextcheckBox")

        self.OKpushButton = QtWidgets.QPushButton(PasswordWindow)
        self.OKpushButton.setGeometry(QtCore.QRect(320, 200, 131, 31))
        self.OKpushButton.setMinimumSize(QtCore.QSize(131, 31))
        self.OKpushButton.setMaximumSize(QtCore.QSize(131, 31))
        self.OKpushButton.setDefault(True)
        self.OKpushButton.setObjectName("OKpushButton")

        self.CancelpushButton = QtWidgets.QPushButton(PasswordWindow)
        self.CancelpushButton.setGeometry(QtCore.QRect(470, 200, 131, 31))
        self.CancelpushButton.setMinimumSize(QtCore.QSize(131, 31))
        self.CancelpushButton.setMaximumSize(QtCore.QSize(131, 31))
        self.CancelpushButton.setObjectName("CancelpushButton")

        self.retranslateUi(PasswordWindow)
        QtCore.QMetaObject.connectSlotsByName(PasswordWindow)
        # Definition of the signals
        self.CancelpushButton.clicked['bool'].connect(PasswordWindow.close)
        self.OKpushButton.clicked.connect(self.function_warning)
        self.ShowTextcheckBox.clicked.connect(self.showtext)

        # Setting up the background color of this window
        pale = QtGui.QPalette()
        pale.setColor(QtGui.QPalette.Background, QtGui.QColor(248, 248, 248))
        PasswordWindow.setPalette(pale)

    def retranslateUi(self, PasswordWindow):
        _translate = QtCore.QCoreApplication.translate
        PasswordWindow.setWindowTitle(_translate("PasswordWindow", "Erstellung des Administratorpasswortes"))
        self.PasswordLabel.setText(_translate("PasswordWindow", "Neues Passwort:"))
        self.passwordRepeatLabel.setText(_translate("PasswordWindow", "Passwort wiederholen:"))
        self.ShowTextcheckBox.setText(_translate("PasswordWindow", "Text zeigen."))
        self.OKpushButton.setText(_translate("PasswordWindow", "Anwenden"))
        self.CancelpushButton.setText(_translate("PasswordWindow", "Stornieren"))

    # if users click the "Ok" button on this window, a warning messageBox will show up and tell: "The functionality
    # of this window is not finished yet."
    def function_warning(self):
        messageBox = QtWidgets.QMessageBox()
        messageBox.setWindowTitle('Hinweis')
        messageBox.setIcon(QtWidgets.QMessageBox.Information)
        messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/23.png'))
        messageBox.setText('Diese Funktionalität ist noch nicht implementiert!')
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
        buttonY.setText('Ok')
        messageBox.exec_()

    # if the "Text zeigen" CheckBox is checked, the covered password will show up.
    # if teh "Text zeigen" CheckBox is not checked, the password can not be seen.
    def showtext(self):
        if self.ShowTextcheckBox.isChecked():
            self.PasswordLineedit.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.PasswordRepeatlineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.PasswordLineedit.setEchoMode(QtWidgets.QLineEdit.Password)
            self.PasswordRepeatlineEdit.setEchoMode(QtWidgets.QLineEdit.Password)


# This class defines the "EMV-Prüfung Konfiguration" window, which is the MainWindow.
# It's Qt-Designer files are "MainWindow_neu.ui", "MainWindow.ui", "GestrahltEmission.ui" in folder "uifiles"
# Until now, only the test mode "Feldgebundene Emissionsmessung" is defined
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1401, 792)
        MainWindow.setMinimumSize(QtCore.QSize(1401, 792))
        MainWindow.setMaximumSize(QtCore.QSize(1401, 792))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon_materials/8.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Definition of the antenne factors and kabeldämpfungen
        self.anntef = []
        self.anntem = []
        self.kabelf1 = []
        self.kabelm1 = []
        self.kabelf2 = []
        self.kabelm2 = []

        self.LeistungsgebundeneEmissionMode = QtWidgets.QToolButton(self.centralwidget)
        self.LeistungsgebundeneEmissionMode.setGeometry(QtCore.QRect(250, 140, 220, 220))
        self.LeistungsgebundeneEmissionMode.setMinimumSize(QtCore.QSize(220, 220))
        self.LeistungsgebundeneEmissionMode.setMaximumSize(QtCore.QSize(220, 220))
        self.LeistungsgebundeneEmissionMode.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon_materials/1.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.LeistungsgebundeneEmissionMode.setIcon(icon1)
        self.LeistungsgebundeneEmissionMode.setIconSize(QtCore.QSize(220, 220))
        self.LeistungsgebundeneEmissionMode.setAutoRaise(True)
        self.LeistungsgebundeneEmissionMode.setObjectName("LeistungsgebundeneEmissionMode")

        self.LeitungsgebundenStoerfestigkeitMode = QtWidgets.QToolButton(self.centralwidget)
        self.LeitungsgebundenStoerfestigkeitMode.setGeometry(QtCore.QRect(940, 140, 220, 220))
        self.LeitungsgebundenStoerfestigkeitMode.setMinimumSize(QtCore.QSize(220, 220))
        self.LeitungsgebundenStoerfestigkeitMode.setMaximumSize(QtCore.QSize(220, 220))
        self.LeitungsgebundenStoerfestigkeitMode.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icon_materials/2.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.LeitungsgebundenStoerfestigkeitMode.setIcon(icon1)
        self.LeitungsgebundenStoerfestigkeitMode.setIconSize(QtCore.QSize(220, 220))
        self.LeitungsgebundenStoerfestigkeitMode.setAutoRaise(True)
        self.LeitungsgebundenStoerfestigkeitMode.setObjectName("LeitungsgebundenStoerfestigkeitMode")

        self.VerticalLine = QtWidgets.QFrame(self.centralwidget)
        self.VerticalLine.setGeometry(QtCore.QRect(690, 190, 21, 480))
        self.VerticalLine.setMinimumSize(QtCore.QSize(21, 480))
        self.VerticalLine.setMaximumSize(QtCore.QSize(21, 480))
        self.VerticalLine.setFrameShadow(QtWidgets.QFrame.Plain)
        self.VerticalLine.setLineWidth(3)
        self.VerticalLine.setFrameShape(QtWidgets.QFrame.VLine)
        self.VerticalLine.setStyleSheet("color:rgb({},{},{},255)".format(190, 222, 240))
        self.VerticalLine.setObjectName("VerticalLine")

        self.PleaseChoose = QtWidgets.QLabel(self.centralwidget)
        self.PleaseChoose.setGeometry(QtCore.QRect(490, 40, 411, 41))
        self.PleaseChoose.setMinimumSize(QtCore.QSize(411, 41))
        self.PleaseChoose.setMaximumSize(QtCore.QSize(411, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.PleaseChoose.setFont(font)
        self.PleaseChoose.setStyleSheet("color:rgb({},{},{},255)".format(31, 78, 121))
        self.PleaseChoose.setObjectName("PleaseChoose")

        self.EmissionsmessungLabel = QtWidgets.QLabel(self.centralwidget)
        self.EmissionsmessungLabel.setGeometry(QtCore.QRect(220, 80, 291, 61))
        self.EmissionsmessungLabel.setMinimumSize(QtCore.QSize(291, 61))
        self.EmissionsmessungLabel.setMaximumSize(QtCore.QSize(291, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.EmissionsmessungLabel.setFont(font)
        self.EmissionsmessungLabel.setStyleSheet("color:rgb({},{},{},255)".format(0, 32, 96))
        self.EmissionsmessungLabel.setObjectName("EmissionsmessungLabel")

        self.StoerfestigkeitLabel = QtWidgets.QLabel(self.centralwidget)
        self.StoerfestigkeitLabel.setGeometry(QtCore.QRect(880, 80, 341, 61))
        self.StoerfestigkeitLabel.setMinimumSize(QtCore.QSize(341, 61))
        self.StoerfestigkeitLabel.setMaximumSize(QtCore.QSize(341, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.StoerfestigkeitLabel.setFont(font)
        self.StoerfestigkeitLabel.setStyleSheet("color:rgb({},{},{},255)".format(0, 32, 96))
        self.StoerfestigkeitLabel.setObjectName("StoerfestigkeitLabel")

        self.FeldgebundenEmissionMode = QtWidgets.QToolButton(self.centralwidget)
        self.FeldgebundenEmissionMode.setGeometry(QtCore.QRect(250, 450, 220, 220))
        self.FeldgebundenEmissionMode.setMinimumSize(QtCore.QSize(220, 220))
        self.FeldgebundenEmissionMode.setMaximumSize(QtCore.QSize(220, 220))
        self.FeldgebundenEmissionMode.setText("")
        self.FeldgebundenEmissionMode.setIcon(icon2)
        self.FeldgebundenEmissionMode.setIconSize(QtCore.QSize(220, 220))
        self.FeldgebundenEmissionMode.setAutoRaise(True)
        self.FeldgebundenEmissionMode.setObjectName("FeldgebundenEmissionMode")

        self.FeldgebundenStoerfestigkeitMode = QtWidgets.QToolButton(self.centralwidget)
        self.FeldgebundenStoerfestigkeitMode.setGeometry(QtCore.QRect(940, 450, 220, 220))
        self.FeldgebundenStoerfestigkeitMode.setMinimumSize(QtCore.QSize(220, 220))
        self.FeldgebundenStoerfestigkeitMode.setMaximumSize(QtCore.QSize(220, 220))
        self.FeldgebundenStoerfestigkeitMode.setText("")
        self.FeldgebundenStoerfestigkeitMode.setIcon(icon2)
        self.FeldgebundenStoerfestigkeitMode.setIconSize(QtCore.QSize(220, 220))
        self.FeldgebundenStoerfestigkeitMode.setAutoRaise(True)
        self.FeldgebundenStoerfestigkeitMode.setObjectName("FeldgebundenStoerfestigkeitMode")

        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(220, 410, 960, 21))
        self.line.setMinimumSize(QtCore.QSize(960, 21))
        self.line.setMaximumSize(QtCore.QSize(960, 21))
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(3)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setStyleSheet("color:rgb({},{},{},255)".format(190, 222, 240))
        self.line.setObjectName("line")

        self.LeistungsgebundeneEmissionModeLabel = QtWidgets.QLabel(self.centralwidget)
        self.LeistungsgebundeneEmissionModeLabel.setGeometry(QtCore.QRect(270, 360, 191, 31))
        self.LeistungsgebundeneEmissionModeLabel.setMinimumSize(QtCore.QSize(191, 31))
        self.LeistungsgebundeneEmissionModeLabel.setMaximumSize(QtCore.QSize(191, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.LeistungsgebundeneEmissionModeLabel.setFont(font)
        self.LeistungsgebundeneEmissionModeLabel.setStyleSheet("color:rgb({},{},{},255)".format(0, 32, 96))
        self.LeistungsgebundeneEmissionModeLabel.setObjectName("LeistungsgebundeneEmissionModeLabel")

        self.FeldgebundenEmissionModeLabel = QtWidgets.QLabel(self.centralwidget)
        self.FeldgebundenEmissionModeLabel.setGeometry(QtCore.QRect(290, 680, 141, 31))
        self.FeldgebundenEmissionModeLabel.setMinimumSize(QtCore.QSize(141, 31))
        self.FeldgebundenEmissionModeLabel.setMaximumSize(QtCore.QSize(141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.FeldgebundenEmissionModeLabel.setFont(font)
        self.FeldgebundenEmissionModeLabel.setStyleSheet("color:rgb({},{},{},255)".format(0, 32, 96))
        self.FeldgebundenEmissionModeLabel.setObjectName("FeldgebundenEmissionModeLabel")

        self.LeitungsgebundenStoerfestigkeitModeLabel = QtWidgets.QLabel(self.centralwidget)
        self.LeitungsgebundenStoerfestigkeitModeLabel.setGeometry(QtCore.QRect(960, 360, 191, 31))
        self.LeitungsgebundenStoerfestigkeitModeLabel.setMinimumSize(QtCore.QSize(191, 31))
        self.LeitungsgebundenStoerfestigkeitModeLabel.setMaximumSize(QtCore.QSize(191, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.LeitungsgebundenStoerfestigkeitModeLabel.setFont(font)
        self.LeitungsgebundenStoerfestigkeitModeLabel.setStyleSheet("color:rgb({},{},{},255)".format(0, 32, 96))
        self.LeitungsgebundenStoerfestigkeitModeLabel.setObjectName("LeitungsgebundenStoerfestigkeitModeLabel")

        self.FeldgebundenStoerfestigkeitModeLabel = QtWidgets.QLabel(self.centralwidget)
        self.FeldgebundenStoerfestigkeitModeLabel.setGeometry(QtCore.QRect(985, 680, 141, 31))
        self.FeldgebundenStoerfestigkeitModeLabel.setMinimumSize(QtCore.QSize(141, 31))
        self.FeldgebundenStoerfestigkeitModeLabel.setMaximumSize(QtCore.QSize(141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.FeldgebundenStoerfestigkeitModeLabel.setFont(font)
        self.FeldgebundenStoerfestigkeitModeLabel.setStyleSheet("color:rgb({},{},{},255)".format(0, 32, 96))
        self.FeldgebundenStoerfestigkeitModeLabel.setObjectName("FeldgebundenStoerfestigkeitModeLabel")

        ''' from this line, the code is for the test mode 'Feldgebundene Emissionsmessung'. '''
        self.EquipmentSettingButton = QtWidgets.QToolButton(self.centralwidget)
        self.EquipmentSettingButton.setGeometry(QtCore.QRect(110, 510, 150, 150))
        self.EquipmentSettingButton.setMinimumSize(QtCore.QSize(150, 150))
        self.EquipmentSettingButton.setMaximumSize(QtCore.QSize(150, 150))
        self.EquipmentSettingButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon_materials/3.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.EquipmentSettingButton.setIcon(icon1)
        self.EquipmentSettingButton.setIconSize(QtCore.QSize(120, 120))
        self.EquipmentSettingButton.setAutoRaise(True)
        self.EquipmentSettingButton.setObjectName("EquipmentSettingButton")
        self.EquipmentSettingButton.hide()

        self.TestSettingButton = QtWidgets.QToolButton(self.centralwidget)
        self.TestSettingButton.setGeometry(QtCore.QRect(370, 510, 150, 150))
        self.TestSettingButton.setMinimumSize(QtCore.QSize(150, 150))
        self.TestSettingButton.setMaximumSize(QtCore.QSize(150, 150))
        self.TestSettingButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icon_materials/4.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.TestSettingButton.setIcon(icon2)
        self.TestSettingButton.setIconSize(QtCore.QSize(150, 150))
        self.TestSettingButton.setAutoRaise(True)
        self.TestSettingButton.setObjectName("TestSettingButton")
        self.TestSettingButton.hide()

        self.CalibrationButton = QtWidgets.QToolButton(self.centralwidget)
        self.CalibrationButton.setGeometry(QtCore.QRect(630, 510, 150, 150))
        self.CalibrationButton.setMinimumSize(QtCore.QSize(150, 150))
        self.CalibrationButton.setMaximumSize(QtCore.QSize(150, 150))
        self.CalibrationButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icon_materials/5.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.CalibrationButton.setIcon(icon3)
        self.CalibrationButton.setIconSize(QtCore.QSize(150, 150))
        self.CalibrationButton.setAutoRaise(True)
        self.CalibrationButton.setObjectName("CalibrationButton")
        self.CalibrationButton.hide()

        self.TestStartButton = QtWidgets.QToolButton(self.centralwidget)
        self.TestStartButton.setGeometry(QtCore.QRect(1150, 510, 150, 150))
        self.TestStartButton.setMinimumSize(QtCore.QSize(150, 150))
        self.TestStartButton.setMaximumSize(QtCore.QSize(150, 150))
        self.TestStartButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icon_materials/7.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.TestStartButton.setIcon(icon4)
        self.TestStartButton.setIconSize(QtCore.QSize(150, 150))
        self.TestStartButton.setAutoRaise(True)
        self.TestStartButton.setObjectName("TestStartButton")
        self.TestStartButton.hide()

        self.ReportButton = QtWidgets.QToolButton(self.centralwidget)
        self.ReportButton.setGeometry(QtCore.QRect(890, 510, 150, 150))
        self.ReportButton.setMinimumSize(QtCore.QSize(150, 150))
        self.ReportButton.setMaximumSize(QtCore.QSize(150, 150))
        self.ReportButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icon_materials/6.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.ReportButton.setIcon(icon5)
        self.ReportButton.setIconSize(QtCore.QSize(150, 150))
        self.ReportButton.setAutoRaise(True)
        self.ReportButton.setObjectName("ReportButton")
        self.ReportButton.hide()

        self.EquipmentSettingLabel = QtWidgets.QLabel(self.centralwidget)
        self.EquipmentSettingLabel.setGeometry(QtCore.QRect(70, 680, 235, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.EquipmentSettingLabel.setFont(font)
        self.EquipmentSettingLabel.setStyleSheet("color:rgb({},{},{},255)".format(0, 32, 96))
        self.EquipmentSettingLabel.setObjectName("EquipmentSettingLabel")
        self.EquipmentSettingLabel.hide()

        self.TestSettingLabel = QtWidgets.QLabel(self.centralwidget)
        self.TestSettingLabel.setGeometry(QtCore.QRect(330, 680, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.TestSettingLabel.setFont(font)
        self.TestSettingLabel.setStyleSheet("color:rgb({},{},{},255)".format(0, 32, 96))
        self.TestSettingLabel.setObjectName("TestSettingLabel")
        self.TestSettingLabel.hide()

        self.CalibrationLabel = QtWidgets.QLabel(self.centralwidget)
        self.CalibrationLabel.setGeometry(QtCore.QRect(640, 680, 150, 41))
        self.CalibrationLabel.setMinimumSize(QtCore.QSize(150, 41))
        self.CalibrationLabel.setMaximumSize(QtCore.QSize(150, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.CalibrationLabel.setFont(font)
        self.CalibrationLabel.setStyleSheet("color:rgb({},{},{},255)".format(0, 32, 96))
        self.CalibrationLabel.setObjectName("CalibrationLabel")
        self.CalibrationLabel.hide()

        self.ReportLabel = QtWidgets.QLabel(self.centralwidget)
        self.ReportLabel.setGeometry(QtCore.QRect(920, 680, 91, 41))
        self.ReportLabel.setMinimumSize(QtCore.QSize(91, 41))
        self.ReportLabel.setMaximumSize(QtCore.QSize(91, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.ReportLabel.setFont(font)
        self.ReportLabel.setStyleSheet("color:rgb({},{},{},255)".format(0, 32, 96))
        self.ReportLabel.setObjectName("ReportLabel")
        self.ReportLabel.hide()

        self.TestLabel = QtWidgets.QLabel(self.centralwidget)
        self.TestLabel.setGeometry(QtCore.QRect(1200, 680, 51, 41))
        self.TestLabel.setMinimumSize(QtCore.QSize(51, 41))
        self.TestLabel.setMaximumSize(QtCore.QSize(51, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.TestLabel.setFont(font)
        self.TestLabel.setStyleSheet("color:rgb({},{},{},255)".format(0, 32, 96))
        self.TestLabel.setObjectName("TestLabel")
        self.TestLabel.hide()

        self.UniLogoLabel = QtWidgets.QLabel(self.centralwidget)
        self.UniLogoLabel.setGeometry(QtCore.QRect(80, 30, 281, 91))
        self.UniLogoLabel.setText("")
        self.UniLogoLabel.setObjectName("UniLogoLabel")
        self.UniLogoLabel.hide()

        self.IEHLogoLabel = QtWidgets.QLabel(self.centralwidget)
        self.IEHLogoLabel.setGeometry(QtCore.QRect(555, 20, 782, 131))
        self.IEHLogoLabel.setText("")
        self.IEHLogoLabel.setObjectName("IEHLogoLabel")
        self.IEHLogoLabel.hide()

        self.GestrahltEmissionBack = QtWidgets.QToolButton(self.centralwidget)
        self.GestrahltEmissionBack.setGeometry(QtCore.QRect(1310, 130, 41, 41))
        self.GestrahltEmissionBack.setMinimumSize(QtCore.QSize(41, 41))
        self.GestrahltEmissionBack.setMaximumSize(QtCore.QSize(41, 41))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icon_materials/34.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.GestrahltEmissionBack.setIcon(icon6)
        self.GestrahltEmissionBack.setIconSize(QtCore.QSize(41, 41))
        self.GestrahltEmissionBack.setObjectName("GestrahltEmissionBack")
        self.GestrahltEmissionBack.setAutoRaise(True)
        self.GestrahltEmissionBack.hide()

        self.NormGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.NormGroupBox.setEnabled(True)
        self.NormGroupBox.setGeometry(QtCore.QRect(50, 160, 1301, 341))
        self.NormGroupBox.setMinimumSize(QtCore.QSize(1301, 341))
        self.NormGroupBox.setMaximumSize(QtCore.QSize(1301, 341))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.NormGroupBox.setFont(font)
        self.NormGroupBox.setAcceptDrops(True)
        self.NormGroupBox.setStyleSheet("color:rgb({},{},{},255)".format(31, 78, 121))
        self.NormGroupBox.setObjectName("NormGroupBox")
        self.NormGroupBox.hide()

        self.NormDescription = QtWidgets.QListWidget(self.NormGroupBox)
        self.NormDescription.setSelectionMode(2)
        self.NormDescription.setGeometry(QtCore.QRect(810, 30, 471, 291))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.NormDescription.setFont(font)
        self.NormDescription.setObjectName("NormDescription")
        self.NormDescription.hide()

        self.NormList = QtWidgets.QListWidget(self.NormGroupBox)
        self.NormList.setGeometry(QtCore.QRect(20, 30, 481, 291))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.NormList.setFont(font)
        self.NormList.setObjectName("NormList")
        item = QtWidgets.QListWidgetItem()
        self.NormList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.NormList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.NormList.addItem(item)
        # neu
        item = QtWidgets.QListWidgetItem()  # Neue Norm hinzufügen
        self.NormList.addItem(item)
        # neu
        self.NormList.setCurrentItem(self.NormList.item(0))
        self.NormList.hide()

        self.NormChooseButton = QtWidgets.QToolButton(self.NormGroupBox)
        self.NormChooseButton.setGeometry(QtCore.QRect(590, 100, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.NormChooseButton.setFont(font)
        self.NormChooseButton.setObjectName("NormChooseButton")
        self.NormChooseButton.hide()

        self.NormAddButton = QtWidgets.QToolButton(self.NormGroupBox)
        self.NormAddButton.setGeometry(QtCore.QRect(590, 210, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.NormAddButton.setFont(font)
        self.NormAddButton.setObjectName("NormAddButton")
        self.NormAddButton.hide()

        self.NormGroupBox.raise_()
        self.VerticalLine.raise_()
        self.PleaseChoose.raise_()
        self.EquipmentSettingButton.raise_()
        self.TestSettingButton.raise_()
        self.CalibrationButton.raise_()
        self.TestStartButton.raise_()
        self.ReportButton.raise_()
        self.EquipmentSettingLabel.raise_()
        self.TestSettingLabel.raise_()
        self.CalibrationLabel.raise_()
        self.ReportLabel.raise_()
        self.TestLabel.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        """ from this line, the codes are for the elements(options) in the menu bar."""
        # activate the menubar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1401, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        # Menu bar -> Datei-> Schließen
        exitAction = QtWidgets.QAction('&Schließen', self)
        exitAction.setStatusTip('Software schließen.')
        exitAction.triggered.connect(QtWidgets.qApp.quit)

        # Menu bar -> Einstellen -> Optionen
        enstellenAction = QtWidgets.QAction('&Optionen', self)
        enstellenAction.setStatusTip('Optionen für die software einstellen.')
        enstellenAction.triggered.connect(self.opensoftwareoptions)

        # Menu bar -> Sicherheit -> Aktivieren
        securityAction = QtWidgets.QAction('&Aktivieren', self)
        securityAction.setStatusTip('Administratorpasswort erstellen.')
        securityAction.triggered.connect(self.openministratorpassword)

        # Menu bar -> Hilfe -> Hilfedatei öffnen
        helpFileAction = QtWidgets.QAction('Hilfedatei öffnen', self)
        helpFileAction.setStatusTip('Hilfedatei öffnen.')
        helpFileAction.triggered.connect(self.hepl_document)

        # Menu bar -> Hilfe -> Über
        AboutAction = QtWidgets.QAction('Über...', self)
        AboutAction.setStatusTip('Versionsinformationen der Software.')
        AboutAction.triggered.connect(self.version_info)

        # implementation of all defined elements(options) in menu bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        fileMenu = self.menubar.addMenu('&Datei')
        fileMenu.addAction(exitAction)
        einstellen = self.menubar.addMenu('&Einstellen')
        einstellen.addAction(enstellenAction)
        security = self.menubar.addMenu('&Sicherheit')
        security.addAction(securityAction)
        help = self.menubar.addMenu('&Hilfe')
        help.addAction(helpFileAction)
        help.addAction(AboutAction)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # definition of signals
        self.LeistungsgebundeneEmissionMode.clicked.connect(self.LeistungsgebundeneEmission)
        self.LeitungsgebundenStoerfestigkeitMode.clicked.connect(self.LeitungsgebundenStoerfestigkeit)
        self.FeldgebundenEmissionMode.clicked.connect(self.FeldgebundenEmission)
        self.FeldgebundenStoerfestigkeitMode.clicked.connect(self.FeldgebundenStoerfestigkeit)
        self.GestrahltEmissionBack.clicked.connect(self.go_back_anfang)
        self.CalibrationButton.clicked.connect(self.calibrationwarning)
        self.NormChooseButton.clicked.connect(self.NormDescribe)
        self.NormList.currentItemChanged.connect(self.clearitems)

        # setting up the background color of the MainWindow
        pale = QtGui.QPalette()
        pale.setColor(QtGui.QPalette.Background, QtGui.QColor(248, 248, 248))
        MainWindow.setPalette(pale)

    choose = 0

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        if self.choose == 1:
            MainWindow.setWindowTitle(_translate("MainWindow", "LE"))
        elif self.choose == 2:
            MainWindow.setWindowTitle(_translate("MainWindow", "FE"))
        elif self.choose == 3:
            MainWindow.setWindowTitle(_translate("MainWindow", "LS"))
        # neu
        elif self.choose == 4:
            MainWindow.setWindowTitle(_translate("MainWindow", "FS"))
        # neu
        elif self.choose == 0:
            MainWindow.setWindowTitle(_translate("MainWindow", "EMV-Prüfsoftware"))

        self.PleaseChoose.setText(_translate("MainWindow", "Bitte wählen Sie einen Test-Modus aus:\n"""))
        self.EmissionsmessungLabel.setText(_translate("MainWindow", "Emissionsmessung"))
        self.StoerfestigkeitLabel.setText(_translate("MainWindow", "Störfestigkeitsprüfung"))
        self.LeistungsgebundeneEmissionModeLabel.setText(_translate("MainWindow", "Leitungsgebunden"))
        self.FeldgebundenEmissionModeLabel.setText(_translate("MainWindow", "Feldgebunden"))
        self.LeitungsgebundenStoerfestigkeitModeLabel.setText(_translate("MainWindow", "Leitungsgebunden"))
        self.FeldgebundenStoerfestigkeitModeLabel.setText(_translate("MainWindow", "Feldgebunden"))
        self.EquipmentSettingLabel.setText(_translate("GestrahlEmmision", "Gerätemanagement"))
        self.TestSettingLabel.setText(_translate("GestrahlEmmision", "Testkonfiguration"))
        self.CalibrationLabel.setText(_translate("GestrahlEmmision", "Kalibrierung"))
        self.ReportLabel.setText(_translate("GestrahlEmmision", "Reports"))
        self.TestLabel.setText(_translate("GestrahlEmmision", "Test"))
        self.NormGroupBox.setTitle(_translate("GestrahlEmmision", "Normen"))
        __sortingEnabled = self.NormList.isSortingEnabled()
        self.NormList.setSortingEnabled(False)
        item = self.NormList.item(0)
        item.setText(_translate("GestrahlEmmision", "CISPR 11: EN 55011"))
        item = self.NormList.item(1)
        item.setText(_translate("GestrahlEmmision", "IEC / EN 61000-4-6"))
        item = self.NormList.item(2)
        item.setText(_translate("GestrahlEmmision", "IEC 61000-6-2"))
        # neu
        item = self.NormList.item(3)
        item.setText(_translate("GestrahlEmmision", "IEC 61000-4-3"))
        # neu
        self.NormList.setSortingEnabled(__sortingEnabled)
        self.NormChooseButton.setText(_translate("GestrahlEmmision", "Auswählen"))
        self.NormAddButton.setText(_translate("GestrahlEmmision", "Hinzufügen"))
        Unilogo = cv.imread("./icon_materials/10.png", -1)
        Unilogo = png_preprocess(Unilogo, 91)
        self.UniLogoLabel.setPixmap(QtGui.QPixmap(Unilogo))
        IEHlogo = cv.imread("./icon_materials/33.png", -1)
        IEHlogo = png_preprocess(IEHlogo, 131)
        self.IEHLogoLabel.setPixmap(QtGui.QPixmap(IEHlogo))

    # if "Menubar -> Hilfe -> Hilfedetei öffnen" is clicked, the help document of the software should show up. But here
    # users get a information messageBox says that the hepl document is not written yet.
    # if the help document is written, then it should be placed here.
    def hepl_document(self):
        messageBox = QtWidgets.QMessageBox()
        messageBox.setWindowTitle('Hinweis')
        messageBox.setIcon(QtWidgets.QMessageBox.Information)
        messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
        messageBox.setText('Das Hilfedokument wird bald verfasst.')
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
        buttonY.setText('Ok')
        messageBox.exec_()

    # in the MainWindow of the test mode "Feldgebundene Emissionsmessung"
    # if users chose a norm, the listView (self.NormDescription) will be cleared at first, then the new marginal
    # values (Grenzwerte) of the chosed norm can be showed in the listView.
    # This function can prevent chaos. e.g. if the marginal values (Grenzwerte) of proviously chosed norm are not cleared, they will
    # be added to the marginal values(Grenzwerte) of the newly chosed norm.
    def clearitems(self):
        self.NormDescription.clear()

    # if "Menu bar -> Hilfe -> Über" is clicked, the version information / icon information(quelle) of the software should show up. But here
    # users get a information messageBox says that the version information / icon information(quelle) is not written yet.
    # if the version information / icon information(quelle) is written, then it should be placed here.
    def version_info(self):
        messageBox = QtWidgets.QMessageBox()
        messageBox.setWindowTitle('Hinweis')
        messageBox.setIcon(QtWidgets.QMessageBox.Information)
        messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
        messageBox.setText('Die Versionsinformationen werden bald eingeführt.')
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
        buttonY.setText('Ok')
        messageBox.exec_()

    # after chosing the test mode "Feldegebundene Emissionsmessung", the relevant widigtes of this test mode should show up
    # and the other non-relevant widgets should be hidden.

    def FeldgebundenEmission(self, MainWindow):
        self.VerticalLine.hide()
        self.PleaseChoose.hide()
        self.EmissionsmessungLabel.hide()
        self.StoerfestigkeitLabel.hide()
        self.line.hide()
        self.FeldgebundenEmissionMode.hide()
        self.FeldgebundenStoerfestigkeitMode.hide()
        self.FeldgebundenEmissionModeLabel.hide()
        self.FeldgebundenStoerfestigkeitModeLabel.hide()
        self.LeistungsgebundeneEmissionMode.hide()
        self.LeitungsgebundenStoerfestigkeitMode.hide()
        self.LeistungsgebundeneEmissionModeLabel.hide()
        self.LeitungsgebundenStoerfestigkeitModeLabel.hide()

        self.choose = 1

        self.EquipmentSettingButton.show()
        self.TestSettingButton.show()
        self.CalibrationButton.show()
        self.TestStartButton.show()
        self.ReportButton.show()
        self.EquipmentSettingLabel.show()
        self.TestSettingLabel.show()
        self.CalibrationLabel.show()
        self.ReportLabel.show()
        self.TestLabel.show()
        self.GestrahltEmissionBack.show()
        self.NormGroupBox.show()
        self.NormDescription.show()
        self.NormList.show()
        self.NormChooseButton.show()
        self.NormAddButton.show()
        self.UniLogoLabel.show()
        self.IEHLogoLabel.show()

    # if the test mode "Leitungsgebundene Emissionsmessung" is chosen, users will recieve an information messageBox
    # says that this test mode is not implemented.
    # once this test mode should be implemented, then show up the relevant widgets here and hide other non-relevant widgets
    # just like the method "def FeldgebundenEmission(self):" in the line 1068
    # FE choose=1, LE choose =2, LS choose=3
    def LeistungsgebundeneEmission(self):
        self.VerticalLine.hide()
        self.PleaseChoose.hide()
        self.EmissionsmessungLabel.hide()
        self.StoerfestigkeitLabel.hide()
        self.line.hide()
        self.FeldgebundenEmissionMode.hide()
        self.FeldgebundenStoerfestigkeitMode.hide()
        self.FeldgebundenEmissionModeLabel.hide()
        self.FeldgebundenStoerfestigkeitModeLabel.hide()
        self.LeistungsgebundeneEmissionMode.hide()
        self.LeitungsgebundenStoerfestigkeitMode.hide()
        self.LeistungsgebundeneEmissionModeLabel.hide()
        self.LeitungsgebundenStoerfestigkeitModeLabel.hide()

        self.choose = 2

        self.EquipmentSettingButton.show()
        self.TestSettingButton.show()
        self.CalibrationButton.show()
        self.TestStartButton.show()
        self.ReportButton.show()
        self.EquipmentSettingLabel.show()
        self.TestSettingLabel.show()
        self.CalibrationLabel.show()
        self.ReportLabel.show()
        self.TestLabel.show()
        self.GestrahltEmissionBack.show()
        self.NormGroupBox.show()
        self.NormDescription.show()
        self.NormList.show()
        self.NormChooseButton.show()
        self.NormAddButton.show()
        self.UniLogoLabel.show()
        self.IEHLogoLabel.show()

    # if the test mode "Leitungsgebundene Störfestigkeit" is chosen, users will recieve an information messageBox
    # says that this test mode is not implemented.
    # once this test mode should be implemented, then show up the relevant widgets here and hide other non-relevant widgets
    # just like the method "def FeldgebundenEmission(self):" in the line 1068
    # choose=3 LS
    def LeitungsgebundenStoerfestigkeit(self):
        self.VerticalLine.hide()
        self.PleaseChoose.hide()
        self.EmissionsmessungLabel.hide()
        self.StoerfestigkeitLabel.hide()
        self.line.hide()
        self.FeldgebundenEmissionMode.hide()
        self.FeldgebundenStoerfestigkeitMode.hide()
        self.FeldgebundenEmissionModeLabel.hide()
        self.FeldgebundenStoerfestigkeitModeLabel.hide()
        self.LeistungsgebundeneEmissionMode.hide()
        self.LeitungsgebundenStoerfestigkeitMode.hide()
        self.LeistungsgebundeneEmissionModeLabel.hide()
        self.LeitungsgebundenStoerfestigkeitModeLabel.hide()

        self.choose = 3

        self.EquipmentSettingButton.show()
        self.TestSettingButton.show()
        self.CalibrationButton.show()
        self.TestStartButton.show()
        self.ReportButton.show()
        self.EquipmentSettingLabel.show()
        self.TestSettingLabel.show()
        self.CalibrationLabel.show()
        self.ReportLabel.show()
        self.TestLabel.show()
        self.GestrahltEmissionBack.show()
        self.NormGroupBox.show()
        self.NormDescription.show()
        self.NormList.show()
        self.NormChooseButton.show()
        self.NormAddButton.show()
        self.UniLogoLabel.show()
        self.IEHLogoLabel.show()

    # if the test mode "Feldgebundene Störfestigkeit" is chosen, users will recieve an information messageBox
    # says that this test mode is not implemented.
    # once this test mode should be implemented, then show up the relevant widgets here and hide other non-relevant widgets
    # just like the method "def FeldgebundenEmission(self):" in the line 1068

    # neu
    def FeldgebundenStoerfestigkeit(self):
        # QtWidgets.QMessageBox.information(self, "Hinweis", "Diese Funktionalität ist noch nicht implementiert.")
        self.VerticalLine.hide()
        self.PleaseChoose.hide()
        self.EmissionsmessungLabel.hide()
        self.StoerfestigkeitLabel.hide()
        self.line.hide()
        self.FeldgebundenEmissionMode.hide()
        self.FeldgebundenStoerfestigkeitMode.hide()
        self.FeldgebundenEmissionModeLabel.hide()
        self.FeldgebundenStoerfestigkeitModeLabel.hide()
        self.LeistungsgebundeneEmissionMode.hide()
        self.LeitungsgebundenStoerfestigkeitMode.hide()
        self.LeistungsgebundeneEmissionModeLabel.hide()
        self.LeitungsgebundenStoerfestigkeitModeLabel.hide()

        self.choose = 4

        self.EquipmentSettingButton.show()
        self.TestSettingButton.show()
        self.CalibrationButton.show()
        self.TestStartButton.show()
        self.ReportButton.show()
        self.EquipmentSettingLabel.show()
        self.TestSettingLabel.show()
        self.CalibrationLabel.show()
        self.ReportLabel.show()
        self.TestLabel.show()
        self.GestrahltEmissionBack.show()
        self.NormGroupBox.show()
        self.NormDescription.show()
        self.NormList.show()
        self.NormChooseButton.show()
        self.NormAddButton.show()
        self.UniLogoLabel.show()
        self.IEHLogoLabel.show()

    # This method is mainly for showing up the marginal values(Grenzwerte) of the chosen norm in listView (self.NormDescription)
    def NormDescribe(self):
        # the same reson as line 1047, the listView should be cleared at first
        self.NormDescription.clear()

        # if the norm "CISPR 11: EN 55011" is chosen, it's marginal values(Grenzwerte) will be showed in listView (self.NormDescription)
        # FE choose=1,LE choose =2, LS choose=3
        if self.NormList.currentItem().text() == 'CISPR 11: EN 55011':
            if self.choose == 1:  # FE choose = 1, LE choose = 2, LS choose = 3, FS choose = 4
                item = QtWidgets.QListWidgetItem()
                self.NormDescription.addItem(item)
                item = QtWidgets.QListWidgetItem()
                item.setBackground(QtGui.QColor(233, 241, 247))
                self.NormDescription.addItem(item)
                item = QtWidgets.QListWidgetItem()
                self.NormDescription.addItem(item)
                item = QtWidgets.QListWidgetItem()
                item.setBackground(QtGui.QColor(233, 241, 247))
                self.NormDescription.addItem(item)
                item = QtWidgets.QListWidgetItem()
                self.NormDescription.addItem(item)
                item = QtWidgets.QListWidgetItem()
                item.setBackground(QtGui.QColor(233, 241, 247))
                self.NormDescription.addItem(item)
                item = QtWidgets.QListWidgetItem()
                self.NormDescription.addItem(item)
                item = QtWidgets.QListWidgetItem()
                item.setBackground(QtGui.QColor(233, 241, 247))
                self.NormDescription.addItem(item)
                item = QtWidgets.QListWidgetItem()
                self.NormDescription.addItem(item)
                item = QtWidgets.QListWidgetItem()
                item.setBackground(QtGui.QColor(233, 241, 247))
                self.NormDescription.addItem(item)
                item = QtWidgets.QListWidgetItem()
                self.NormDescription.addItem(item)
                item = QtWidgets.QListWidgetItem()
                item.setBackground(QtGui.QColor(233, 241, 247))
                self.NormDescription.addItem(item)
                item = QtWidgets.QListWidgetItem()
                self.NormDescription.addItem(item)
                item = QtWidgets.QListWidgetItem()
                item.setBackground(QtGui.QColor(233, 241, 247))
                self.NormDescription.addItem(item)

                item = self.NormDescription.item(0)
                item.setText("Benutzerdefiniert: Kein Gerenzwert.")
                item = self.NormDescription.item(1)
                item.setText("Gruppe 1 (>20kVA). Klasse A. Quasi-Peak. 3m.")
                item = self.NormDescription.item(2)
                item.setText("Gruppe 1 (<=20kVA). Klasse A. Quasi-Peak. 3m.")
                item = self.NormDescription.item(3)
                item.setText("Gruppe 1 (>20kVA). Klasse A. Quasi-Peak. 10m.")
                item = self.NormDescription.item(4)
                item.setText("Gruppe 1 (<=20kVA). Klasse A. Quasi-Peak. 10m.")
                item = self.NormDescription.item(5)
                item.setText("Gruppe 1. Klasse B. Quasi-Peak. 3m.")
                item = self.NormDescription.item(6)
                item.setText("Gruppe 1. Klasse B. Quasi-Peak. 10m.")
                item = self.NormDescription.item(7)
                item.setText("Gruppe 2. Klasse A. Quasi-Peak. 3m.")
                item = self.NormDescription.item(8)
                item.setText("Gruppe 2. Klasse A. Quasi-Peak. 10m.")
                item = self.NormDescription.item(9)
                item.setText("Gruppe 2. Klasse A. Quasi-Peak. 30m.")
                item = self.NormDescription.item(10)
                item.setText("Gruppe 2. Klasse B. Quasi-Peak. 3m.")
                item = self.NormDescription.item(11)
                item.setText("Gruppe 2. Klasse B. Average. 3m.")
                item = self.NormDescription.item(12)
                item.setText("Gruppe 2. Klasse B. Quasi-Peak. 10m.")
                item = self.NormDescription.item(13)
                item.setText("Gruppe 2. Klasse B. Average. 10m.")
            elif self.choose == 2:  # FE choose=1,LE choose =2, LS choose=3
                item = QtWidgets.QListWidgetItem()
                self.NormDescription.addItem(item)
                item = QtWidgets.QListWidgetItem()
                item.setBackground(QtGui.QColor(233, 241, 247))
                self.NormDescription.addItem(item)
                item = QtWidgets.QListWidgetItem()
                self.NormDescription.addItem(item)
                item = QtWidgets.QListWidgetItem()
                item.setBackground(QtGui.QColor(233, 241, 247))
                self.NormDescription.addItem(item)
                item = QtWidgets.QListWidgetItem()
                self.NormDescription.addItem(item)
                item = QtWidgets.QListWidgetItem()
                item.setBackground(QtGui.QColor(233, 241, 247))
                self.NormDescription.addItem(item)
                item = QtWidgets.QListWidgetItem()
                self.NormDescription.addItem(item)
                item = QtWidgets.QListWidgetItem()
                item.setBackground(QtGui.QColor(233, 241, 247))
                self.NormDescription.addItem(item)

                item = self.NormDescription.item(0)
                item.setText("Benutzerdefiniert: Kein Gerenzwert.")
                item = self.NormDescription.item(1)
                item.setText("Gruppe 1 (>75kVA). Gruppe 2 (>75kVA).Klasse A. Quasi-Peak.")
                item = self.NormDescription.item(2)
                item.setText("Gruppe 1 (>75kVA). Gruppe 2 (>75kVA).Klasse A. Average.")
                item = self.NormDescription.item(3)
                item.setText("Gruppe 1 (>20kVA). Klasse A. Quasi-Peak. 10m.")
                '''item = self.NormDescription.item(4)
                item.setText("Gruppe 1 (<=20kVA). Klasse A. Quasi-Peak. 10m.")
                item = self.NormDescription.item(5)
                item.setText("Gruppe 1. Klasse B. Quasi-Peak. 3m.")
                item = self.NormDescription.item(6)
                item.setText("Gruppe 1. Klasse B. Quasi-Peak. 10m.")
                item = self.NormDescription.item(7)
                item.setText("Gruppe 2. Klasse A. Quasi-Peak. 3m.")'''
                '''item = self.NormDescription.item(8)
                item.setText("Gruppe 2. Klasse A. Quasi-Peak. 10m.")
                item = self.NormDescription.item(9)
                item.setText("Gruppe 2. Klasse A. Quasi-Peak. 30m.")
                item = self.NormDescription.item(10)
                item.setText("Gruppe 2. Klasse B. Quasi-Peak. 3m.")
                item = self.NormDescription.item(11)
                item.setText("Gruppe 2. Klasse B. Average. 3m.")
                item = self.NormDescription.item(12)
                item.setText("Gruppe 2. Klasse B. Quasi-Peak. 10m.")
                item = self.NormDescription.item(13)
                item.setText("Gruppe 2. Klasse B. Average. 10m.")'''
            # neu
            elif self.choose == 4:
                item = QtWidgets.QListWidgetItem()  # add item
                self.NormDescription.addItem(item)
                item = QtWidgets.QListWidgetItem()  # add item with background color
                item.setBackground(QtGui.QColor(233, 241, 247))
                self.NormDescription.addItem(item)
                item = QtWidgets.QListWidgetItem()  # add item
                self.NormDescription.addItem(item)

                item = self.NormDescription.item(0)
                item.setText("Benutzerdefiniert: Kein Gerenzwert.")  # Norm description text
                item = self.NormDescription.item(1)
                item.setText("Gruppe 1")  # Norm description text
                item = self.NormDescription.item(2)
                item.setText("Gruppe 2")  # Norm description text
            # neu

        # if the norm "IEC / EN 61000-4-6" is chosen, it's Kopplungseinrichtung will be showed in listView (self.NormDescription)
        elif self.NormList.currentItem().text() == 'IEC / EN 61000-4-6':
            item = QtWidgets.QListWidgetItem()
            self.NormDescription.addItem(item)
            item = QtWidgets.QListWidgetItem()
            item.setBackground(QtGui.QColor(233, 241, 247))
            self.NormDescription.addItem(item)
            item = QtWidgets.QListWidgetItem()
            self.NormDescription.addItem(item)

            item = self.NormDescription.item(0)
            item.setText('Kopplungseinrichtung:')
            item = self.NormDescription.item(1)
            item.setText("CDN")
            item = self.NormDescription.item(2)
            item.setText("Koppelzange")


        # if the norm "IEC 61000-6-2" is chosen, it's marginal values(Grenzwerte) will be showed in listView (self.NormDescription)
        elif self.NormList.currentItem().text() == 'IEC 61000-6-2':
            item = QtWidgets.QListWidgetItem()
            self.NormDescription.addItem(item)

            item = self.NormDescription.item(0)
            item.setText("Noch nicht definiert!")
        # neu
        # if the norm "IEC 61000-4-3" is chosen, it's marginal values(Grenzwerte) will be showed in listView (self.NormDescription)
        elif self.NormList.currentItem().text() == 'IEC 61000-4-3':
            item = QtWidgets.QListWidgetItem()
            self.NormDescription.addItem(item)
            item.setBackground(QtGui.QColor(233, 241, 247))

            item = self.NormDescription.item(0)
            item.setText("Standard!")
        # neu
        else:
            item = QtWidgets.QListWidgetItem()
            self.NormDescription.addItem(item)

            item = self.NormDescription.item(0)
            item.setText("Benutzerdefiniert!")

    # if users want to quit the test mode "Feldgebundene Emissionsmessung", just click the "self.GestrahltEmissionBack" button
    # then all with this test mode relevant widgets are hidden and all with this test mode relevant setting will be reset.
    # and the widgets of the start window will show up
    def go_back_anfang(self):

        self.VerticalLine.show()
        self.PleaseChoose.show()
        self.EmissionsmessungLabel.show()
        self.StoerfestigkeitLabel.show()
        self.line.show()
        self.FeldgebundenEmissionMode.show()
        self.FeldgebundenStoerfestigkeitMode.show()
        self.FeldgebundenEmissionModeLabel.show()
        self.FeldgebundenStoerfestigkeitModeLabel.show()
        self.LeistungsgebundeneEmissionMode.show()
        self.LeitungsgebundenStoerfestigkeitMode.show()
        self.LeistungsgebundeneEmissionModeLabel.show()
        self.LeitungsgebundenStoerfestigkeitModeLabel.show()

        self.EquipmentSettingButton.hide()
        self.TestSettingButton.hide()
        self.CalibrationButton.hide()
        self.TestStartButton.hide()
        self.ReportButton.hide()
        self.EquipmentSettingLabel.hide()
        self.TestSettingLabel.hide()
        self.CalibrationLabel.hide()
        self.ReportLabel.hide()
        self.TestLabel.hide()
        self.UniLogoLabel.hide()
        self.IEHLogoLabel.hide()
        self.GestrahltEmissionBack.hide()
        self.NormGroupBox.hide()
        self.NormDescription.hide()
        self.NormList.hide()
        self.NormChooseButton.hide()
        self.NormAddButton.hide()
        self.NormDescription.clear()

    # if " Menu bar -> Sicherheit -> Aktivieren " is clicked, the "Erstellung des Administratorpasswortes" window will show up. see line 448
    def openministratorpassword(self):
        widget = QtWidgets.QDialog()
        ui = Ui_PasswordWindow()
        ui.setupUi(widget)
        widget.exec_()

    # if " Menu bar -> Einstellen -> Optionen " is clicked, the "Software Optionen" window will show up. see line 15
    def opensoftwareoptions(self):
        widget = QtWidgets.QDialog()
        ui = Ui_SoftwareOptionen()
        ui.setupUi(widget)
        widget.exec_()

    # under the test mode "Feldgebundene Emissionsmessung", if users click the "Kalibrierung" button, an information
    # messageBox will show up and says that the functionality of calibration is not implemented yet. (because it is not needed in this experiment)
    def calibrationwarning(self):
        # neu
        if self.choose == 4:
            ui = Ui_Calibration()
            ui.setupUi()
            ui.exec_()
        # neu
        # QtWidgets.QMessageBox.information(self.ui)
        else:
            QtWidgets.QMessageBox.information(self, "Hinweis", "Diese Funktionalität ist noch nicht implementiert.")


# function that can process .jpg image
def pic_preprocess(img, new_height):
    show = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    width = show.shape[1]
    height = show.shape[0]
    ratio = float(height / width)
    new_width = int(new_height / ratio)
    show = cv.resize(show, (new_width, new_height))
    totalBytes = show.nbytes
    bytesPerLine = int(totalBytes / new_height)
    return QtGui.QImage(show, new_width, new_height, bytesPerLine, QtGui.QImage.Format_RGB888)


# function that can process .png image
def png_preprocess(img, new_height):
    width = img.shape[1]
    height = img.shape[0]
    ratio = float(height / width)
    new_width = int(new_height / ratio)
    show = cv.resize(img, (new_width, new_height))
    totalBytes = show.nbytes
    bytesPerLine = int(totalBytes / new_height)
    return QtGui.QImage(show, new_width, new_height, bytesPerLine, QtGui.QImage.Format_ARGB32)
