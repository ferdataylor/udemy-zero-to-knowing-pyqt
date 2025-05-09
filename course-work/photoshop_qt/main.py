import os
from PyQt5.QtCore import Qt # for misc things like alignment
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QPushButton, QListWidget, QComboBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter, ImageEnhance
from utils.pyqt_detector import PyQtDetector




#--- App Settings ---#
app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("PhotoQt")
main_window.resize(900, 700) # starting size, resizeable


#--- All App Objects/Widgets ---#
btn_folder = QPushButton("Select Folder")
file_list = QListWidget()

# Buttons
btn_left = QPushButton("Left")
btn_right = QPushButton("Right")
mirror = QPushButton("Mirror")
sharpness = QPushButton("Sharpen")
gray = QPushButton("B/W")
saturation = QPushButton("Color")
contrast = QPushButton("Contrast")
blur = QPushButton("Blur")

# Dropdown box
filter_box = QComboBox()
filter_box.addItem("Original")
filter_box.addItem("Left")
filter_box.addItem("Right")
filter_box.addItem("Mirror")
filter_box.addItem("Sharpen")
filter_box.addItem("B/W")
filter_box.addItem("Color")
filter_box.addItem("Contrast")
filter_box.addItem("Blur")

picture_box = QLabel("Image will appear here")


#--- App Design and Layout ---#
master_layout = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()

col1.addWidget(btn_folder)
col1.addWidget(file_list)
col1.addWidget(filter_box)
col1.addWidget(btn_left)
col1.addWidget(btn_right)
col1.addWidget(mirror)
col1.addWidget(sharpness)
col1.addWidget(gray)
col1.addWidget(saturation)
col1.addWidget(contrast)
col1.addWidget(blur)

col2.addWidget(picture_box)


#--- Add columns to the main layout ---#
master_layout.addLayout(col1, 20) #20 is the stretch factor
master_layout.addLayout(col2, 80) #80 is the stretch factor

#--- Set the main layout to the main window ---#
main_window.setLayout(master_layout)

#--- All App Functions ---#
working_directory = ""

#--- Filter Files and Extentions ---#
def filter(files, extensions):
    results = []
    for file in files:
        for ext in extensions:
            if file.endswith(ext):
                results.append(file)
    return results


#--- Choose the Current Working Directory ---#
def getWorkingDirectory():
    global working_directory
    working_directory = QFileDialog.getExistingDirectory()
    extensions = ['.jpg', '.jpeg', '.png', '.svg']
    filenames = filter(os.listdir(working_directory), extensions)
    file_list.clear()
    for filename in filenames:
        file_list.addItem(filename)
        




class Editor():
    def __init__(self):
        self.image = None
        self.original = None
        self.filename = None
        self.save_folder = "edits/"

    def load_image(self, filename):
        self.filename = filename
        fullname = os.path.join(working_directory, self.filename)
        self.image = Image.open(fullname)
        self.original = self.image.copy()

    def save_image(self):
        path = os.path.join(working_directory, self.save_folder)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)

    def show_image(self, path):
        picture_box.hide()
        image = QPixmap(path)
        w, h = picture_box.width(), picture_box.height()
        image = image.scaled(w,h, Qt.KeepAspectRatio)
        picture_box.setPixmap(image)
        picture_box.show()

    def palettedToRgb(self):
        # NOTE: Have to convert the Paletted images when using PyQt5
        # (i.e., image in P mode) to RGB before applying filters
        detector = PyQtDetector()
        pyqt_version = detector.get_version()
        if detector.is_pyqt5():
            if self.image.mode == "P":
                self.image = self.image.convert("RGB")

    # 'lambda' is a small anonymous function that can take any number of arguments, but can only have one expression.
    #
    # When you have a bunch of filters or things you have to do, 
    # you can use a dictionary where each of the widgets' text values
    # would be the key and the value would be a function that is 
    # triggered only once.
    #
    # 'mapping' is the dictionary, and the key is the filter name (i.e., "B/W", "Color", etc.)
    # The value is a lambda function that takes the 'image' as a parameter and applies it to the filter.
    # This is a more efficient way to handle multiple filters.
    #
    # NOTE: You can also use a dictionary to map the filter names to the actual filter functions
    # in the PIL library, but for this example, we are using lambda functions.
    def transformImage(self, tranformation):
        self.palettedToRgb()
        transformation = {
            "B/W": lambda image: image.convert("L"),
            "Color": lambda image: ImageEnhance.Color(image).enhance(1.2),
            "Contrast": lambda image: ImageEnhance.Contrast(image).enhance(1.2),
            "Blur": lambda image: image.filter(ImageFilter.BLUR),
            "Sharpen": lambda image: image.filter(ImageFilter.SHARPEN),
            "Left": lambda image: image.transpose(Image.ROTATE_90),
            "Right": lambda image: image.transpose(Image.ROTATE_270),
            "Mirror": lambda image: image.transpose(Image.FLIP_LEFT_RIGHT)
        }
        transformation_function = transformation.get(tranformation)
        if transformation_function:
            self.image = transformation_function(self.image)
            self.save_image()
        self.save_image()
        image_path = os.path.join(working_directory, self.save_folder, self.filename)
        self.show_image(image_path)

    def apply_filter(self, filter_name):
        self.palettedToRgb()
        if filter_name == "Original":
            self.image = self.original.copy()
        else:
            mapping = {
                "B/W": lambda image: image.convert("L"),
                "Color": lambda image: ImageEnhance.Color(image).enhance(1.2),
                "Contrast": lambda image: ImageEnhance.Contrast(image).enhance(1.2),
                "Blur": lambda image: image.filter(ImageFilter.BLUR),
                "Sharpen": lambda image: image.filter(ImageFilter.SHARPEN),
                "Left": lambda image: image.transpose(Image.ROTATE_90),
                "Right": lambda image: image.transpose(Image.ROTATE_270),
                "Mirror": lambda image: image.transpose(Image.FLIP_LEFT_RIGHT)
            }
            filter_function = mapping.get(filter_name)
            if filter_function:
                self.image = filter_function(self.image)
                self.save_image()
                image_path = os.path.join(working_directory, self.save_folder, self.filename)
                self.show_image(image_path)
            pass
        
        self.save_image()
        image_path = os.path.join(working_directory, self.save_folder, self.filename)
        self.show_image(image_path)
# End of the class


main = Editor()


#--- Connect the filter to the function ---#
def handle_filter():
    if file_list.currentRow() >= 0: # Check if an image is selected
        select_filter = filter_box.currentText()
        main.apply_filter(select_filter)


def displayImage():
    if file_list.currentRow() >= 0:
        filename = file_list.currentItem().text()
        main.load_image(filename)
        main.show_image(os.path.join(working_directory, main.filename))


#--- Connect the objects to their functions ---#
btn_folder.clicked.connect(getWorkingDirectory)
file_list.currentRowChanged.connect(displayImage)
filter_box.currentTextChanged.connect(handle_filter) # handle_filter call here!

#--- Connect buttons to their functions ---#
gray.clicked.connect(lambda : main.transformImage("B/W"))
saturation.clicked.connect(lambda : main.transformImage("Color"))
contrast.clicked.connect(lambda : main.transformImage("Contrast"))
blur.clicked.connect(lambda : main.transformImage("Blur"))
sharpness.clicked.connect(lambda : main.transformImage("Sharpen"))
btn_left.clicked.connect(lambda : main.transformImage("Left"))
btn_right.clicked.connect(lambda : main.transformImage("Right"))
mirror.clicked.connect(lambda : main.transformImage("Mirror"))


#--- Show the main window ---#
main_window.show()
app.exec()