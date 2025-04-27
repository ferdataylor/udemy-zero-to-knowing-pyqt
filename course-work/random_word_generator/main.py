# Import Modules
from PyQt5.QtCore import Qt # for misc things like alignment
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

# Getting a Random Word from a List
from random import choice



# Main App Objects and Settings
app = QApplication([])
main_window = QWidget() # can use QMainWindow() for more complex apps
main_window.setWindowTitle("Random Word Maker")
main_window.resize(300, 200) # starting size, resizeable


# Create all App Objects
title = QLabel("Random Keywords")

text1 = QLabel("?")
text2 = QLabel("?")
text3 = QLabel("?")

button1 = QPushButton("Generate")
button2 = QPushButton("Clear")
button3 = QPushButton("Exit")


# Create our list of words
words = ["apple", "banana", "cherry", "date", "fig", "grape", "kiwi", "lemon", "mango", "nectarine"]


#--- Add Functions Here ---#
#functions don not need to be created in any order

def random_word1():
    # Get a random word from the list
    word = choice(words)
    # Set the text of the label to the random word
    text1.setText(word)

def random_word2():
    # Get a random word from the list
    word = choice(words)
    # Set the text of the label to the random word
    text2.setText(word)

def random_word3():
    # Get a random word from the list
    word = choice(words)
    # Set the text of the label to the random word
    text3.setText(word)


# All Design and Layout Here
master_layout = QVBoxLayout()

row1 = QHBoxLayout()
row2 = QHBoxLayout()
row3 = QHBoxLayout()

row1.addWidget(title, alignment=Qt.AlignCenter)

row2.addWidget(text1, alignment=Qt.AlignCenter)
row2.addWidget(text2, alignment=Qt.AlignCenter)
row2.addWidget(text3, alignment=Qt.AlignCenter)

row3.addWidget(button1)
row3.addWidget(button2)
row3.addWidget(button3)

#add layout widgets to layouts
master_layout.addLayout(row1)
master_layout.addLayout(row2)
master_layout.addLayout(row3)

main_window.setLayout(master_layout)


# Events
button1.clicked.connect(random_word1)
button2.clicked.connect(random_word2)
button3.clicked.connect(random_word3)


# Show/Run our App
main_window.show()
app.exec_()
# End of File
