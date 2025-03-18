from script_definitions.EPC102.epc_tester import EPCTester
from script_definitions.modbus_client import ModbusClient

def play_test(port):
    #Kontrola správně vybraného zařízení
    device_id = 1
    script_id = 1
    try:
        R500_client = ModbusClient(port, 253)
        RMIO_client = ModbusClient(port, 254)
        R430_client = ModbusClient(port, 255)
        EPC_client = ModbusClient(port, 1)
        epc_tester = EPCTester(R500_client, RMIO_client, R430_client, EPC_client)
        # database_connector = DatabaseConnector()

        epc_tester.device_power(True)
        epc_tester.modbus_communication(True)
        epc_tester.one_wire_communication(True)

        device_modbus_id = 802
        actual_device_modbus_id = epc_tester.get_module_id()
        if (device_modbus_id == actual_device_modbus_id):
            message = f"Výsledek testu {script_id} - Jedná se o správné zařízení."
            result_test = True
            print(message)
            return result_test, message, device_id, script_id
        else:
            message = f"Výsledek testu {script_id} - Nejedná se o EPC102"
            result_test = False
            print(message)
            return result_test, message, device_id, script_id
    except:
        print(f"Test {script_id} selhal")
        return False, f"Test {script_id} selhal", device_id, script_id
# play_test("COM4")

