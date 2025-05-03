#--- Import Modules ---#
import sys
from PyQt5.QtCore import QDate # for misc things like alignment
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtGui import QIcon, QFont



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
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()
        
        self.add_button = QPushButton("Add Expense")
        self.delete_button = QPushButton("Delete Expense")
        
        self.add_button.clicked.connect(self.add_expense)
        # self.delete_button.clicked.connect(self.delete_expense)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5) #Id, Date, Category, Amount, Description
        header_labels = ["ID", "Date", "Category", "Amount", "Description"]
        self.table.setHorizontalHeaderLabels(header_labels)
        
        dropdown_items = ["Select Category", "Food", "Transportation", "Rent", "Shopping", "Entertainment", "Bills", "Other"]
        self.dropdown.addItems(dropdown_items)
        self.dropdown.setCurrentIndex(0)
        self.dropdown.model().item(0).setEnabled(False)  # Disable the placeholder item
        self.dropdown.setEditable(False)
        self.dropdown.setInsertPolicy(QComboBox.InsertAtTop)
        self.dropdown.setDuplicatesEnabled(False)
        self.dropdown.setMaxVisibleItems(10)
        self.dropdown.setMinimumContentsLength(10)            
        
        
        #--- Design App with Layouts ---#
        
        # Set up the ROWS
        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()
        
        self.row1.addWidget(QLabel("Date:"))
        self.row1.addWidget(self.date_box)
        self.row1.addWidget(QLabel("Category:"))
        self.row1.addWidget(self.dropdown)
        
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
        
        self.setup_db_connection()
        self.load_table()
        
    def setup_db_connection(self):        
            # Setup Database Connection
            database = QSqlDatabase.addDatabase("QSQLITE")
            database.setDatabaseName("udemy-zero-to-knowing-pyqt/course-work/expense_tracker/expense.db")
            if not database.open():
                QMessageBox.critical(None, "Database Error", "Unable to open database")
                print("Unable to open database")
                sys.exit(1)
            
            # Create the table if it doesn't exist
            query = QSqlQuery()
            query.exec_("""
                        CREATE TABLE IF NOT EXISTS expenses (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            date TEXT,
                            category TEXT,
                            amount REAL,
                            description TEXT
                        )
                        """)
        
    
    #-- Create/Load the Database --#
    
    # Steps to Load Expenses Table
    #
    # 1.  Clear the current Table - .setRowCount()
    # 2.  Create a query to SELECT everythig FROM our table - QSqlQuery
    # 3.  Create a Loop to run as long as there are ore rows in the table - .next()
    # 4.  Retrieve the value from each column in the table - .value(#)
    # 5.  Insert the collected data from #4 into a new row - .insertRow(#)
    # 6.  Increase row counter - .rowCount()
    def load_table(self):
        # Clear the table
        self.table.setRowCount(0)
        query = QSqlQuery("SELECT * FROM expenses")
        row = 0
        
        while query.next():
            expense_id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            amount = query.value(3)
            description = query.value(4)
            
            # Insert the data into the table
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(expense_id)))
            self.table.setItem(row_position, 1, QTableWidgetItem(date))
            self.table.setItem(row_position, 2, QTableWidgetItem(category))
            self.table.setItem(row_position, 3, QTableWidgetItem(str(amount)))
            self.table.setItem(row_position, 4, QTableWidgetItem(description))
    
    
    # Steps to Add New Expenses
    #
    # 1.  Gather the information entered in the input boxes
    # 2.  Insert the expense into the database
    # 3.  Clear the input fields for the next expense entry
    # 4.  Load in the updated data from the database
    def add_expense(self):        
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()
        
        query = QSqlQuery()
        query.prepare("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)")
        
        # Send/push informtion to the database
        query.addBindValue(date)
        query.addBindValue(category)
        query.addBindValue(amount)
        query.addBindValue(description)
        
        # Execute the query
        if not query.exec_():
            QMessageBox.critical(None, "Database Error", "Unable to add expense")
            print("Unable to add expense")
            return
        
        # Load the categories from the database
        query.exec_("SELECT DISTINCT category FROM expenses")
        while query.next():
            category = query.value(0)
            self.dropdown.addItem(category)
        
        # Clear the input fields
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()
        
        self.load_table()



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
 
