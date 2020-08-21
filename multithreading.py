from PyQt5.QtCore import *
import traceback
import sys


class WorkerSignals(QObject):
    """The different custom signals that are sent out during multi-threading"""
    result = pyqtSignal(object, object)  # The result of every multi-thread function is two objects, img and label
    error = pyqtSignal(object, object)  # Error will return error type and error message, both objects


class Worker(QRunnable):
    """Generic multi-thread worker, used to help create new threads"""
    def __init__(self, func, label, *args, **kwargs):
        super(QRunnable, self).__init__()
        self.func = func  # The function to execute in the thread
        self.label = label  # A QLabel that is changed in the function connected to self.signals.result.emit (display_img function in main_app)

        self.args = args  # args represents the variables unique to each different function passed to func
        self.kwargs = kwargs
        self.signals = WorkerSignals()  # The signal to be returned

    @pyqtSlot()
    def run(self):
        try:
            img, label = self.func(self.label, *self.args)
        except:
            traceback.print_exc()  # Print error
            error_type, error_msg = sys.exc_info()[:2]

            self.label.setText("Error")
            self.signals.error.emit(error_type, error_msg)
        else:
            self.signals.result.emit(img, label)


