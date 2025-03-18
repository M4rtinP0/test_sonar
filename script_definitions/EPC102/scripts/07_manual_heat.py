import time
from script_definitions.EPC102.epc_tester import EPCTester
from script_definitions.modbus_client import ModbusClient

def play_test(port):
    #manuální sepnutí výstupu
    device_id = 1
    script_id = 7

    try:
        RMIO_client = ModbusClient(port, 254)
        R500_client = ModbusClient(port, 253)
        R430_client = ModbusClient(port, 255)
        EPC_client = ModbusClient(port, 1)
        epc_tester = EPCTester(R500_client, RMIO_client, R430_client, EPC_client)

        print("manual output control")
        epc_tester.device_power(True)
        epc_tester.modbus_communication(True)
        epc_tester.one_wire_communication(True)

        result_test = False
        message = ""
        continue_ = False

        #výchozí nastavení regulátoru
        epc_tester.manual_heat_allowed(False)
        epc_tester.set_valve_polarity("no")
        epc_tester.manual_heat_value(0)
        time.sleep(3)

        epc_tester.manual_heat_allowed(True)
        time.sleep(3)
        epc_tester.set_valve_polarity("nc")
        epc_tester.manual_heat_value(100)
        time.sleep(3)
        print("požadavek na topení")
        time.sleep(3)
        do_1_state = epc_tester.do_1_state()
        do_2_state = epc_tester.do_1_state()
        print(do_1_state)
        if (do_1_state == 1 and do_2_state == 1):
            continue_ = True

        if continue_:
            continue_ = False
            epc_tester.manual_heat_value(0)
            print('požadavek na "netopení"')
            time.sleep(3)
            do_1_state = epc_tester.do_1_state()
            do_2_state = epc_tester.do_1_state()
            print(do_1_state)
            if not (do_1_state == 1 and do_2_state == 1):
                continue_ = True
                print("zatím funguje dobře")

        if continue_:
            continue_ = False

            epc_tester.set_valve_polarity("no")

            epc_tester.manual_heat_value(100)
            print("požadavek na topení")
            time.sleep(3)
            do_1_state = epc_tester.do_1_state()
            do_2_state = epc_tester.do_1_state()
            print(do_1_state)
            if not (do_1_state == 1 and do_2_state == 1):
                continue_ = True

            if continue_ == True:
                continue_ = False

                epc_tester.manual_heat_value(0)
                print('požadavek na "netopení"')
                time.sleep(3)
                do_1_state = epc_tester.do_1_state()
                do_2_state = epc_tester.do_1_state()
                print(do_1_state)
                if (do_1_state == 1 and do_2_state == 1):
                    continue_ = True

        epc_tester.manual_heat_value(0)
        epc_tester.manual_heat_allowed(False)
        epc_tester.set_valve_polarity("no")
        time.sleep(3)

        if continue_:
            message = "Regulátor správně reaguje na změnu výstupu a na změnu polarity ventilu při manuálním řízení."
            result_test = True
        else:
            message = "Regulátor reaguje špatně na změnu výstupu a na zaměnu polarity ventilu při manuálním řízení."
            result_test = False
        message =  f"Výsledek testu {script_id} - " + message 

        print(message)
        print(result_test)
        return result_test, message, device_id, script_id
    except:
        print(False, f"Test {script_id} selhal")
        return False, f"Test {script_id} selhal", device_id, script_id


# play_test("COM4")

# while True:
#     print(f"polarita ventilů {epc_tester.get_valve_polarity()}")
#     time.sleep(3)
#     epc_tester.set_valve_polarity("nc")
#     print(f"polarita ventilů {epc_tester.get_valve_polarity()}")
#     time.sleep(3)
#     epc_tester.set_valve_polarity("no")

# while True:
#     epc_tester.manual_heat_value(100)
#     print("topíme")
#     time.sleep(5)
#
#     epc_tester.manual_heat_value(0)
#     print("netopíme")
#     time.sleep(5)