import time
from script_definitions.EPC102.epc_tester import EPCTester
from script_definitions.modbus_client import ModbusClient

def play_test(port):
    #Manuální sepnutí výstupu - PWM sekvence, polarita NC
    device_id = 1
    script_id = 8

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
        num_of_samples = 3
        epc_tester.manual_heat_allowed(True)
        epc_tester.set_valve_polarity("nc")

        second_measure_avr = 0
        third_measure_avr = 0

        last_time = time.time()
        last_do_val = 0
        continue_ = False

        # Vytvoření prázdného dvoudimenzionálního seznamu o 4 řádcích
        first_measure_list = []
        epc_tester.manual_heat_value(25)
        while len(first_measure_list)!=num_of_samples:
            new_do_val = epc_tester.do_1_state()
            new_time = time.time()
            if last_do_val != new_do_val:
                elapsed_time = new_time - last_time
                if (last_do_val == 0):
                    print(f"Přečtená hodnota {last_do_val} - čas {elapsed_time}")
                elif(last_do_val==1):
                    first_measure_list.append(elapsed_time)
                    print(f"Přečtená hodnota {last_do_val} - čas {elapsed_time}")
                print("hodnota se změnila")
                print("")
                last_time = new_time
                last_do_val = new_do_val
        first_measure_list.pop(0)
        first_measure_avr = round(sum(first_measure_list)/ len(first_measure_list),2)
        print(first_measure_avr)
        if first_measure_avr > 4.5 and first_measure_avr < 5.5:
            continue_ = True
        print(f"měření na 25% ok? {continue_} hodnota - {first_measure_avr}")

        if continue_:
            continue_ = False
            second_measure_list = []
            epc_tester.manual_heat_value(50)

            last_time = time.time()
            last_do_val = 0
            while len(second_measure_list)!=num_of_samples:
                new_do_val = epc_tester.do_1_state()
                new_time = time.time()
                if last_do_val != new_do_val:
                    elapsed_time = new_time - last_time
                    if (last_do_val == 0):
                        print(f"Přečtená hodnota {last_do_val} - čas {elapsed_time}")
                    elif (last_do_val == 1):
                        second_measure_list.append(elapsed_time)
                        print(f"Přečtená hodnota {last_do_val} - čas {elapsed_time}")
                    print("hodnota se změnila")
                    print("")
                    last_time = new_time
                    last_do_val = new_do_val
            second_measure_list.pop(0)
            second_measure_avr = round(sum(second_measure_list) / len(second_measure_list), 2)
            print(second_measure_avr)
            if second_measure_avr > 9.5 and second_measure_avr < 10.5:
                continue_ = True
        print(f"měření na 50% ok? {continue_} hodnota - {second_measure_avr}")

        if continue_:
            continue_ = False
            third_measure_list = []
            epc_tester.manual_heat_value(75)

            last_time = time.time()
            last_do_val = 0
            while len(third_measure_list)!=num_of_samples:
                new_do_val = epc_tester.do_1_state()
                new_time = time.time()
                if last_do_val != new_do_val:
                    elapsed_time = new_time - last_time
                    if (last_do_val == 0):
                        print(f"Přečtená hodnota {last_do_val} - čas {elapsed_time}")
                    elif (last_do_val == 1):
                        third_measure_list.append(elapsed_time)
                        print(f"Přečtená hodnota {last_do_val} - čas {elapsed_time}")
                    print("hodnota se změnila")
                    print("")
                    last_time = new_time
                    last_do_val = new_do_val
            third_measure_list.pop(0)
            third_measure_avr = round(sum(third_measure_list) / len(third_measure_list), 2)
            if third_measure_avr > 14.5 and third_measure_avr < 15.5:
                continue_ = True
        print(f"měření na 75% ok? {continue_} - hodnota {third_measure_avr}")

        epc_tester.manual_heat_value(0)
        epc_tester.set_valve_polarity("no")
        epc_tester.manual_heat_allowed(False)



        if continue_:
            result_test = True
            message = "Výstup regulátoru správně přepočítává zadanou hodnotu na PWM sekvenci při NC polaritě."
        else:
            result_test = False
            message = "Výstup regulátoru špatně přepočítává zadanou hodnotu na PWM sekvenci při NC polaritě."


        message =  f"Výsledek testu {script_id} - " + message 

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