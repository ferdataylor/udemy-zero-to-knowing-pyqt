from PyQt5.QtCore import Qt # for misc things like alignment
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QFont


#--- App Settings ---#

app = QApplication([])
main_window = QWidget() # can use QMainWindow() for more complex apps

main_window.setWindowTitle("Interactive Calculator")
main_window.resize(250, 300) # starting size, resizeable


#--- All objects/widgets ---#

# NOTE: This text_box is outside of the grid but inside the main window
text_box = QLineEdit()
text_box.setFont(QFont("Helvetica", 32))

grid = QGridLayout()

buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "0", "=", "+"
]

clear_button = QPushButton("Clear")
delete_button = QPushButton("<")


#--- Event Handling ---#

# This is where the buttons-clicked event handling function goes
def button_click():
    
    # Listen for who was clicked
    button = app.sender()
    
    # Get the text of the button
    text = button.text()
    
    # Check if the text is the equal sign
    if text == "=":
        
        # Grab the text from the text box
        symbol = text_box.text()
        try:
            # Evaluate the expression
            result = eval(symbol)
            # Set the text box to the result
            text_box.setText(str(result))
        except Exception as e:
            # If there is an error, set the text box to the error
            print("Error:", e)
            text_box.setText("Error")
        
    elif text == "Clear":
        # Clear the text box
        text_box.clear()
        
    elif text == "<":
        current_value = text_box.text()
        # Delete the last character in the text box
        text_box.setText(current_value[:-1])
    else:
        # Append the text of the button to the text box
        current_value = text_box.text()
        text_box.setText(current_value + text)
# Connect the buttons to the button_click function


row = 0
col = 0

# Add buttons to the grid
#This needs to go before our layout.
for text in buttons:
    button = QPushButton(text)
    
    # NOTE: This button has to connect to some kind of event handler function
    # so that event handling function must be defined before this line
    button.clicked.connect(button_click)
    
    grid.addWidget(button, row, col)
    
    col += 1
    if col > 3:
        col = 0
        row += 1


#--- Design and Layout ---#

master_layout = QVBoxLayout()
master_layout.addWidget(text_box)
master_layout.addLayout(grid)

button_row = QHBoxLayout()
button_row.addWidget(clear_button)
button_row.addWidget(delete_button)

master_layout.addLayout(button_row)

main_window.setLayout(master_layout)

clear_button.clicked.connect(button_click)
delete_button.clicked.connect(button_click)

#--- Styles ---#

# NOTE: This is a very basic style, you can customize it as you like
main_window.setStyleSheet("""
    QWidget {
        background-color: #2E2E2E;
        color: #FFFFFF;
    }
    QLineEdit {
        background-color: #1E1E1E;
        color: #FFFFFF;
        border: 1px solid #3C3C3C;
    }
    QPushButton {
        background-color: #3C3C3C;
        color: #FFFFFF;
        border: 1px solid #3C3C3C;
    }
    QPushButton:hover {
        background-color: #4E4E4E;
    }
""")


#--- Show/Run --#

main_window.show()
app.exec_()