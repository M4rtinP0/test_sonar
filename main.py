from error_container import ErrorContainer
from settings_connector import SettingsConnector
from ftp_client import FtpClient
from gui.error_windowui import ErrorWindowUi
from gui.main_window_ui import MainWindowUi
from database_connector import DatabaseConnector

if __name__ == "__main__":
    err_container = ErrorContainer()
    sett_connector = SettingsConnector()
    if (sett_connector.read_settings_file()):
        ftp_c = FtpClient()
        db_c = DatabaseConnector()
        is_ftp_connected = ftp_c.test_ftp_connection()
        is_db_connected = db_c.test_database_connection()
        if (is_ftp_connected and is_db_connected):
            if (ftp_c.download_device_photo() and ftp_c.download_schemes() and ftp_c.download_schemes_description()):
                MainWindowUi.run_application()
        if (is_ftp_connected and not is_db_connected):
            ErrorWindowUi.run_application("ftp","Nepovedlo se připojit k databázi")
        if (not is_ftp_connected and is_db_connected):
            ErrorWindowUi.run_application("db","Nepovedlo se připojit k FTP serveru")
        if (not is_ftp_connected and not is_db_connected):
            ErrorWindowUi.run_application(None,"Nepovedlo se připojit k databázi a FTP serveru")
    else:
        ErrorWindowUi.run_application(None,"Nebyl nalezen konfigurační soubor")
    print(err_container.get_errors())




























