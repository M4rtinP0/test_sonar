from PyQt5.QtWidgets import QMainWindow,QCheckBox, QScrollArea, QTextBrowser, QComboBox, QAction, QMenu, QVBoxLayout, QApplication, QLabel, QPushButton, QLineEdit, QMessageBox, QWidget, QStatusBar
from PyQt5 import uic
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QPixmap

from functools import partial
import serial.tools.list_ports
import sys
import os

from ftp_client import FtpClient
from database_connector import DatabaseConnector
from script_definitions.script_starter import ScriptStarter
from script_definitions.modbus_client import ModbusClient

class MainWindowUi(QMainWindow):
    def __init__(self):
        super(MainWindowUi, self).__init__()
        uic.loadUi("gui\main_window_ui.ui", self)
        self.setWindowTitle("Automatizované testy FW")

        self.findPorts_Action = self.findChild(QAction,"findPorts_Action")
        self.USB_port_Qmenu = self.findChild(QMenu,"USB_port_Qmenu")
        self.device_foto_label = self.findChild(QLabel,"device_foto_label")
        self.device_comboBox = self.findChild(QComboBox,"device_comboBox")
        self.device_textBrowser = self.findChild(QTextBrowser, "device_textBrowser")
        self.schema_foto_label = self.findChild(QLabel,"schema_foto_label")
        self.scrollArea = self.findChild(QScrollArea, "scrollArea")
        self.scrollAreaWidgetContents = self.findChild(QWidget,"scrollAreaWidgetContents")
        self.select_all_checkBox = self.findChild(QCheckBox,"select_all_checkBox")
        self.start_script_pushButton = self.findChild(QPushButton,"start_script_pushButton")
        self.script_description_textBrowser = self.findChild(QTextBrowser, "script_description_textBrowser")
        self.statusbar = self.findChild(QStatusBar, "statusbar")

        self.label_2 = self.findChild(QLabel, "label_2")

        self.local_download_path = os.path.join(os.path.join(os.getenv('APPDATA'), "AutomaticTest"), "download")
        self.default_device = "EPC102"
        self.set_default_device(self.default_device)

        self.fill_comboBox()

        #function connection
        self.device_comboBox.currentIndexChanged.connect(self.onComboBoxChange)
        self.select_all_checkBox.stateChanged.connect(self.change_state_of_all_checkboxs)
        self.start_script_pushButton.clicked.connect(self.start_scenarios)
        self.findPorts_Action.triggered.connect(self.find_actual_port)

        self.checkboxs_dictionary = {}
        self.fill_checkbox_dictionary()
        self.checkbox_states = []
        self.actual_device = self.default_device
        self.db_connector = DatabaseConnector()
        self.actual_script_info = []
        self.actual_port_name = ""
        self.formatted_text = ''' 
        <p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:11pt; font-weight:600;">Po vybrání scénáře se zobrazí jeho popis</span></p>
        '''#format is from QTdesigne
        self.generate_checkboxs(self.default_device)
        self.find_actual_port()

        self.show()

    def find_actual_port(self):
        com_ports = serial.tools.list_ports.comports()
        port_list = [port.device for port in com_ports]
        self.generate_actual_coms(port_list)
    def generate_actual_coms(self,port_list):
        self.clearActions()
        for item in port_list:
            new_action = QAction(f"{item}",self)
            new_action.triggered.connect(partial(self.return_port_name, item))
            self.USB_port_Qmenu.addAction(new_action)
    def return_port_name(self,port):
        self.actual_port_name = port
    def clearActions(self):
        # Clear all actions from the 'File' menu
        if self.USB_port_Qmenu:
            self.USB_port_Qmenu.clear()
    #methods
    def onComboBoxChange(self):
        self.actual_device = self.device_comboBox.currentText()
        self.load_html_file(self.actual_device)
        self.load_device_photo(self.actual_device)
        self.load_schemes_description(self.actual_device)
        self.generate_checkboxs(self.actual_device)
        self.select_all_checkBox.setChecked(False)
        self.script_description_textBrowser.clear()
        self.script_description_textBrowser.setHtml(self.formatted_text)
    def change_state_of_all_checkboxs(self):
        state_of_main_checkbox = self.select_all_checkBox.isChecked()
        for checkbox in self.scrollAreaWidgetContents.findChildren(QCheckBox):
            if (state_of_main_checkbox):
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)
        self.script_description_textBrowser.clear()
        self.script_description_textBrowser.setHtml(self.formatted_text)
    def start_scenarios(self):
        if(self.actual_port_name==""):
            self.show_pop()
        else:
            scripts = self.return_state_of_checkboxs()
            scripts_to_play=[]
            for item in scripts:
                if(item[1]==True):
                    script=item[0]
                    script = script[:-9]        #obsahuje na konci - checkbox - proto se to odstranuje
                    # script = script+".py"
                    scripts_to_play.append(script)
            if(len(scripts_to_play)>0):
                # self.label_2.setText("Probíhá test")
                # self.statusbar.showMessage("Probíhá test - nevypínejte aplikaci.")
                # self.statusbar.repaint()
                # self.label_2.repaint()
                scr_starter = ScriptStarter(scripts_to_play,self.actual_device,self.actual_port_name,self)
                scr_starter.run_scripts()
    def show_pop(self):
        msg = QMessageBox()
        msg.setWindowTitle("Check COM")
        msg.setText("V nastavení vyberte COM")
        msg.setIcon(QMessageBox.Warning)
        msg.buttonClicked.connect(msg.accept)  # aby se po stisknutí ok, popup zavřel

        x = msg.exec_()
    def return_state_of_checkboxs(self): #vložit do funkce start_test - ta bude spouštět scripty.
        checkbox_states = []
        for checkbox in self.scrollAreaWidgetContents.findChildren(QCheckBox):
            checkB_name = checkbox.objectName()
            newCB_state = [f"{checkB_name}", checkbox.isChecked()]
            checkbox_states.append(newCB_state)
        # print(checkbox_states)
        return checkbox_states
    def generate_checkboxs(self, device_name):
        self.clear_scrollarea_layout()
        is_returned, script_names = self.db_connector.return_script_names(device_name)
        # script_names.reverse() # aby se zobrazily testy od test_id 1
        # print(script_names)
        layout = self.scrollAreaWidgetContents.layout()
        if (is_returned==True):
            for script_name in script_names:
                # v script_name je např. 'Modbusové adresy' - zobrazí se v aplikaci - je to i v databázi
                # checkboxs_dictionary vrátí 'modbus_adress_checkBox'
                try:
                    checkbox_attrib_name = self.checkboxs_dictionary[script_name]
                    checkbox_instance = QCheckBox(script_name, self)
                    checkbox_instance.setObjectName(f"{checkbox_attrib_name}")
                    layout.addWidget(checkbox_instance)
                    checkbox_instance.clicked.connect(self.checkbox_clicked)
                except:
                    self.statusbar.showMessage("Je potřeba zkontrolovat názvy testů v databázi",5000)
                    self.statusbar.repaint()
    def checkbox_clicked(self):
        # Získání aktuálního jména checkboxu
        checkbox_instance = self.sender()
        checkbox_name = checkbox_instance.objectName()
        checkbox_text = checkbox_instance.text()
        is_return, script_info = self.db_connector.return_script_info(self.actual_device, checkbox_text)
        if(is_return):
            self.actual_script_info = script_info[0]
            print(self.actual_script_info)
            formatted_text = f'''<p><font size='5'>{self.actual_script_info[1]}</font><br><br>
            <font size='4'>{self.actual_script_info[2]}</font><br><br>
            <font size='4'>použité registry - {self.actual_script_info[3]}</font></p>'''
            self.script_description_textBrowser.setHtml(formatted_text)
    def fill_checkbox_dictionary(self):
        self.checkboxs_dictionary["Kontrola správně vybraného zařízení"] = "01_default_test_checkBox"
        self.checkboxs_dictionary["Test modbusových adres"] = "02_modbus_address_checkBox"
        self.checkboxs_dictionary["Test okenního kontaktu"] = "03_window_contact_checkBox"
        self.checkboxs_dictionary["Přerušená sběrnice k pokojovému regulátoru"] = "04_cut_communication_checkBox"
        self.checkboxs_dictionary["Přerušený one-wire"] = "04_cut_one_wire_checkBox"
        self.checkboxs_dictionary["Provozní módy - modbus"] = "05_presence_mode_modbus_checkBox"
        self.checkboxs_dictionary["Provozní módy - okenní kontakt"] = "06_presence_mode_window_sensor_checkBox"
        self.checkboxs_dictionary['Topení sepnuto manuálně'] = "07_manual_heat_checkBox"
        self.checkboxs_dictionary["Topení sepnuto manuálně - PWM sekvence, polarita NC"] = "08_manual_heat_pwm_nc_checkBox"





        self.checkboxs_dictionary['Provozní módy'] = "presence_mode_checkBox"
        self.checkboxs_dictionary['Testování digitálních výstupů'] = "di_test_checkBox"
        self.checkboxs_dictionary['Testování analogových výstupů'] = "ai_test_checkBox"
        self.checkboxs_dictionary['Testování digitálních vstupů'] = "do_test_checkBox"
        self.checkboxs_dictionary['Testování analogových vstpů'] = "ao_test_checkBox"
        self.checkboxs_dictionary['Baudrate'] = "baudrate_checkBox"
        # self.checkboxs_dictionary['Testování schodovité funkce'] = "05_presence_mode_modbus_checkBox"
    def clear_scrollarea_layout(self):
        for widget in self.scrollAreaWidgetContents.findChildren(QWidget):
            widget.setParent(None)
    def load_device_photo(self,selected_option):
        device_photo_path = os.path.join(self.local_download_path,"device_photo")
        device_path = os.path.join(device_photo_path,selected_option)
        pixmap = QPixmap(device_path+".jpeg")
        self.device_foto_label.setPixmap(pixmap)
    def load_html_file(self, device_name):
        download_path = self.local_download_path
        schemes_description_path = os.path.join(download_path,"schemes_description")
        device_path = os.path.join(schemes_description_path,device_name+".html")
        file = QFile(device_path)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            html_content = stream.readAll()
            file.close()
            self.device_textBrowser.setHtml(html_content)
    def load_schemes_description(self,device_name):
        schemes_path = os.path.join(self.local_download_path, "schemes")
        device_path = os.path.join(schemes_path, device_name)
        pixmap = QPixmap(device_path + ".png")
        self.schema_foto_label.setPixmap(pixmap)
    def set_default_device(self,device_name):
        self.load_device_photo(device_name)
        self.load_html_file(device_name)
        self.load_schemes_description(device_name)
    def fill_comboBox(self):
        self.device_comboBox.clear()
        ftp_c = FtpClient()
        self.device_comboBox.addItems(ftp_c.get_remote_devices())

    @staticmethod
    def run_application():
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        error_win = MainWindowUi()
        app.exec_()