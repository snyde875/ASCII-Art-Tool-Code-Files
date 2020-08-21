import fix_qt_import_error

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore

from notice_dialog import NoticeDialog
from multithreading import Worker

from ascii_art import ascii_art
from k_means_image import k_means

from PIL.ImageQt import ImageQt
from wand.image import Image as ImageWand
import sys

SUPPORTED_FORMATS = [
    ".png",
    ".jpg",
    ".ppm (P6; compressed)",
    ".ppm (P3; uncompressed)",
    ".bmp",
    ".pgm"
]


def set_button_length(btns):
    """Sets the width and height of the buttons in the button panel; see below for button panel"""
    for btn in btns:
        btn.setMaximumWidth(200)
        btn.setMinimumWidth(200)
        btn.setMaximumHeight(600)


def add_widgets_to_layout(layout, widgets):
    """Adds a set of widgets to a certain layout. Variable widgets is a list holding PyQt5 widgets"""
    for widget in widgets:
        layout.addWidget(widget)


def remove_margin(layouts):
    """Sets margins to zero for every layout stored in list variable layouts"""
    for layout in layouts:
        layout.setContentsMargins(0, 0, 0, 0)


def remove_spacing(layouts):
    """Sets spacing to zero for every layout stored in list variable layouts"""
    for layout in layouts:
        layout.setSpacing(0)


def unexpected_error(error):
    """Takes an error from a try-except and displays that error to the user"""
    msg = "An unexpected error occurred.\nError: " + str(error)
    NoticeDialog(msg, True)


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle("Image Tool")
        self.setMinimumHeight(900)
        self.setMinimumWidth(1300)

        self.img_to_save = None
        self.cur_pix = None
        self.q_img = None  # A variable storing the current image to be displayed as a QImage object; used to avoid errors with garbage collection
        self.threadpool = QThreadPool()

        # Create main layout of app
        widget = QWidget()  # Main widget of the app that'll hold the top-level layout
        window_layout = QVBoxLayout()  # Final top level layout of entire application

        widget.setLayout(window_layout)  # Put top-level layout inside of widget; widget is like a placeholder
        self.setCentralWidget(widget)  # Set as central widget of the entire application

        # Create status bar and tool bar for app
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        toolbar = QToolBar()
        self.addToolBar(toolbar)

        save_btn = QPushButton("Save")
        save_btn.setShortcut(QKeySequence("Ctrl+S"))
        save_btn.pressed.connect(lambda format=".png": self.save_img(format))
        toolbar.addWidget(save_btn) # Add the save button to the toolbar

        # Create the button panel with their layouts
        btn_layout = QVBoxLayout()  # A vertical layout to horizontally align the buttons on the left of the app
        btn_panel = QHBoxLayout()  # A horizontal layout to position btn_layout with a vertical line serving as a border

        ascii_btn = QPushButton("Create ASCII art")
        convert_btn = QPushButton("Convert file format")
        k_btn = QPushButton("Group colors")
        brighten_btn = QPushButton("Brighten")
        detect_btn = QPushButton("Blur Detection")
        warp_btn = QPushButton("Warp colors")

        ascii_btn.setStatusTip("Recreate an image out of keyboard characters (ASCII characters)")
        convert_btn.setStatusTip("Convert your image file from one type to the next. Supported file types: png, jpg, "
                                 " ASCII ppm, binary ppm, bmp, and pgm")
        k_btn.setStatusTip("Take any image and recreate that image using just its core colors")

        btns = [ascii_btn, convert_btn, k_btn, brighten_btn, detect_btn, warp_btn]
        set_button_length(btns)

        line1 = QFrame()  # Will be used as a border between the btn_panel and rest of app
        line1.setFrameShape(QFrame.VLine)

        add_widgets_to_layout(btn_layout, btns)  # Put all the buttons inside the vertical button layout

        btn_panel.addLayout(btn_layout)
        btn_panel.addWidget(line1)

        # Create layout for the image to be displayed
        img_layout = QVBoxLayout()

        self.img_display = QLabel("No Image Displayed")
        self.img_display.setFont(QFont("Arial", 30))
        self.img_display.setAlignment(Qt.AlignCenter)

        line2 = QFrame()  # Will be used to separate where the image is displayed and the panel beneath it
        line2.setFrameShape(QFrame.HLine)

        img_layout.addWidget(self.img_display)
        img_layout.addWidget(line2)

        # Create layout for the stack that'll cycle through the different customization options for each app function
        stack = QStackedLayout()

        initial_display = QLabel("Click one of the side widgets to continue")
        stack.addWidget(initial_display)

        # Create ASCII layout
        ascii_layout = QFormLayout()
        ascii_layout.addRow(QLabel("Leaving the fields below blank will result in an image with black "
                                   "ASCII characters and a white background"))

        self.ascii_path = QLabel()
        upload_ascii_btn = QPushButton("Upload file")
        ascii_layout.addRow(upload_ascii_btn, self.ascii_path)

        upload_ascii_btn.pressed.connect(lambda label=self.ascii_path: self.open_img(label))

        self.start_color = QLineEdit()
        ascii_layout.addRow(QLabel("Start color:"), self.start_color)

        self.end_color = QLineEdit()
        ascii_layout.addRow(QLabel("End color:"), self.end_color)

        self.bgcolor = QLineEdit()
        ascii_layout.addRow(QLabel("Background color:"), self.bgcolor)

        create_btn_ascii = QPushButton("Create ASCII Art")
        self.ascii_status = QLabel()

        ascii_layout.addRow(create_btn_ascii, self.ascii_status)

        create_btn_ascii.pressed.connect(lambda: self.create_ascii_art())

        ascii_widget = QWidget()  # Once layout is finished, add it to the stack of layouts to switch from
        ascii_widget.setLayout(ascii_layout)

        stack.addWidget(ascii_widget)
        ascii_btn.pressed.connect(lambda n=1: stack.setCurrentIndex(n))

        # Convert file format layout
        convert_layout = QFormLayout()

        upload_convert_btn = QPushButton("Upload")
        self.convert_path = QLabel()
        convert_layout.addRow(upload_convert_btn, self.convert_path)

        upload_convert_btn.pressed.connect(lambda label=self.convert_path: self.open_img(label))

        create_convert_btn = QPushButton("Convert file format to")
        create_convert_btn.pressed.connect(self.convert_file_format)

        self.selected_format = QComboBox()
        for format in SUPPORTED_FORMATS:
            self.selected_format.addItem(format)

        convert_layout.addRow(create_convert_btn, self.selected_format)

        convert_widget = QWidget()
        convert_widget.setLayout(convert_layout)

        stack.addWidget(convert_widget)
        convert_btn.pressed.connect(lambda n=2: stack.setCurrentIndex(n))

        # k means layout
        k_layout = QFormLayout()

        upload_k_btn = QPushButton("Upload file")
        self.k_path = QLabel()
        k_layout.addRow(upload_k_btn, self.k_path)

        upload_k_btn.pressed.connect(lambda label=self.k_path: self.open_img(label))

        self.num_select = QComboBox()
        for i in range(2, 11):
            self.num_select.addItem(str(i))

        create_k_btn = QPushButton("Create and display new image")
        self.k_status = QLabel()

        create_k_btn.pressed.connect(self.create_k_img)

        k_layout.addRow(QLabel("Select the number of colors you would like your image averaged to"), self.num_select)
        k_layout.addRow(create_k_btn, self.k_status)

        k_widget = QWidget()
        k_widget.setLayout(k_layout)

        stack.addWidget(k_widget)
        k_btn.pressed.connect(lambda n=3: stack.setCurrentIndex(n))

        # Create and set up the splitter
        splitter = QSplitter()
        splitter.setOrientation(QtCore.Qt.Vertical)  # Create a vertical splitter
        splitter.splitterMoved.connect(self.dynamic_scaling)  # When splitter is moved, execute dynamic_scaling func
        splitter.setChildrenCollapsible(True)  # Top and bottom layouts can be completely collapsed

        img_widget = QWidget()
        img_widget.setLayout(img_layout)

        stack_widget = QWidget()
        stack_widget.setLayout(stack)

        splitter.addWidget(img_widget)
        splitter.addWidget(stack_widget)
        splitter.setSizes([4000, 1000])  # Top half will represent displayed image, so should be larger

        splitter_layout = QHBoxLayout()
        splitter_layout.addWidget(splitter)  # Splitter is represented as a layout

        # Add individual layouts to the central layouts
        line3 = QFrame()  # Another dividing line between the entire app and the status bar below it
        line3.setFrameShape(QFrame.HLine)

        pagelayout = QHBoxLayout()
        pagelayout.addLayout(btn_panel)
        pagelayout.addLayout(splitter_layout)

        window_layout.addLayout(pagelayout)  # Place everything into the top-level layout along with a dividing line
        window_layout.addWidget(line3)

        # Modify the margins and spacing for most of the layouts
        all_layouts = [splitter_layout, img_layout, window_layout, pagelayout, btn_layout, btn_panel]
        remove_margin(all_layouts)
        remove_spacing(all_layouts)

    # These functions are related to opening, saving, and displaying image files as well as displaying errors
    def open_img(self, label):
        """Opens an image by getting its file path and setting a QLabel's text to that file path"""

        # An array that stores a file path and the types of files that the user can select
        fname = QFileDialog.getOpenFileName(self, "Open Image", "c\\", "Image Files (*.jpg *.png *.bmp *.ppm *.pgm)")

        # Actual path to the image file
        path = QFileInfo(fname[0]).filePath()
        label.setText(path)  # Displays the opened file path

    def save_img(self, extension):
        """Saves an image with the desired extension"""
        try:
            if self.img_to_save is None:
                NoticeDialog("There is nothing to save", True)
            else:
                fname = QFileDialog.getSaveFileName(self, "Save File")
                new_file_name = QFileInfo(fname[0]).filePath() + extension  # Determine new file name by asking user

                self.img_to_save.save(new_file_name)
                self.img_to_save = None  # Since image has been saved, there is no longer an image to save
                NoticeDialog("Image was saved successfully", False)

        except ValueError:
            NoticeDialog("Image saving canceled", False)
        except Exception as err:
            unexpected_error(err)

    def dynamic_scaling(self):
        """Scales the image as the splitter is moved up and down, keeping aspect ratio of image and scaling
        its width and height"""
        pix = self.cur_pix  # Current pixmap of the image
        display = self.img_display  # The image currently being displayed on screen

        if pix is None:
            return
        else:
            w, h = display.width(), display.height()
            display.setPixmap(QPixmap(pix.scaled(w, h, Qt.KeepAspectRatio)))

    def display_img(self, display_img, label):
        """After processing new image art, this function displays the unsaved image, giving the user a preview
        before they decide to save the image"""
        self.img_to_save = display_img  # Image that can be saved is the image displayed

        self.q_img = ImageQt(display_img)  # Convert from PIL Image to QImage
        q_pix = QPixmap.fromImage(self.q_img)  # Create QPixmap from QImage

        self.cur_pix = q_pix  # Only necessary with dynamic scaling

        self.img_display.setPixmap(QPixmap(q_pix))  # Display the image by setting the pixmap of the label img_display
        self.dynamic_scaling()

        label.setText("Process complete")
        NoticeDialog("Image created successfully\nHit Ctrl+S to save your image", False)
        # self.img_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def display_error(self, error_type, error_msg):
        """Displays errors to the user that arise during the execution of threaded functions"""

        # Occurs if the user enters an invalid color when trying to create ASCII art
        if error_type == ValueError:
            NoticeDialog("One or more of the colors you have entered are invalid. Please try different input", True)

        # Occurs if the user attempts to execute a function without first uploading an image
        elif error_type == AttributeError:
            NoticeDialog("Please upload a file first", True)

        # Occurs if ImageMagick is not installed or if the image uploaded is not in binary form
        elif error_type == OSError:
            NoticeDialog("Please ensure that the format of your file is binary and that image ImageMagick is installed",
                         True)
        else:
            unexpected_error(error_msg)

    # The following functions are for image creation/manipulation
    def create_ascii_art(self):
        self.ascii_status.setText("Creating your image. Please wait.")

        label = self.ascii_status
        path = self.ascii_path.text()
        start_color = self.start_color.text()
        end_color = self.end_color.text()
        bgcolor = self.bgcolor.text()

        worker = Worker(ascii_art, label, path, start_color, end_color, bgcolor)
        worker.signals.error.connect(self.display_error)
        worker.signals.result.connect(self.display_img)

        self.threadpool.start(worker)

    def convert_file_format(self):
        """Converts the file format of an image to a different format
        This function does not change the exisiting image but instead creates a copy with the desired format"""

        try:
            path = self.convert_path.text()
            new_extension = self.selected_format.currentText()

            """Using an if-else to catch whether the user uploaded an image or not prior to launching this function
            because using try-except with an AttributeError won't work for some reason"""
            if path == "":
                NoticeDialog("Please upload a file first", True)
                return
            else:
                # Use Wand to open image since wand supports uncompressed image formats
                with ImageWand(filename=path) as img:
                    if new_extension == ".ppm (P3; uncompressed)":
                        img.format = "ppm"
                        img.compression = "no"
                        new_extension = ".ppm"
                    elif new_extension == ".ppm (P6; compressed)":
                        img.format = "ppm"
                        new_extension = ".ppm"
                    else:
                        img.format = new_extension[1:]

                    fname = QFileDialog.getSaveFileName(self, "Save File")
                    new_file_name = QFileInfo(fname[0]).filePath() + new_extension

                    img.save(filename=new_file_name)
                    return

        except Exception as err:
            unexpected_error(err)

    def create_k_img(self):
        """Takes an image and creates a copy with the colors averaged to k number of colors"""
        self.k_status.setText("Creating your image. Please wait.")

        label = self.k_status
        k = int(self.num_select.currentText())  # Number of colors user wants image reduced to
        img = self.k_path.text()  # File path to the image

        if img == "":
            label.setText("Error")
            NoticeDialog("Please upload a file first", True)
        else:
            NoticeDialog("This may take a while depending on your computer's processing speed\n"
                         "The more colors you selected, the longer it will take", False)

            worker = Worker(k_means, label, img, k)
            worker.signals.error.connect(self.display_error)
            worker.signals.result.connect(self.display_img)

            self.threadpool.start(worker)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

