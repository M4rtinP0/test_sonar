import time

from script_definitions.EPC102.epc_tester import EPCTester
from script_definitions.modbus_client import ModbusClient

def play_test(port):
    # #Test okenního kontaktu
    print(f"Test okenního kontaktu {port}")
    device_id = 1
    script_id = 3
    delay_time = 20

    try:
        RMIO_client = ModbusClient(port, 254)
        R500_client = ModbusClient(port, 253)
        R430_client = ModbusClient(port, 255)
        EPC_client = ModbusClient(port, 1)
        epc_tester = EPCTester(R500_client, RMIO_client, R430_client, EPC_client)

        epc_tester.device_power(True)
        epc_tester.modbus_communication(True)
        epc_tester.one_wire_communication(True)
        epc_tester.window_contact(False)



        epc_tester.window_contact(True)
        time.sleep(delay_time)
        di_state = epc_tester.get_DI_state()
        if (di_state):
            result_test = True
            message = "Zařízení reaguje správně na okenní kontakt"

        else:
            result_test = False
            message = "Zařízení nereaguje srávně na okenní kontakt"

        epc_tester.window_contact(False)
        time.sleep(delay_time)
        di_state = epc_tester.get_DI_state()
        if(di_state==False):
            result_test = True
            message = "Zařízení reaguje správně na okenní kontakt"
        else:
            result_test = False
            message = "Zařízení nereaguje srávně na okenní kontakt"
        message = f"Výsledek testu {script_id} - {message}."
        # message = f"Výsledek testu {script_id} - Jedná se o správné zařízení."

        print(message)
        return result_test, message, device_id, script_id
    except:
        print( False, f"Test {script_id} selhal")
        return False, f"Test {script_id} selhal", device_id, script_id
# play_test("COM4")


        # while (True):
        #     epc_tester.window_contact(True)
        #     time.sleep(1)
        #     di_state = epc_tester.get_DI_state()
        #     print(type(di_state))
        #     print(di_state)
        #
        #     epc_tester.window_contact(False)
        #     di_state = epc_tester.get_DI_state()
        #     print(type(di_state))
        #     print(di_state)



#         EPC_client = ModbusClient(port, 1,1200)
#         epc_tester = EPCTester(None, None, None, EPC_client)
#         print(epc_tester.get_current_baudrate())
#
#         epc_tester.sw_reset_allowed(True)
#         epc_tester.write_to_eeprom_allowed(True)
#         epc_tester.set_baud_rate(9600)
#
#         epc_tester.device_power(False)
#         time.sleep(2)
#         epc_tester.device_power(True)
#         time.sleep(2)
#
#         EPC_client = ModbusClient(port, 1, 9600)
#         epc_tester = EPCTester(R500_client, RMIO_client, R430_client, EPC_client)
#         print(epc_tester.get_current_baudrate())
#
#
#
#     except:
#         print( False, f"Test {script_id} selhal")
#         return False, f"Test {script_id} selhal"
# play_test("COM4")
#
