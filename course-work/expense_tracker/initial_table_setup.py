#--- Import Modules ---#
import os
from PyQt5.QtCore import Qt # for misc things like alignment
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QTableWidget, QHBoxLayout, QVBoxLayout



#--- App Class ---#
class ExpenseApp(QWidget):  #QWidget is the base class here
    def __init__(self):
        # Call the parent class constructor
        super().__init__()

        # Main App Objects & Settings
        self.resize(550, 500)
        self.setWindowTitle("Expense Tracker 2.0")
    
    
    
        # Create Objects
        self.date_box = QDateEdit()
        self._dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()
        
        self.add_button = QPushButton("Add Expense")
        self.delete_button = QPushButton("Delete Expense")
        
        self.table = QTableWidget()
        self.table.setColumnCount(5) #Id, Date, Category, Amount, Description
        header_labels = ["ID", "Date", "Category", "Amount", "Description"]
        self.table.setHorizontalHeaderLabels(header_labels)
        
        
        #--- Design App with Layouts ---#
        
        # Set up the ROWS
        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()

        self.row1.addWidget(QLabel("Date:"))
        self.row1.addWidget(self.date_box)
        self.row1.addWidget(QLabel("Category:"))
        self.row1.addWidget(self._dropdown)

        self.row2.addWidget(QLabel("Amount:"))
        self.row2.addWidget(self.amount)
        self.row2.addWidget(QLabel("Description:"))
        self.row2.addWidget(self.description)
        
        self.row3.addWidget(self.add_button)
        self.row3.addWidget(self.delete_button)
        
        # Add the rows to the master layout
        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addLayout(self.row3)
        
        # # Set up the table formatting
        # self.table.setColumnWidth(0, 50)
        # self.table.setColumnWidth(1, 100)
        # self.table.setColumnWidth(2, 100)
        # self.table.setColumnWidth(3, 100)
        # self.table.setColumnWidth(4, 150)
        # self.table.setRowCount(0)
        # self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        # self.table.setSelectionBehavior(QTableWidget.SelectRows)
        # self.table.setSelectionMode(QTableWidget.SingleSelection)
        # self.table.setAlternatingRowColors(True)
        # self.table.setStyleSheet("QTableWidget::item:selected { background-color: #A0C4FF; }")
        # self.table.setStyleSheet("QTableWidget::item { background-color: #FFFFFF; }")
        # self.table.setStyleSheet("QTableWidget::item { border: 1px solid #000000; }")
        # self.table.setStyleSheet("QTableWidget::item { padding: 5px; }")
        # self.table.setStyleSheet("QTableWidget::item { font-size: 14px; }")
        # self.table.setStyleSheet("QTableWidget::item { font-family: Arial; }")
        # self.table.setStyleSheet("QTableWidget::item { color: #000000; }")
        
        # Add the table to the master layout
        self.master_layout.addWidget(self.table)
        
        # Set the master layout to the main window
        self.setLayout(self.master_layout)
        




# Run the App
if __name__ == "__main__":
    app = QApplication([])
    window = ExpenseApp()
    window.show()
    app.exec_()





#--- Notes ---#
# - The QTableWidget is a powerful widget that allows you to display and edit tabular data in a grid format.
# - The QTableWidget is a subclass of QTableView, which is a more general-purpose table view that can be used to display data from a model.
# - The QTableWidget is a good choice for simple applications where you want to display and edit data in a table format.
 
