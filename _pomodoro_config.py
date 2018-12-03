"""
https://stackoverflow.com/questions/39023584/implementing-a-preferences-dialog-window-in-pyqt
"""

import sys
import ConfOBJ

from PyQt5 import QtCore, QtGui, QtWidgets


class ConfigDialog(object):
    def setup_config(self, Dialog):
        Dialog.setObjectName('Configurations')
        Dialog.resize(500, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(150, 250, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.work_time_slider = QtWidgets.QSlider(Dialog)
        self.work_time_slider.setGeometry(QtCore.QRect(150, 250, 340, 30))
        self.work_time_slider.setOrientation(QtCore.Qt.Horizontal)
        self.work_time_slider.setObjectName('Work time slider')
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
