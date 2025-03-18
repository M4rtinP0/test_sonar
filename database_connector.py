from settings_connector import SettingsConnector
from error_container import ErrorContainer
import psycopg2
class DatabaseConnector:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
            cls.sett_connector = SettingsConnector()
            cls.err_container = ErrorContainer()
            cls.dbname = cls.sett_connector.postgress_credentials["dbname"]
            cls.user = cls.sett_connector.postgress_credentials["user"]
            cls.password = cls.sett_connector.postgress_credentials["password"]
            cls.host = cls.sett_connector.postgress_credentials["host"]
            cls.port = cls.sett_connector.postgress_credentials["port"]
            cls.remote_devices = []
        return cls._instance

    def test_database_connection(self):
        try:
            connection = psycopg2.connect(
                dbname = self.dbname,
                user = self.user,
                password = self.password,
                host = self.host,
                port = self.port
            )
            cursor = connection.cursor()
            cursor.execute("SELECT version();")                                                           # vypíše verzi databázového systému
            result = cursor.fetchone()
            print("Připojení k databázi úspěšné.")
            cursor.close()
            connection.close()
            return True
        except Exception as e:
            self.err_container.log_error(f"Chyba při připojování k databázi: {e}")
            return False


    def write_test_result_to_database(self, device_id, script_id, test_result, result_comment):
        try:
            connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            cursor = connection.cursor()
            query = "INSERT INTO test_log (device_id, script_id, test_result, result_comment) VALUES (%s, %s, %s, %s);"
            val = (device_id, script_id, test_result, result_comment)
            cursor.execute(query, val)
            connection.commit()
            return True
        except Exception as e:
            print(f"Nepovedl se zapsat výsledek do databáze - {e}")
            return False

    def return_script_names(self, device_name):
        try:
            connection = psycopg2.connect(
                dbname = self.dbname,
                user = self.user,
                password = self.password,
                host = self.host,
                port = self.port
            )
            cursor = connection.cursor()
            cursor.execute(f'''
            SELECT script.script_name FROM device
            INNER JOIN script ON device.device_id = script.device_id
            WHERE device.device_name = '{device_name}' 
            ORDER BY script.script_id
            ''')
            result = cursor.fetchall()

            # print(result)
            result_list = [item[0] for item in result]
            # print(result_list)
            return [True,result_list]
        except:

            return False

    def return_script_info(self, device_name, script_name):
        try:
            connection = psycopg2.connect(
                dbname = self.dbname,
                user = self.user,
                password = self.password,
                host = self.host,
                port = self.port
            )
            cursor = connection.cursor()
            cursor.execute(f'''
            SELECT device.device_name, script.script_name, script.script_description, script.registers FROM device 
            INNER JOIN script ON device.device_id = script.device_id 
            WHERE device.device_name = '{device_name}' AND script.script_name = '{script_name}'
            ''')
            result = cursor.fetchall()
            return [True, result]
        except Exception as e:

            return [False, None]



