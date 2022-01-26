# -*- coding: utf-8 -*-

# This script connects all windows together.

import sys

sys.path.append('gui')
from PyQt5 import QtGui, QtWidgets, uic
from MainWindow import Ui_MainWindow
from ManagementderAusrustung_FE import FE_EquipmentManagement
from ManagementderAusrustung_LS import LS_EquipmentManagement
from ManagementderAusrustung_LE import LE_EquipmentManagement
from ManagementderAusrustung_FS import FS_EquipmentManagement
from TestWindow_LE import Ui_TestWindow_LE
from TestWindow_FE import Ui_TestWindow_FE
from TestWindow_LS import Ui_TestWindow_LS
from TestWindow_FS import Ui_TestWindow_FS
from Versuchsaufbau import Ui_TestSetUp
from ReportWindow import Ui_ReportWindow
from versuchsaufbau_FS import Ui_CalibrationSetup_FS
import sys


# Initialization of the "Repots" Window
class ReportGernartion(QtWidgets.QWidget, Ui_ReportWindow):
    def __init__(self, parent=None):
        super(ReportGernartion, self).__init__(parent)
        self.setupUi(self)


# Initialization of the "Testkonfiguration" Window
class TestSetUp(QtWidgets.QWidget, Ui_TestSetUp):
    def __init__(self, parent=None):
        super(TestSetUp, self).__init__(parent)
        self.setupUi(self)


# Initialization of the "Test_LE" Window
class Test_LE(QtWidgets.QWidget, Ui_TestWindow_LE):
    def __init__(self, parent=None):
        super(Test_LE, self).__init__(parent)
        self.setupUi(self)


# Initialization of the "Test_FE" Window
class Test_FE(QtWidgets.QWidget, Ui_TestWindow_FE):
    def __init__(self, parent=None):
        super(Test_FE, self).__init__(parent)
        self.setupUi(self)


# Initialization of the "Test_LS" Window
class Test_LS(QtWidgets.QWidget, Ui_TestWindow_LS):
    def __init__(self, parent=None):
        super(Test_LS, self).__init__(parent)
        self.setupUi(self)


# neu
# Initialization of the "Test_FS" Window
class Test_FS(QtWidgets.QWidget, Ui_TestWindow_FS):
    def __int__(self, parent=None):
        super(Test_FS, self).__int__(parent)
        self.setupUi(self)
# neu


# Initialization of the "Gerätemanagement" Fenster for 4 tests
class Equipment(QtWidgets.QWidget, FE_EquipmentManagement):
    def __init__(self, parent=None):
        super(Equipment, self).__init__(parent)
        self.setupUi(self)


class Equipment(QtWidgets.QWidget, LS_EquipmentManagement):
    def __init__(self, parent=None):
        super(Equipment, self).__init__(parent)
        self.setupUi(self)


class Equipment(QtWidgets.QWidget, LE_EquipmentManagement):
    def __init__(self, parent=None):
        super(Equipment, self).__init__(parent)
        self.setupUi(self)

# neu
class Equipment(QtWidgets.QWidget, FS_EquipmentManagement):
    def __init__(self, parent=None):
        super(Equipment, self).__init__(parent)
        self.setupUi(self)
# neu


# This MainWindow is the main body of the whole gui. After chosing the test mode "Feldgebundene Emissionsmessung", this MainWindow will show up.
# The function of this class is to connect the functional buttons to corrosponding windows.
# For example, if user clicks the EquipmentSettingButton, the window of "Gerätemanagement" will show up.
class MyMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        # singals for connecting the functional buttons to the corrospongding slot functions
        self.EquipmentSettingButton.clicked.connect(self.equipmentManagement)
        self.TestStartButton.clicked.connect(self.testStart)
        self.TestSettingButton.clicked.connect(self.testSETUP)
        self.ReportButton.clicked.connect(self.reporthaving)

        # Make sure that the MainWindow is on the center of user's desktop
        self.center()

    # This method is used for reminding users.
    # When users close the MainWindow, a messageBox will show up and ask: Do yo really want to close the window? Two options: Yes or no.
    def closeEvent(self, QCloseEvent):
        # Defining the messageBox.
        messageBox = QtWidgets.QMessageBox()
        messageBox.setWindowTitle('Programm beenden')
        messageBox.setIcon(QtWidgets.QMessageBox.Question)
        messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
        messageBox.setText('Möchten Sie das Programm wirklich beenden?')
        # Definition of the options
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        messageBox.setDefaultButton(QtWidgets.QMessageBox.No)
        # Change the English text of options into German.
        buttonY = messageBox.button(QtWidgets.QMessageBox.Yes)
        buttonY.setText('Ja')
        buttonN = messageBox.button(QtWidgets.QMessageBox.No)
        buttonN.setText('Nein')
        messageBox.exec_()
        # If option "Yes", the "close" command for the MainWindow will be accepted, otherwise, the MainWindow won't be closed
        if messageBox.clickedButton() == buttonY:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

    # slot function of the "Test" Window
    def reporthaving(self):
        widget = QtWidgets.QDialog(self)
        ui = Ui_ReportWindow()
        ui.setupUi(widget)
        widget.exec_()

    # slot function of the "Gerätemanagement" Window
    # FE choose=1,LE choose =2, LS choose=3, FS choose=4
    def equipmentManagement(self):
        print(self.choose)
        if self.choose == 1:
            widget = QtWidgets.QDialog(self)
            ui = FE_EquipmentManagement()
            ui.setupUi(widget)
            widget.exec_()
            # antenne factors are tansported into the "Gerätemanagement" Window
            self.anntef = ui.anntenfre
            self.anntem = ui.anntenmag
            self.kabelf1 = ui.frequenz1
            self.kabelm1 = ui.magnitude1
            self.kabelf2 = ui.frequenz2
            self.kabelm2 = ui.magnitude2
        elif self.choose == 2:
            widget = QtWidgets.QDialog(self)
            ui = LE_EquipmentManagement()
            ui.setupUi(widget)
            widget.exec_()
            # antenne factors are tansported into the "Gerätemanagement" Window
            self.anntef = ui.anntenfre
            self.anntem = ui.anntenmag
            self.kabelf1 = ui.frequenz1
            self.kabelm1 = ui.magnitude1
            self.kabelf2 = ui.frequenz2
            self.kabelm2 = ui.magnitude2
        elif self.choose == 3:
            widget = QtWidgets.QDialog(self)
            ui = LS_EquipmentManagement()
            ui.setupUi(widget)
            widget.exec_()
        # neu
        elif self.choose == 4:
            widget = QtWidgets.QDialog(self)
            ui = FS_EquipmentManagement()
            ui.setupUi(widget)
            widget.exec_()
            # antenne factors are tansported into the "Gerätemanagement" Window
            self.anntef = ui.anntenfre
            self.anntem = ui.anntenmag
            self.kabelf1 = ui.frequenz1
            self.kabelm1 = ui.magnitude1
            self.kabelf2 = ui.frequenz2
            self.kabelm2 = ui.magnitude2
        # neu

    # slot function for the "Test" window.
    def testStart(self):
        # Conditions for judging wether norms are selected when users open the "Test" window
        if self.choose == 1:
            if self.NormDescription.count() == 0:  # If no norms selected, a warning messageBox show up
                messageBox = QtWidgets.QMessageBox()
                messageBox.setWindowTitle('Normauswahl')
                messageBox.setIcon(QtWidgets.QMessageBox.Warning)
                messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
                messageBox.setText('Bitte wählen Sie zuerst eine Norm aus!')
                messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
                buttonY.setText('Ok')
                messageBox.exec_()
            # if norm "CISPR 11: EN 55011" is selected, show all it's detailed marginal values (Grenzwerte) in a listView
            else:
                if self.NormList.currentItem().text() == "CISPR 11: EN 55011":
                    widget = QtWidgets.QDialog(self)
                    ui = Ui_TestWindow_FE()
                    ui.setupUi(widget)
                    # recieving the chosed marginal value and draw a curve for it in "Test" window
                    www = self.NormDescription.selectedItems()
                    ui.drawnormlimit(www)
                    # Tansfer the antenne factors into "Test" window
                    if self.anntef != []:
                        ui.tianxianf = self.anntef
                        ui.tianxianm = self.anntem
                        ui.cablef1 = self.kabelf1
                        ui.cablem1 = self.kabelm1
                        ui.cablef2 = self.kabelf2
                        ui.cablem2 = self.kabelm2
                    widget.exec_()
                # if norm "IEC / EN 61000-4-3" is selected, whose marginal values (Grenzwerte) are not defined yet, a warning messageBox will show up and
                # tell users "The marginal values (Grenzwerte) of this norm are not defined, please go back and choose other norms."
                elif self.NormList.currentItem().text() == "IEC / EN 61000-4-6":
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Mangel an Definition')
                    messageBox.setIcon(QtWidgets.QMessageBox.Warning)
                    messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
                    messageBox.setText('Sorry, diese Norm ist für die Prüfung nicht geeigenet.')
                    messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
                    buttonY.setText('Ok')
                    messageBox.exec_()
                # if norm "IEC 61000-6-2" is selected, whose marginal values (Grenzwerte) are not defined yet, a warning messageBox will show up and
                # tell users "The marginal values (Grenzwerte) of this norm are not defined, please go back and choose other norms."
                elif self.NormList.currentItem().text() == "IEC 61000-6-2":
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Mangel an Definition')
                    messageBox.setIcon(QtWidgets.QMessageBox.Warning)
                    messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
                    messageBox.setText('Sorry, diese Norm wird bald hinzugefügt.')
                    messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
                    buttonY.setText('Ok')
                    messageBox.exec_()
                # if a not yet defined norm is selected, a warning messageBox will show up and tell users "This norm is not defined, please go back and choose other norms"
                else:
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Mangel an Definition')
                    messageBox.setIcon(QtWidgets.QMessageBox.Warning)
                    messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
                    messageBox.setText('Sorry, diese Norm wird bald hinzugefügt.')
                    messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
                    buttonY.setText('Ok')
                    messageBox.exec_()
        elif self.choose == 2:
            if self.NormDescription.count() == 0:  # If no norms selected, a warning messageBox show up
                messageBox = QtWidgets.QMessageBox()
                messageBox.setWindowTitle('Normauswahl')
                messageBox.setIcon(QtWidgets.QMessageBox.Warning)
                messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
                messageBox.setText('Bitte wählen Sie zuerst eine Norm aus!')
                messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
                buttonY.setText('Ok')
                messageBox.exec_()
            # if norm "CISPR 11: EN 55011" is selected, show all it's detailed marginal values (Grenzwerte) in a listView
            else:
                if self.NormList.currentItem().text() == "CISPR 11: EN 55011":
                    widget = QtWidgets.QDialog(self)
                    ui = Ui_TestWindow_LE()
                    ui.setupUi(widget)
                    # recieving the chosed marginal value and draw a curve for it in "Test" window
                    www = self.NormDescription.selectedItems()
                    ui.drawnormlimit(www)
                    # Tansfer the antenne factors into "Test" window
                    if self.anntef != []:
                        ui.tianxianf = self.anntef
                        ui.tianxianm = self.anntem
                        ui.cablef1 = self.kabelf1
                        ui.cablem1 = self.kabelm1
                        ui.cablef2 = self.kabelf2
                        ui.cablem2 = self.kabelm2
                    widget.exec_()
                # if norm "IEC / EN 61000-4-3" is selected, whose marginal values (Grenzwerte) are not defined yet, a warning messageBox will show up and
                # tell users "The marginal values (Grenzwerte) of this norm are not defined, please go back and choose other norms."
                elif self.NormList.currentItem().text() == "IEC / EN 61000-4-6":
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Mangel an Definition')
                    messageBox.setIcon(QtWidgets.QMessageBox.Warning)
                    messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
                    messageBox.setText('Sorry, diese Norm ist für die Prüfung nicht geeigenet.')
                    messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
                    buttonY.setText('Ok')
                    messageBox.exec_()
                # if norm "IEC 61000-6-2" is selected, whose marginal values (Grenzwerte) are not defined yet, a warning messageBox will show up and
                # tell users "The marginal values (Grenzwerte) of this norm are not defined, please go back and choose other norms."
                elif self.NormList.currentItem().text() == "IEC 61000-6-2":
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Mangel an Definition')
                    messageBox.setIcon(QtWidgets.QMessageBox.Warning)
                    messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
                    messageBox.setText('Sorry, diese Norm wird bald hinzugefügt.')
                    messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
                    buttonY.setText('Ok')
                    messageBox.exec_()
                # if a not yet defined norm is selected, a warning messageBox will show up and tell users "This norm is not defined, please go back and choose other norms"
                else:
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Mangel an Definition')
                    messageBox.setIcon(QtWidgets.QMessageBox.Warning)
                    messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
                    messageBox.setText('Sorry, diese Norm wird bald hinzugefügt.')
                    messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
                    buttonY.setText('Ok')
                    messageBox.exec_()
        elif self.choose == 3:
            if self.NormDescription.count() == 0:  # If no norms selected, a warning messageBox show up
                messageBox = QtWidgets.QMessageBox()
                messageBox.setWindowTitle('Normauswahl')
                messageBox.setIcon(QtWidgets.QMessageBox.Warning)
                messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
                messageBox.setText('Bitte wählen Sie zuerst eine Norm aus!')
                messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
                buttonY.setText('Ok')
                messageBox.exec_()

            # if norm "CISPR 11: EN 55011" is selected, whose coupling devices are not defined yet, a warning messageBox will show up and
            # tell users "The coupling devices of this norm are not defined, please go back and choose other norms."
            else:
                if self.NormList.currentItem().text() == "CISPR 11: EN 55011":
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Mangel an Definition')
                    messageBox.setIcon(QtWidgets.QMessageBox.Warning)
                    messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
                    messageBox.setText('Sorry, diese Norm ist für die Prüfung nicht geeigenet.')
                    messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
                    buttonY.setText('Ok')
                    messageBox.exec_()

                # if norm "IEC / EN 61000-4-6" is selected, show all it's detailed coupling devices in a listView
                elif self.NormList.currentItem().text() == "IEC / EN 61000-4-6":
                    widget = QtWidgets.QDialog(self)
                    ui = Ui_TestWindow_LS()
                    ui.setupUi(widget)
                    # recieving the chosed marginal value and draw a curve for it in "Test" window
                    www = self.NormDescription.selectedItems()
                    ui.drawnormlimit(www)
                    # Tansfer the antenne factors into "Test" window
                    if self.anntef != []:
                        ui.tianxianf = self.anntef
                        ui.tianxianm = self.anntem
                        ui.cablef1 = self.kabelf1
                        ui.cablem1 = self.kabelm1
                        ui.cablef2 = self.kabelf2
                        ui.cablem2 = self.kabelm2
                    widget.exec_()

                # if norm "IEC 61000-6-2" is selected, whose marginal values (Grenzwerte) are not defined yet, a warning messageBox will show up and
                # tell users "The marginal values (Grenzwerte) of this norm are not defined, please go back and choose other norms."
                elif self.NormList.currentItem().text() == "IEC 61000-6-2":
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Mangel an Definition')
                    messageBox.setIcon(QtWidgets.QMessageBox.Warning)
                    messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
                    messageBox.setText('Sorry, diese Norm wird bald hinzugefügt.')
                    messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
                    buttonY.setText('Ok')
                    messageBox.exec_()
                # if a not yet defined norm is selected, a warning messageBox will show up and tell users "This norm is not defined, please go back and choose other norms"
                else:
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Mangel an Definition')
                    messageBox.setIcon(QtWidgets.QMessageBox.Warning)
                    messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
                    messageBox.setText('Sorry, diese Norm wird bald hinzugefügt.')
                    messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
                    buttonY.setText('Ok')
                    messageBox.exec_()
        # neu
        elif self.choose == 4:
            if self.NormDescription.count() == 0:  # If no norms selected, a warning messageBox show up
                messageBox = QtWidgets.QMessageBox()
                messageBox.setWindowTitle('Normauswahl')
                messageBox.setIcon(QtWidgets.QMessageBox.Warning)
                messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
                messageBox.setText('Bitte wählen Sie zuerst eine Norm aus!')
                messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
                buttonY.setText('Ok')
                messageBox.exec_()

            else:
                if self.NormList.currentItem().text() == "IEC 61000-4-3":
                    widget = QtWidgets.QDialog(self)
                    ui = Ui_TestWindow_FS()
                    ui.setupUi(widget)
                    # recieving the chosed marginal value and draw a curve for it in "Test" window
                    www = self.NormDescription.selectedItems()
                    ui.drawnormlimit(www)
                    # Tansfer the antenne factors into "Test" window
                    if self.anntef != []:
                        ui.tianxianf = self.anntef
                        ui.tianxianm = self.anntem
                        ui.cablef1 = self.kabelf1
                        ui.cablem1 = self.kabelm1
                        ui.cablef2 = self.kabelf2
                        ui.cablem2 = self.kabelm2
                    widget.exec_()

                # if norm "CISPR 11: EN 55011" is selected, whose coupling devices are not defined yet,
                # a warning messageBox will show up and tell users
                # "The coupling devices of this norm are not defined, please go back and choose other norms."
                elif self.NormList.currentItem().text() == "CISPR 11: EN 55011":
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Mangel an Definition')
                    messageBox.setIcon(QtWidgets.QMessageBox.Warning)
                    messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
                    messageBox.setText('Sorry, diese Norm ist für die Prüfung nicht geeigenet.')
                    messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
                    buttonY.setText('Ok')
                    messageBox.exec_()

                elif self.NormList.currentItem().text() == "IEC / EN 61000-4-6":
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Mangel an Definition')
                    messageBox.setIcon(QtWidgets.QMessageBox.Warning)
                    messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
                    messageBox.setText('Sorry, diese Norm ist für die Prüfung nicht geeigenet.')
                    messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
                    buttonY.setText('Ok')
                    messageBox.exec_()

                elif self.NormList.currentItem().text() == "IEC 61000-6-2":
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Mangel an Definition')
                    messageBox.setIcon(QtWidgets.QMessageBox.Warning)
                    messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
                    messageBox.setText('Sorry, diese Norm ist für die Prüfung nicht geeigenet.')
                    messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
                    buttonY.setText('Ok')
                    messageBox.exec_()

                    # if a not yet defined norm is selected, a warning messageBox will show up and tell users "This norm is not defined, please go back and choose other norms"
                else:
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Mangel an Definition')
                    messageBox.setIcon(QtWidgets.QMessageBox.Warning)
                    messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
                    messageBox.setText('Sorry, diese Norm wird bald hinzugefügt.')
                    messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
                    buttonY.setText('Ok')
                    messageBox.exec_()
        # neu

    # slot function of "Testkonfiguration" Window
    def testSETUP(self):
        #neu
        if self.choose == 4:
            #ui = Ui_Calibration_FS()
            #ui.setupUi()
            #ui.exec_()
            widget = QtWidgets.QDialog(self)
            ui = Ui_CalibrationSetup_FS()
            ui.setupUi(widget)
            widget.exec_()
        #neu
        else:
            widget = QtWidgets.QDialog(self)
            ui = Ui_TestSetUp()
            ui.setupUi(widget)
            widget.exec_()

    # Method to make sure that the gui is placed in the center of users desktop
    def center(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


if __name__ == "__main__":
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    mywin = MyMainWindow()
    mywin.show()
    sys.exit(app.exec_())
