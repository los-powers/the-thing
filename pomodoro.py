import os
from PyQt5 import QtWidgets, QtCore, QtGui
import signal
import sys
import time

REST_DURATION = 5
TOO_EARLY = 800
TOO_LATE = 1900
WORK_DURATION = 20


class PomodoroTimer(QtWidgets.QSystemTrayIcon):
    rest_icon_path = 'red.png'
    work_icon_path = 'green.png'

    def __init__(self, parent=None):
        super(PomodoroTimer, self).__init__()
        self.rest_icon = QtGui.QIcon(self.rest_icon_path)
        self.work_icon = QtGui.QIcon(self.work_icon_path)
        self.parent = parent

        self.cur_icon = self.work_icon
        self.setIcon(self.cur_icon)
        self.show()

        self.until = set_time(WORK_DURATION)

        menu = QtWidgets.QMenu(self.parent)
        menu.addAction('Exit')
        self.setContextMenu(menu)
        menu.triggered.connect(self.exit)
        self.display_msg_box()

    def display_msg_box(self):
        msgbox = QtWidgets.QMessageBox()
        msgbox.setIcon(QtWidgets.QMessageBox.Information)
        msgbox.setWindowIcon(self.cur_icon)
        if self.cur_icon == self.rest_icon:
            msgbox.setText('Rest until %s' % self.until)
        else:
            msgbox.setText('Work until %s' % self.until)
        msgbox.setFocus(True)
        msgbox.exec_()

    def exit(self):
        QtCore.QCoreApplication.exit()

    def update_icon(self):
        cur_time = int(time.strftime('%H%M'))
        if self.until <= cur_time:
            if self.cur_icon == self.rest_icon:
                self.cur_icon = self.work_icon
                self.until = set_time(WORK_DURATION)
            else:
                self.cur_icon = self.rest_icon
                self.until = set_time(REST_DURATION)
            self.setIcon(self.cur_icon)
            self.display_msg_box()


def find_already_running():
    run_count = 0
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    for pid in pids:
        ps = open(os.path.join('/proc', pid, 'cmdline'), 'rb').read()
        args = ps.split('\0')
        if len(args) > 2:
            if sys.argv[0] in args:
                run_count += 1
                if run_count > 1:
                    print '%s is already running' % sys.argv[0]
                    sys.exit()


def tray_icon():
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    wdgt = QtWidgets.QWidget()
    trayIcon = PomodoroTimer(wdgt)
    qtimer = QtCore.QTimer()
    qtimer.timeout.connect(trayIcon.update_icon)
    qtimer.start(1000)
    trayIcon.show()
    sys.exit(app.exec_())


def set_time(offset=0):
    ret_time = int(time.strftime('%H%M')) + offset
    if ret_time % 100 / 60 > 0:
        ret_time = ret_time + 40
    return ret_time


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    find_already_running()
    tray_icon()
