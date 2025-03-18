import os.path
from ftplib import FTP
from settings_connector import SettingsConnector
from error_container import ErrorContainer

class FtpClient:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
            cls._initialized = True
            cls.sett_connector = SettingsConnector()
            cls.err_container = ErrorContainer()
            cls.server = cls.sett_connector.ftp_credentials["host"]
            cls.port = cls.sett_connector.ftp_credentials["port"]
            cls.username = cls.sett_connector.ftp_credentials["username"]
            cls.password = cls.sett_connector.ftp_credentials["password"]
            cls.ftp_default_folder = cls.sett_connector.ftp_credentials["default_folder"]
            cls.appdata_path = os.path.join(os.path.join(os.getenv("APPDATA"), "AutomaticTest"))


            cls.ftp = FTP()
            cls.ftp.encoding = 'utf-8'
            cls.remote_devices = []
        return cls._instance

    def get_remote_devices(self):# odstraní z názvu souboru příponu
        device_list = []
        for dev in  self.remote_devices:
            index_of_dot = dev.rfind('.')
            name_without_dot = dev[:index_of_dot]
            device_list.append(name_without_dot)
        return device_list

    def test_ftp_connection(self):
        try:
            self.ftp.connect(self.server,self.port)
            self.ftp.login(self.username, self.password)
            self.ftp.cwd(self.ftp_default_folder)
            return True
        except Exception as e:
            self.err_container.log_error(f"Nastala chyba: {e}")
            return False

    def download_device_photo(self):
        try:
            local_download_path = os.path.join(self.appdata_path, "download")
            local_device_photo_path = os.path.join(local_download_path, "device_photo")
            if not (os.path.exists(local_download_path)):
                os.mkdir(local_download_path)
            if not (os.path.exists(local_device_photo_path)):
                os.mkdir(local_device_photo_path)
            remote_folder = self.ftp_default_folder + "/" + "device_photo"
            self.ftp.connect(self.server, self.port)
            self.ftp.login(self.username, self.password)
            self.ftp.cwd(remote_folder)             #cwd - change working directory
            self.remote_devices = self.ftp.nlst()   #nlst - name list                                                  #return list of names images
            for im in self.remote_devices:
                local_im_path = os.path.join(local_device_photo_path, im)
                with open(local_im_path, 'wb') as f:
                    self.ftp.retrbinary('RETR ' + im, f.write)
            return True
        except:
            self.err_container.log_error(f"Nepovedlo se stáhnout data z FTP serveru")
            return False

    def download_schemes(self):
        try:
            local_download_path = os.path.join(self.appdata_path, "download")
            local_device_photo_path = os.path.join(local_download_path, "schemes")
            if not (os.path.exists(local_download_path)):
                os.mkdir(local_download_path)
            if not (os.path.exists(local_device_photo_path)):
                os.mkdir(local_device_photo_path)


            remote_folder = self.ftp_default_folder + "/" + "schemes"
            # self.check_ftp_connection()
            self.ftp.connect(self.server, self.port)
            self.ftp.login(self.username, self.password)
            self.ftp.cwd(remote_folder)
            self.remote_devices = self.ftp.nlst() #return list of names images

            # Stažení každého souboru
            for im in self.remote_devices:

                local_im_path = os.path.join(local_device_photo_path, im)
                with open(local_im_path, 'wb') as f:
                    self.ftp.retrbinary('RETR ' + im, f.write)
            return True
        except:
            self.err_container.log_error(f"Nepovedlo se stáhnout data z FTP serveru")
            return False

    def download_schemes_description(self):
        try:
            local_download_path = os.path.join(self.appdata_path, "download")
            local_device_photo_path = os.path.join(local_download_path, "schemes_description")
            if not (os.path.exists(local_download_path)):
                os.mkdir(local_download_path)
            if not (os.path.exists(local_device_photo_path)):
                os.mkdir(local_device_photo_path)
            remote_folder = self.ftp_default_folder + "/" + "schemes_description"

            self.ftp.connect(self.server, self.port)
            self.ftp.login(self.username, self.password)
            self.ftp.cwd(remote_folder)
            self.remote_devices = self.ftp.nlst()  # return list of names images

            # Stažení každého souboru
            for im in self.remote_devices:
                local_im_path = os.path.join(local_device_photo_path, im)
                with open(local_im_path, 'wb') as f:
                    self.ftp.retrbinary('RETR ' + im, f.write)
            return True
        except:
            self.err_container.log_error(f"Nepovedlo se stáhnout data z FTP serveru")
            return False

