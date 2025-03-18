import time
from script_definitions.EPC102.epc_tester import EPCTester
from script_definitions.modbus_client import ModbusClient

def play_test(port):
    #Provozní módy - Modbus
    device_id = 1
    script_id = 5

    try:
        RMIO_client = ModbusClient(port, 254)
        R500_client = ModbusClient(port, 253)
        R430_client = ModbusClient(port, 255)
        EPC_client = ModbusClient(port, 1)
        epc_tester = EPCTester(R500_client, RMIO_client, R430_client, EPC_client)

        print("presence_mode_modbus")
        epc_tester.device_power(True)
        epc_tester.modbus_communication(True)
        epc_tester.one_wire_communication(True)
        result_test = False
        message = ""
        wait_time = 3
        # TODO: zakázat změnu pomocí okna
        epc_tester.set_presence_mode("day")
        time.sleep(wait_time)
        actual_presence_mode = epc_tester.get_actual_presence_mode()
        print(actual_presence_mode)
        if (actual_presence_mode == "day"):
            day_result = True
        else:
            day_result = False

        epc_tester.set_presence_mode("night")
        time.sleep(wait_time)
        actual_presence_mode = epc_tester.get_actual_presence_mode()
        print(actual_presence_mode)
        if (actual_presence_mode == "night"):
            night_result = True
        else:
            night_result = False

        epc_tester.set_presence_mode("off")
        time.sleep(wait_time)
        actual_presence_mode = epc_tester.get_actual_presence_mode()
        print(actual_presence_mode)
        if (actual_presence_mode == "off"):
            off_result = True
        else:
            off_result = False

        # day_result = False
        # night_result = False
        # off_result = False

        if day_result and night_result and off_result:
            result_test = True
            message = f"Výsledek testu {script_id} - Regulátor reaguje správně na všechny změny provozních režimů."
        else:
            result_test = False
            results = day_result, night_result, off_result
            error_string = ""
            if results[0] == False:
                error_string = "den"
            if results[1] == False:
                error_string = error_string + " noc "
            if results[2] == False:
                error_string = error_string + "vypnuto"
            message = f"Výsledek testu {script_id} - Regulátor nereaguje správně na požadované změny do těchto provozních režimů: [{error_string}]."
            # message = f"Výsledek testu {script_id} - Jedná se o správné zařízení."

        print(message)
        return result_test, message, device_id, script_id
    except:
        print(False, f"Test {script_id} selhal")
        return False, f"Test {script_id} selhal", device_id, script_id
# play_test("COM4")

# while True:
#     epc_tester.set_presence_mode("day")
#     time.sleep(5)
#     print(epc_tester.get_actual_presence_mode())
#
#     epc_tester.set_presence_mode("night")
#     time.sleep(5)
#     print(epc_tester.get_actual_presence_mode())
#
#     epc_tester.set_presence_mode("off")
#     time.sleep(5)
#     print(epc_tester.get_actual_presence_mode())
