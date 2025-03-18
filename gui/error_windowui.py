from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QLineEdit, QMessageBox, QGroupBox, QStatusBar
from PyQt5 import uic
import sys



from settings_connector import SettingsConnector

class ErrorWindowUi(QMainWindow):
    def __init__(self, what_hide, message):
        super(ErrorWindowUi, self).__init__()
        #load the ui file
        uic.loadUi("gui\error_window_ui.ui",self)

        self.what_hide = what_hide
        self.message = message
        self.statusbar = self.findChild(QStatusBar, "statusbar")


        self.save_button = self.findChild(QPushButton, "save_button")
        self.close_button = self.findChild(QPushButton, "close_button")

        self.sub_sub_label = self.findChild(QLabel,"sub_sub_label")

        self.db_groupBox = self.findChild(QGroupBox, "db_groupBox")
        self.ftp_groupBox = self.findChild(QGroupBox, "ftp_groupBox")

        self.ftp_host_lineEdit = self.findChild(QLineEdit, "ftp_host_lineEdit")
        self.ftp_username_lineEdit = self.findChild(QLineEdit, "ftp_username_lineEdit")
        self.ftp_password_lineEdit = self.findChild(QLineEdit, "ftp_password_lineEdit")

        self.db_name_lineEdit = self.findChild(QLineEdit, "db_name_lineEdit")
        self.db_host_lineEdit = self.findChild(QLineEdit, "db_host_lineEdit")
        self.db_username_lineEdit = self.findChild(QLineEdit, "db_username_lineEdit")
        self.db_password_lineEdit = self.findChild(QLineEdit, "db_password_lineEdit")

        self.db_password_lineEdit.setEchoMode(QLineEdit.Password)
        self.ftp_password_lineEdit.setEchoMode(QLineEdit.Password)

        self.save_button.clicked.connect(self.save_config_data)
        self.close_button.clicked.connect(self.close_window)
        #show the app

        self.show_error_message(message)
        if what_hide is not None:
            self.hide_part_of_app(what_hide)

        self.show()
    def show_error_message(self, message):
        self.sub_sub_label.setText(message)
    def hide_part_of_app(self, what_hide):
        if what_hide == "ftp":
            # self.ftp_groupBox.deleteLater()
            self.ftp_groupBox.setVisible(False)
            self.setMinimumSize(0, 0)
            self.resize(377,303)
        if what_hide == "db":
            # self.db_groupBox.deleteLater()
            self.db_groupBox.setVisible(False)
            self.setMinimumSize(0, 0)
            self.resize(377, 303)
    def save_config_data(self):
        # host = self.host_lineEdit.text()
        # user = self.username_lineEdit.text()
        # passw = self.password_lineEdit.text()

        set_c = SettingsConnector()
        ftp = {
            "host": self.ftp_host_lineEdit.text(),
            "port": 21,
            "username": self.ftp_username_lineEdit.text(),
            "password": self.ftp_password_lineEdit.text(),
            "default_folder": "/AutomaticTest/"
        }
        database = {
            "dbname": self.db_name_lineEdit.text(),
            "user": self.db_username_lineEdit.text(),
            "password": self.db_password_lineEdit.text(),
            "host": self.db_host_lineEdit.text(),
            "port": "5432"
        }
        if(self.what_hide == "ftp"): #ftp settings je vpořádku
            settings = {
                "database": database
            }
            set_c.update_settings_file(settings)
        elif(self.what_hide =="db"):
            settings = {
                "ftp": ftp,
            }
            set_c.update_settings_file(settings)
        else:
            settings = {
                "ftp": ftp,
                "database": database
            }
            set_c.create_settings_file(settings)

        self.statusbar.showMessage("Konfigurace uložena", 5000)

        self.show_popop()
        self.close()
    def close_window(self):
        self.close()
    def show_popop(self):
        msg = QMessageBox()
        msg.setWindowTitle("Chyba VPN")
        msg.setText("Zkontrolujte připojení do VPN")
        msg.setIcon(QMessageBox.Warning)
        msg.buttonClicked.connect(msg.accept)  # aby se po stisknutí ok, popup zavřel

        x = msg.exec_()



    @staticmethod
    def run_application(what_hide=None,message=None):
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        error_win = ErrorWindowUi(what_hide,message)
        app.exec_()

