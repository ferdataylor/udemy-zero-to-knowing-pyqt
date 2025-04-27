import sys
import os

from PyQt5.QtCore import Qt # for misc things like alignment
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QFont


# App Settings
app = QApplication([sys.argv])
main_window = QWidget() # can use QMainWindow() for more complex apps
main_window.setWindowTitle("My First App")
main_window.resize(300, 200) # starting size, resizeable

# Create all objects/widgets below here


main_window.show()
app.exec_()