"""Main file, that creates Main window
   and starts Bookkeeper application"""
from controller.crud_controller import CrudController
from view.main_window import MainWindow
from PySide6.QtWidgets import QApplication


class App(QApplication):
    """Bookkeeper application class"""
    def __init__(self):
        super().__init__()
        self.controller = CrudController()
        self.view = MainWindow(self.controller)
        self.view.show()


if __name__ == "__main__":
    app = App()
    app.exec()
