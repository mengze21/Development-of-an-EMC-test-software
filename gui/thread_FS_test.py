import sys, os
from os.path import join, getsize

from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
import sys
import time
sys.path.append('gui')


class External_FS_test(QThread):
    completedflag = pyqtSignal(bool)
    countChanged = pyqtSignal(float, float, float)
    dataCache = pyqtSignal(list, list, list)
    def __init__(self, StartFreq, FreqStep, MaxFreq):
        #QtCore.QThread.__init__(self)
        super(External_FS_test, self).__init__()
        self.StartFreq = StartFreq
        self.FreqStep = FreqStep
        self.MaxFreq = MaxFreq
        self.stopped = False
        self.completed = False
        self.restart = False
        self.ispaused = False
        self.testFreq = 0
        self.vorPower = 0
        self.FieldStrength = 0

    def initialize(self):
        #self.stopped = False
        self.completed = False
        self.restart = False

    def run(self):
        self.stopped = False
        self.testFreq = self.StartFreq
        # measuredFreq = 0
        # vorPower = 0
        # FieldStrength = 0
        while self.testFreq < self.MaxFreq:
            self.vorPower = self.vorPower + 0.04
            self.FieldStrength = self.FieldStrength + 0.04
            print("testFreq %s" %self.testFreq)
            print("freq step %s" % self.FreqStep)
            measuredFreq = self.testFreq
            vorPower = self.vorPower
            FieldStrength = self.FieldStrength
            self.testFreq = self.testFreq + self.FreqStep * self.testFreq
            self.countChanged.emit(measuredFreq, vorPower, FieldStrength)

            time.sleep(0.1)
            while self.ispaused:
                time.sleep(0)

            if self.stopped:
                break
        if not self.stopped:
            self.completed = True
            completed = self.completed
            self.completedflag.emit(completed)
        #self.completed = True
        #self.completedflag.emit(self.completed)
        # for i in range(10):
        #     print(i)
        #     time.sleep(1)
        #
        #     while self.ispaused:
        #         time.sleep(0)
        #
        #     if self.stopped:
        #         break
        # if i == 9 :
        #     print("thread finished")
        #self.completed = True
        #completed = self.completed
        #self.completedflag.emit(completed)

    def stop(self):
        print("thread stoped")
        self.stopped = True

    def pause(self):
        # restart
        self.ispaused = True

    def resum(self):
        self.ispaused = False
