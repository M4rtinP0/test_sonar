import time

from script_definitions.FCR010.fcr010_tester import FCR010Tester
from script_definitions.modbus_client import ModbusClient

def play_test(port):
    #Kontrola správně vybraného zařízení
    device_id = 2
    script_id = 104
    delay_time = 5

    try:
        R500_client = ModbusClient(port, 253)
        RMIO_client = ModbusClient(port, 254)
        R430_client = ModbusClient(port, 255)
        FCR10_client = ModbusClient(port, 1)
        fcr010_tester = FCR010Tester(R500_client, RMIO_client, R430_client, FCR10_client)
        # database_connector = DatabaseConnector()

        fcr010_tester.device_power(True)
        fcr010_tester.modbus_communication(True)
        fcr010_tester.slave_device_power(True)
        fcr010_tester.slave_modbus_communication(True)
        time.sleep(0.2)

        # while (True):
        #     overide_time = 5
        #     fcr010_tester.slave_modbus_communication(False)
        #     time.sleep(overide_time)
        #     print(fcr010_tester.get_slave_communication_state())
        #
        #     fcr010_tester.slave_modbus_communication(True)
        #     time.sleep(overide_time)
        #     print(fcr010_tester.get_slave_communication_state())


        fcr010_tester.slave_modbus_communication(False)
        time.sleep(delay_time)
        communication_state = fcr010_tester.get_slave_communication_state()
        print(communication_state)
        if not (communication_state):
            result_test = True
            message = f"Regulátor zaznamenal odpojený pokojový ovladač. Reakční doba - {delay_time} s."
        else:
            message = "Regulátor nezaznamenal odpojený pokojový ovladač"
            result_test = False

        fcr010_tester.slave_modbus_communication(True)
        time.sleep(delay_time)
        communication_state = fcr010_tester.get_slave_communication_state()
        print(communication_state)

        if(communication_state):
            result_test = True
            message = f"Regulátor zaznamenal odpojený pokojový ovladač. Reakční doba - {delay_time} s."
        else:
            message = "Regulátor nezaznamenal odpojený pokojový ovladač"
            result_test = False
        print(result_test,message)
        return result_test, message, device_id, script_id


        # device_modbus_id = 1286
        # actual_device_modbus_id = fcr010_tester.get_module_id()
        # if (device_modbus_id == actual_device_modbus_id):
        #     message = f"Výsledek testu {script_id} - Jedná se o správné zařízení"
        #     result_test = True
        #     print(message)
        #     return result_test, message, device_id, script_id
        # else:
        #     message = f"Výsledek testu {script_id} - Nejedná se o EPC102"
        #     result_test = False
        #     print(message)
        #     return result_test, message, device_id, script_id
    except:
        print(f"Test {script_id} selhal")
        return False, f"Test {script_id} selhal", device_id, script_id
# play_test("COM4")


