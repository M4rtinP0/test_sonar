import time
from script_definitions.FCR010.fcr010_tester import FCR010Tester
from script_definitions.modbus_client import ModbusClient
def play_test(port):
    #Test modbusových adres
    device_id = 2
    script_id = 102
    max_tested_address = 3

    R500_client = ModbusClient(port, 253)
    RMIO_client = ModbusClient(port, 254)
    R430_client = ModbusClient(port, 255)
    FCR10_client = ModbusClient(port, 1)
    fcr010_tester = FCR010Tester(R500_client, RMIO_client, R430_client, FCR10_client)

    fcr010_tester.device_power(True)
    fcr010_tester.modbus_communication(True)
    fcr010_tester.slave_modbus_communication(True)
    fcr010_tester.slave_device_power(True)


    print(fcr010_tester.get_module_id())

    try:
        if max_tested_address >=2:
            for i in range(2,max_tested_address+2): #  i  = <1-254) = 1-253 <2,5) -> 2,4
                if(i==max_tested_address+1):
                    i = 1
                fcr010_tester.sw_reset_allowed(True)
                fcr010_tester.write_to_eeprom_allowed(True)

                fcr010_tester.set_new_modbus_address(i)

                fcr010_tester.sw_reset()
                time.sleep(1)

                FCR10_client = ModbusClient(port, i)
                fcr010_tester = FCR010Tester(R500_client, RMIO_client, R430_client, FCR10_client)

                actual_modbus_address = fcr010_tester.get_modbus_address()
                print(f"Nově nastavená modbus adressa - {actual_modbus_address}")
                print(f"Module ID = {fcr010_tester.get_module_id()}")
                if actual_modbus_address == i:
                    message = f"Výsledek testu {script_id} - Zařízení je dostupné na adresách 1 - {max_tested_address}"
                    result_test = True
                else:
                    message = f"Výsledek testu {script_id} - Zařízení není dostupné na adrese {i}"
                    result_test = False
        return result_test, message, device_id, script_id
    except:
        return False, f"Test {device_id} selhal", device_id, script_id
        print(f"test {script_id} selhal")
# play_test("COM4")

