import sys
import os.path
from countdown import Countdown
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QSound
import atexit


def save(w, c, __file__):
    f = open(os.path.abspath(os.path.dirname(__file__)) + '/save/countdown_save.bin', 'wb+')

    f.write(str.encode(str(w.countdown_hours_spinBox.value()) + ':' + str(w.countdown_mins_spinBox.value()) + ':' + str(
        w.countdown_secs_spinBox.value()) + '\n'))
    f.write(str.encode(str(c.hours) + ':' + str(c.mins) + ':' + str(c.secs)))

    f.close()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    w = loadUi(os.path.abspath(os.path.dirname(__file__)) + '/ui/clock.ui')

    w.setWindowIcon(QtGui.QIcon(os.path.abspath(os.path.dirname(__file__)) + '/image/clock.ico'))

    try:
        countdown_history = open(os.path.abspath(os.path.dirname(__file__)) + '/save/countdown_save.bin', 'rb')
        countdown_lines = countdown_history.readlines()
        countdown_set_time = countdown_lines[0].decode().strip('\n').split(':')
        countdown_current_time = countdown_lines[1].decode().split(':')
        for i in range(0, len(countdown_set_time)):
            countdown_set_time[i] = int(countdown_set_time[i])
            countdown_current_time[i] = int(countdown_current_time[i])
        c = Countdown(w, countdown_set_time, countdown_current_time)
    except:
        c = Countdown(w)

    w.countdown_timer = QTimer()

    w.beep_sound = QSound(os.path.abspath(os.path.dirname(__file__)) + '/sound/bip-bip.wav')
    w.beep_sound.setLoops(10)

    w.countdown_stop_btn.clicked.connect(c.reset_btn)
    w.countdown_start_btn.clicked.connect(c.start_btn)
    w.countdown_pause_btn.clicked.connect(c.pause_btn)
    w.countdown_close_btn.clicked.connect(c.close_btn)
    w.countdown_hours_spinBox.valueChanged.connect(c.setCountdownTime)
    w.countdown_mins_spinBox.valueChanged.connect(c.setCountdownTime)
    w.countdown_secs_spinBox.valueChanged.connect(c.setCountdownTime)
    w.countdown_timer.timeout.connect(c.display)

    atexit.register(save, w, c, __file__)

    w.show()
    app.exec_()
