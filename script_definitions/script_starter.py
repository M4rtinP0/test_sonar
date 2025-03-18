import os
import importlib
import time
from database_connector import DatabaseConnector

class ScriptStarter:
    def __init__(self, scripts_to_play, actual_device, actual_port_name, main_win):
        self.scripts_to_play = scripts_to_play
        self.device_to_test = actual_device
        self.actual_port_name = actual_port_name
        self.python_files = []
        self.import_needed_scripts()
        self.db_con = DatabaseConnector()
        self.main_win = main_win

    def import_needed_scripts(self):
        device = self.device_to_test
        sripts_path = f"script_definitions/{device}/scripts"    #path in project not in appdata directory
        for file in os.listdir(sripts_path):
            if file.endswith(".py"):
                file = file[:-3]
                module_name = f"script_definitions.{self.device_to_test}.scripts.{file}"
                module = importlib.import_module(module_name)
                setattr(self,file,module)
                print(module)
                self.python_files.append(file)

    def run_scripts(self):
        result_test = False
        message = ""
        for module_name in self.python_files:
            if module_name in self.scripts_to_play:
                module = getattr(self, module_name)
                if hasattr(module, "play_test"):  # Ověřit, zda modul obsahuje požadovanou metodu
                    method = getattr(module, "play_test")

                    self.main_win.statusbar.showMessage("Probíhá test - nevypínejte aplikaci.")
                    self.main_win.statusbar.repaint()

                    result_test, message, device_id, script_id = method(self.actual_port_name)  # Volat metodu
                    self.db_con.write_test_result_to_database(device_id,script_id, result_test, message)
                    self.main_win.statusbar.showMessage(message,2000)
                    self.main_win.statusbar.repaint()
                    time.sleep(2)

