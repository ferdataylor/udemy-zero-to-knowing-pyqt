import sys
import os

from PyQt5.QtCore import Qt # for misc things like alignment
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTreeView, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class FinanceApp(QMainWindow):
    def __init__(self):
        # Inherit eveything from our FinanceApp class
        # This initializes FinanceApp as a superclass as well as activating the QMainWindow
        # 1.  Activating my superclass QMainWindow
        # 2.  Giving my superclass my class that we just designed (FinanceApp)
        # This is how we setup inheritance for our QMainWindow
        super(FinanceApp, self).__init__()
        
        self.setWindowTitle("Interest Rate Calculator")
        self.resize(800, 600)
        
        main_window = QWidget()
        
        # Creation of our input fields
        self.rate_text = QLabel("Interest Rate (%):")
        self.rate_input = QLineEdit()
        
        self.initial_text = QLabel("Initial Investment ($):")
        self.initial_input = QLineEdit()
        
        self.years_text = QLabel("Years to Invest:")
        self.years_input = QLineEdit()
        
        # Creation of our TreeView
        self.model = QStandardItemModel()
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        
        # Creation of our buttons
        self.calc_button = QPushButton("Calculate")
        self.save_button = QPushButton("Save")
        self.clear_button = QPushButton("Clear")
        
        # Creation of our chart
        # self.figure = QLabel("---CHART WILL GO HERE---")
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        # self.figure = FigureCanvas(plt.Figure()) #<-- More succinct way to create a figure
        
        
        # Create our master layout
        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        
        self.col1 = QVBoxLayout()
        self.col2 = QVBoxLayout()
        
        
        # Add our input widgets to the layout
        self.row1.addWidget(self.rate_text)
        self.row1.addWidget(self.rate_input)
        
        self.row1.addWidget(self.initial_text)
        self.row1.addWidget(self.initial_input)
        
        self.row1.addWidget(self.years_text)
        self.row1.addWidget(self.years_input)
        
        # Add our tree view widget to the layout
        self.col1.addWidget(self.tree_view)
        
        # Add our buttons to the layout
        self.col1.addWidget(self.calc_button)
        self.col1.addWidget(self.save_button)
        self.col1.addWidget(self.clear_button)
        
        # Add our chart to the layout
        # NOTE: Create the figure then "wrap" it in a canvas
        self.col2.addWidget(self.canvas)
        
        
        # Add our 2 columns to the 2nd row
        self.row2.addLayout(self.col1, 30)
        self.row2.addLayout(self.col2, 70)
        
        # Add our rows to the master layout
        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        
        # Add our master layout to the main window
        main_window.setLayout(self.master_layout)
        self.setCentralWidget(main_window)
        
        self.calc_button.clicked.connect(self.calculate_interest)
        self.save_button.clicked.connect(self.save_data)
        self.clear_button.clicked.connect(self.reset)
    
    
    def clear_input(self):
        self.rate_input.clear()
        self.initial_input.clear()
        self.years_input.clear()
        
        # Clear the QTreeView
        self.model.clear()
    
    
    # ADD INTEREST CALCULATION TO QTREEVIEW
    # 1. Convert all of our input fields to numbers
    # 2. Catch any errors that may occur
    # 3. For every year, multiplythe total investment by the interest rate
    #    total * (interest rate / 100)
    # 4. Create TreeView items with QStanardItem
    # 5. Add item_year and item_total to our QTreeView as a List
    # 6. Create a Save Button and add it to the Layout
    #
    def calculate_interest(self):
        if self.model.rowCount() > 0:
            self.model.clear()
        
        interest_rate = 0
        try:
            interest_rate = float(self.rate_input.text())
            initial_investment = float(self.initial_input.text())
            num_years = int(self.years_input.text())
        except ValueError:
            self.model.clear()
            self.model.setHorizontalHeaderLabels(["Error"])
            self.model.appendRow(QStandardItem("Please enter valid numbers."))
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers.")
            return
        
        # The way it's being calculated in the lesson        
        total = initial_investment
        for year in range(1, num_years + 1):
            total += total * (interest_rate/100)
            item_year = QStandardItem(str(year))
            item_total = QStandardItem("{:.2f}".format(total))
            self.model.appendRow([item_year, item_total])
        
        # Update the chart with our data
        self.figure.clear()
        ax = self.figure.subplots() #<-- can have multiple subplots
        years = list(range(1, num_years + 1))
        totals = [initial_investment * ((1 + interest_rate/100) ** year) for year in years]
        
        # Plotting the data
        ax.plot(years, totals)
        ax.set_title("Investment Growth Over Time")
        ax.set_xlabel("Years")
        ax.set_ylabel("Total Investment ($)")
        ax.grid()
        self.canvas.draw()
    
    
    # AI: save the QTreeView to a CSV file
    def ai_save_to_csv(self):
        # Get the file path to save the CSV
        file_path = os.path.join(os.getcwd(), "interest_rate_data.csv")
        
        # Open the file in write mode
        with open(file_path, "w") as file:
            # Write the header
            file.write("Year,Total\n")
            
            # Write the data from the QTreeView
            for row in range(self.model.rowCount()):
                year_item = self.model.item(row, 0)
                total_item = self.model.item(row, 1)
                file.write(f"{year_item.text()},{total_item.text()}\n")
        
        QMessageBox.information(self, "Save Successful", f"Data saved to {file_path}")
    
    
    # Course: save the QTreeView to a CSV file in a subfolder
    def save_data(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            # Create a subfolder within the selected directory
            folder_path = os.path.join(dir_path, "Saved/")
            os.makedirs(folder_path, exist_ok=True)
            
            # Save the results to a CSV file within the subfolder
            file_path = os.path.join(folder_path, "results.csv")
            with open(file_path, "w") as file:
                file.write("Year, Total\n")
                for row in range( self.model.rowCount() ):  #<-- our treeview is inside the model
                    year = self.model.index(row, 0).data()
                    total = self.model.index(row, 1).data()
                    file.write("{}, {}\n".format(year, total))
            
            plt.savefig(os.path.join(folder_path, "chart.png"))
            
            QMessageBox.information(self, "Save Results", "Results saved successfully in '{}'".format(folder_path))
        else:
            QMessageBox.warning(self, "Save Results", "No directory selected.")
    
    
    # Clear the QLineEdit fields
    def reset(self):
        self.rate_input.clear()
        self.initial_input.clear()
        self.years_input.clear()
        self.model.clear()
        
        self.figure.clear()
        self.canvas.draw() #<-- Clears the chart
        

#--- MAIN FUNCTION ---#
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceApp()
    window.show()
    sys.exit(app.exec_())