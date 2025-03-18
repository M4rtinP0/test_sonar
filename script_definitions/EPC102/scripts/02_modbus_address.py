import time
from script_definitions.EPC102.epc_tester import EPCTester
from script_definitions.modbus_client import ModbusClient

def play_test(port):
    #Test modbusových adres
    device_id = 1
    script_id = 2
    max_tested_address = 3

    RMIO_client = ModbusClient(port, 254)
    R500_client = ModbusClient(port, 253)
    R430_client = ModbusClient(port, 255)
    EPC_client = ModbusClient(port, 1)

    epc_tester = EPCTester(R500_client, RMIO_client, R430_client, EPC_client)

    epc_tester.device_power(True)
    epc_tester.modbus_communication(True)
    epc_tester.one_wire_communication(True)

    try:
        if max_tested_address >=2:
            for i in range(2,max_tested_address+2): #  i  = <1-254) = 1-253 <2,5) -> 2,4
                if(i==max_tested_address+1):
                    i = 1
                epc_tester.sw_reset_allowed(True)
                epc_tester.write_to_eeprom_allowed(True)

                epc_tester.set_new_modbus_address(i)

                epc_tester.sw_reset()
                time.sleep(1)
                # vytvoř nového clienta na nové adrese

                EPC_client = ModbusClient(port, i)
                epc_tester = EPCTester(R500_client, RMIO_client, R430_client, EPC_client)

                actual_modbus_address = epc_tester.get_modbus_address()
                print(f"Nově nastavená modbus adressa - {actual_modbus_address}")
                print(f"Module ID = {epc_tester.get_module_id()}")
                if actual_modbus_address == i:
                    message = f"Výsledek testu {script_id} - Zařízení je dostupné na adresách 1 - {max_tested_address}."
                    # message = f"Výsledek testu {script_id} - Jedná se o správné zařízení."

                    result_test = True
                else:
                    message = f"Výsledek testu {script_id} - Zařízení není dostupné na adrese {i}"
                    result_test = False
        return result_test, message, device_id, script_id
    except:
        return False, f"Test {device_id} selhal", device_id, script_id
        print(f"test {script_id} selhal")
# play_test("COM4")

