import time
from script_definitions.EPC102.epc_tester import EPCTester
from script_definitions.modbus_client import ModbusClient

def play_test(port):
    #Provozní módy - okenní kontakt
    device_id = 1
    script_id = 6

    try:
        RMIO_client = ModbusClient(port, 254)
        R500_client = ModbusClient(port, 253)
        R430_client = ModbusClient(port, 255)
        EPC_client = ModbusClient(port, 1)
        epc_tester = EPCTester(R500_client, RMIO_client, R430_client, EPC_client)

        print("presence_mode_window_senzor")
        epc_tester.device_power(True)
        epc_tester.modbus_communication(True)
        epc_tester.one_wire_communication(True)
        epc_tester.window_contact(False)
        epc_tester.allow_DI_on_presence_mode(True)
        wait_time = 15
        result_test = False
        epc_tester.set_presence_mode("off")
        time.sleep(3)
        actual_presence_mode = epc_tester.get_actual_presence_mode()
        print(actual_presence_mode)
        continue_ = False
        result_test = False
        if(actual_presence_mode == "off"):
            continue_ = True


        if continue_:
            continue_ = False
            message = ""
            epc_tester.set_presence_mode("day")
            time.sleep(3)
            actual_presence_mode = epc_tester.get_actual_presence_mode()
            print(actual_presence_mode)
            epc_tester.window_contact(True)
            time.sleep(wait_time)
            actual_presence_mode = epc_tester.get_actual_presence_mode()
            print(actual_presence_mode)

            if actual_presence_mode == "off":
                message = "Regulátor reaguje správně na vypnutí provozního režimu den, zapomocí otevření okna."
                continue_ = True
            elif actual_presence_mode == "day":
                message = "Regulátor nepřepnul z režimu den na vypnuto zapomocí otevření okna."

        epc_tester.window_contact(False)
        time.sleep(wait_time)

        if continue_:
            epc_tester.set_presence_mode("night")
            time.sleep(3)
            actual_presence_mode = epc_tester.get_actual_presence_mode()
            print(actual_presence_mode)
            epc_tester.window_contact(True)
            time.sleep(wait_time)
            actual_presence_mode = epc_tester.get_actual_presence_mode()
            print(actual_presence_mode)
            if actual_presence_mode == "off":
                message = "Regulátor reaguje správně na vypnutí provozního režimu den a noc, pomocí otevření okna."
                continue_ = True
                result_test = True
            elif actual_presence_mode == "day":
                message = "Regulátor nepřepnul z režimu noc na vypnuto pomocí otevření okna."
        message =  f"Výsledek testu {script_id} - " + message

        print(message)
        epc_tester.window_contact(False)
        time.sleep(10)

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
