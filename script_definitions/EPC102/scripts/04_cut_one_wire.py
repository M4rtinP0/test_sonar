import time
from script_definitions.EPC102.epc_tester import EPCTester
from script_definitions.modbus_client import ModbusClient

def play_test(port):
    #přerušená sběrnice one-wire
    device_id = 1
    script_id = 4
    overide_time = 90

    try:
        RMIO_client = ModbusClient(port, 254)
        R500_client = ModbusClient(port, 253)
        R430_client = ModbusClient(port, 255)
        EPC_client = ModbusClient(port, 1)
        epc_tester = EPCTester(R500_client, RMIO_client, R430_client, EPC_client)

        print("one_wire_test")

        epc_tester.device_power(True)
        epc_tester.modbus_communication(True)

        epc_tester.one_wire_communication(False)
        time.sleep(overide_time)
        sensor_state = epc_tester.get_sensor_state()
        if( not sensor_state):   #když je odpojeno čislo - senzor_state == True
            message = f"Výsledek testu {script_id} - Regulátor zaznamenal odpojenou sběrnici one-wire."
            result_test = True

        else:
            message = f"Výsledek testu {script_id} - Regulátor nezaznamenal odpojenou sběrnici one-wire."
            result_test = False

        epc_tester.one_wire_communication(True)
        time.sleep(overide_time)
        sensor_state = epc_tester.get_sensor_state()
        if sensor_state:
            message = f"Výsledek testu {script_id} - Regulátor zaznamenal odpojenou sběrnici one-wire."
            result_test = True

        else:
            message = f"Výsledek testu {script_id} - Regulátor nezaznamenal odpojenou sběrnici one-wire."
            # message = f"Výsledek testu {script_id} - Jedná se o správné zařízení"

            result_test = False
        return result_test, message, device_id, script_id

    except:
        print(False, f"Test {script_id} selhal")
        return False, f"Test {script_id} selhal", device_id, script_id
# play_test("COM4")

# předělat time.sleep na tento způsob asi.
# import time
#
# def wait_for_event(timeout):
#     start_time = time.time()
#     while time.time() < start_time + timeout:
#         # provádějte jakékoli operace nebo kontroly stavu
#         pass
#
# wait_for_event(1)  # čekání na událost po dobu 1 sekundy

   # while (True):
        #     overide_time = 90
        #     epc_tester.one_wire_communication(False)
        #     time.sleep(overide_time)
        #     print(epc_tester.get_sensor_state())
        #
        #     epc_tester.one_wire_communication(True)
        #     time.sleep(overide_time)
        #     print(epc_tester.get_sensor_state())

