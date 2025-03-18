import json
import os
from error_container import ErrorContainer

class SettingsConnector:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.err_container = ErrorContainer()
            cls.settings_file_name = "settings.json"
            cls.file_path = ""
            cls.postgress_credentials = []
            cls.ftp_credentials = []
        return cls._instance

    def read_settings_file(self):
        self.create_appdata_folder()
        try:
            with open(self.file_path, "r") as file:
                settings_file = json.load(file)
                self.ftp_credentials = settings_file["ftp"]
                self.postgress_credentials = settings_file["database"]
            return True
        except FileNotFoundError:
            self.err_container.log_error(f"Soubor '{self.file_path}' nebyl nalezen.")
            return False
        except json.JSONDecodeError as e:
            self.err_container.log_error(f"Chyba při dekódování JSON souboru: {e}")
            return False
        except Exception as e:
            self.err_container.log_error(f"Nastala neočekávaná chyba: {e}")
            return False
    def create_appdata_folder(self):
        try:
            self.file_path = os.path.join(os.getenv("APPDATA"), "AutomaticTest")
            if not os.path.exists(self.file_path):
                os.mkdir(self.file_path)
            self.file_path = os.path.join(self.file_path,self.settings_file_name)
        except:
            self.err_container.log_error(f"Nepodařilo se vytvořit složku {format(self.file_path)},"
                                         f" zkontrolujte prosím svá oprávnění.")
    def create_settings_file(self, settings):
        try:
            file_path = os.path.join(os.path.join(os.getenv("APPDATA"), "AutomaticTest"),self.settings_file_name)
            with open(file_path, 'w') as js_file:
                json.dump(settings, js_file,indent=2)
        except:
            self.err_container.log_error("Nepovedlo se vytvořit settings.json soubor.")
    def update_settings_file(self, new_settings_block):
        try:
            file_path = os.path.join(os.path.join(os.getenv("APPDATA"), "AutomaticTest"), "settings.json")
            with open(file_path, 'r') as file:
                data = json.load(file)
                data.update(new_settings_block)
            with open(file_path, 'w') as js_file:
                json.dump(data, js_file,indent=2)
        except:
            self.err_container.log_error("Nepovedlo se aktualizovat settings.json soubor.")





