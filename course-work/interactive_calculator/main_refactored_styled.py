from PyQt5.QtCore import Qt # for misc things like alignment
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QFont


class CalcApp(QWidget):

    def __init__(self):
        super().__init__()

        #--- App Settings ---#
        self.setWindowTitle("Interactive Calculator")
        self.resize(250, 300) # starting size, resizeable


        #--- All objects/widgets ---#
        # NOTE: This text_box is outside of the grid but inside the main window
        self.text_box = QLineEdit()
        self.text_box.setFont(QFont("Helvetica", 32))

        self.grid = QGridLayout()

        self.buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", "=", "+"
        ]

        row = 0
        col = 0

        # Add buttons to the grid
        #This needs to go before our layout.
        for text in self.buttons:
            button = QPushButton(text)
            
            # NOTE: This button has to connect to some kind of event handler function
            # so that event handling function must be defined before this line
            button.clicked.connect(self.button_click)
            
            #--- Button Styles ---#
            button.setStyleSheet("QPushButton { font-size: 25px Comic Sans MS; padding: 10px; color: #948979 }")
            
            self.grid.addWidget(button, row, col)
            
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.clear_button = QPushButton("Clear")
        self.delete_button = QPushButton("<")
        
        
        #--- Design and Layout ---#
        master_layout = QVBoxLayout()
        master_layout.addWidget(self.text_box)
        master_layout.addLayout(self.grid)

        button_row = QHBoxLayout()
        button_row.addWidget(self.clear_button)
        button_row.addWidget(self.delete_button)

        master_layout.addLayout(button_row)

        #--- Master Layout Styles ---#
        master_layout.setContentsMargins(25, 25, 25, 25)

        self.setLayout(master_layout)

        self.clear_button.clicked.connect(self.button_click)
        self.delete_button.clicked.connect(self.button_click)
        
        #--- Clear & Delete Button Styles ---#
        self.clear_button.setStyleSheet("QPushButton { font-size: 25px Comic Sans MS; padding: 10px; color: #F7AD45 }")
        self.delete_button.setStyleSheet("QPushButton { font-size: 25px Comic Sans MS; padding: 10px; color: #F7AD45 }")



    #--- Event Handling ---#
    # This is where the buttons-clicked event handling function goes
    def button_click(self):
        
        # Listen for who was clicked
        button = app.sender()
        
        # Get the text of the button
        text = button.text()
        
        # Check if the text is the equal sign
        if text == "=":
            
            # Grab the text from the text box
            symbol = self.text_box.text()
            try:
                # Evaluate the expression
                result = eval(symbol)
                # Set the text box to the result
                self.text_box.setText(str(result))
            except Exception as e:
                # If there is an error, set the text box to the error
                print("Error:", e)
                self.text_box.setText("Error")
            
        elif text == "Clear":
            # Clear the text box
            self.text_box.clear()
            
        elif text == "<":
            current_value = self.text_box.text()
            # Delete the last character in the text box
            self.text_box.setText(current_value[:-1])
        else:
            # Append the text of the button to the text box
            current_value = self.text_box.text()
            self.text_box.setText(current_value + text)
    # Connect the buttons to the button_click function



#--- Show/Run --#
if __name__ == "__main__":
    # This is where the app is created and run
    app = QApplication([])
    main_window = CalcApp()
    
    #--- Styles ---#
    main_window.setStyleSheet("""
        QWidget {
            background-color: #393E46;
            color: #FFFFFF;
        }
        # QLineEdit {
        #     background-color: #1E1E1E;
        #     color: #FFFFFF;
        #     border: 1px solid #3C3C3C;
        # }
        # QPushButton {
        #     background-color: #3C3C3C;
        #     color: #FFFFFF;
        #     border: 1px solid #3C3C3C;
        # }
        # QPushButton:hover {
        #     background-color: #4E4E4E;
        # }
    """)

    
    main_window.show()
    app.exec_()
