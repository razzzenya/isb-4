import sys
from time import time

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from card_number_recover import recover_card_num
from file_manager import FileManager
from luhn_algorithm import is_card_number_valid
from plot import draw_plot

SETTINGS_FILE = "files/settings.json"


class AppGUI(QWidget):

    def __init__(self, file_manager) -> None:
        super().__init__()
        self.initUI()
        self.file_manager = file_manager

    def initUI(self) -> None:
        self.setWindowTitle("Card number finder application")
        self.resize(300, 300)
        load_settings_btn = QPushButton("&Load settings", self)
        load_settings_btn.setToolTip("Loads .json settings file")
        load_settings_btn.clicked.connect(self.select_settings_file)
        check_card_btn = QPushButton("&Check card number for validity", self)
        check_card_btn.move(0, 30)
        check_card_btn.clicked.connect(self.check_card_number)
        recover_number_btn = QPushButton("&Recover bank card number", self)
        recover_number_btn.move(0, 60)
        recover_number_btn.clicked.connect(self.recover_number)
        draw_plot_btn = QPushButton("&Draw statistics plot", self)
        draw_plot_btn.move(0, 90)
        draw_plot_btn.clicked.connect(self.draw_statistics_plot)
        quit_btn = QPushButton("&Quit", self)
        quit_btn.move(120, 270)
        quit_btn.clicked.connect(QCoreApplication.instance().quit)

    def select_settings_file(self) -> None:
        """Method that initializes settings into a class File_manager
        """
        try:
            path = QFileDialog.getOpenFileName(
                self, "Select file", filter="*.json")[0]
            done_msg = QMessageBox()
            done_msg.setWindowTitle("Info message")
            done_msg.setText(
                f"Settings file successfully loaded from file {path}")
            done_msg.setIcon(QMessageBox.Information)
            done_msg.exec_()
            self.file_manager.settings_path = path
        except OSError:
            self.file_manager.settings_path = SETTINGS_FILE
            QMessageBox.information(
                self, "Settings", f"Settings file was not loaded from file {path}." f"The default path was applied.\nPath: {SETTINGS_FILE}")

    def check_card_number(self) -> None:
        """Method that checks if the card number is valid
        """
        if not self.file_manager.are_settings_loaded:
            msg = QMessageBox()
            msg.setWindowTitle("Info message")
            msg.setText("Settings were not loaded!")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            return
        if is_card_number_valid(self.file_manager.load_text(self.file_manager.card_number_path)):
            done_msg = QMessageBox()
            done_msg.setWindowTitle("Info message")
            done_msg.setText("Bank card number is valid.")
            done_msg.setIcon(QMessageBox.Information)
            done_msg.exec_()
        else:
            done_msg = QMessageBox()
            done_msg.setWindowTitle("Info message")
            done_msg.setText("Bank card number is not valid.")
            done_msg.setIcon(QMessageBox.Information)
            done_msg.exec_()

    def recover_number(self) -> None:
        """The method that picks up the card number and calls the output method from the FileManager class
        """
        if not self.file_manager.are_settings_loaded:
            msg = QMessageBox()
            msg.setWindowTitle("Info message")
            msg.setText("Settings were not loaded!")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            return
        start = time()
        card_number = recover_card_num(
            self.file_manager.hash, self.file_manager.last_symbols, self.file_manager.bin, int(self.file_manager.number_of_processes))
        end = time()
        if (not card_number):
            done_msg = QMessageBox()
            done_msg.setWindowTitle("Info message")
            done_msg.setText("Failed to find card number.")
            done_msg.setIcon(QMessageBox.Information)
            done_msg.exec_()
        else:
            validation_mark = is_card_number_valid(card_number)
            self.file_manager.write_output(
                f"{card_number} is {validation_mark}")
            done_msg = QMessageBox()
            done_msg.setWindowTitle("Info message")
            done_msg.setText(
                "Search completed successfully. The card number and its validity are written to the file.")
            done_msg.setIcon(QMessageBox.Information)
            done_msg.exec_()
        self.file_manager.write_statistic(
            end-start, self.file_manager.number_of_processes)
        done_msg = QMessageBox()
        done_msg.setWindowTitle("Info message")
        done_msg.setText(
            "An entry was successfully added to the statistics file.")
        done_msg.setIcon(QMessageBox.Information)
        done_msg.exec_()

    def draw_statistics_plot(self):
        if not self.file_manager.are_settings_loaded:
            msg = QMessageBox()
            msg.setWindowTitle("Info message")
            msg.setText("Settings were not loaded!")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            return
        fig = draw_plot(self.file_manager.load_statistic())
        self.file_manager.save_plot_image(fig)
        done_msg = QMessageBox()
        done_msg.setWindowTitle("Info message")
        done_msg.setText("Plot image was saved successfully.")
        done_msg.setIcon(QMessageBox.Information)
        done_msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    file_manager = FileManager()
    window = AppGUI(file_manager)
    window.show()
    sys.exit(app.exec_())
