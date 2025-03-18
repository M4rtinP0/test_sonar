from script_definitions.convertor import Convertor
import time
class EPCTester: #metody pro testování EPC102
    def __init__(self,R500_client, RMIO_client, R430_client, EPC_client):
        self.R500_client = R500_client
        self.RMIO_client = RMIO_client
        self.R430_client = R430_client
        self.EPC_client = EPC_client

    # RMIO client
    def device_power(self,is_allowed):
        if (is_allowed == True):
            self.RMIO_client.write_coils_15(9, [1], 0, 0)
        elif (is_allowed == False):
            self.RMIO_client.write_coils_15(9, [0], 0, 0)
    def one_wire_communication(self, is_allowed):
        if (is_allowed == True):
            self.RMIO_client.write_coils_15(9, [1], 4, 4)
        elif (is_allowed == False):
            self.RMIO_client.write_coils_15(9, [0], 4, 4)
    def modbus_communication(self, is_allowed):
        if (is_allowed == True):
            self.RMIO_client.write_coils_15(9, [1], 3, 3)
        elif (is_allowed == False):
            self.RMIO_client.write_coils_15(9, [0], 3, 3)
    def window_contact(self, connected):
        if (connected == True):
            self.RMIO_client.write_coils_15(9, [1], 5, 5)
        elif (connected == False):
            self.RMIO_client.write_coils_15(9, [0], 5, 5)

    # R430 client
    def do_1_state(self):
        return (self.R430_client.read_coils_01(5, 0, 0, "msb")[0])
    def do_2_state(self):
        return (self.R430_client.read_coils_01(5, 1, 1, "msb")[0])

    # EPC client
    def get_module_id(self):
        bi_list = self.EPC_client.read_coils_01(1, 0, 15, mode="whole")
        return Convertor.binary_list_to_decima(bi_list)
    def set_new_modbus_address(self, address):
        self.EPC_client.write_coils_15(4,Convertor.convert_8bit_val_to_list(address),0,7)
    def get_modbus_address(self):
        return Convertor.binary_list_to_decima(self.EPC_client.read_coils_01(4,0,7,"lsb"))
    def set_baud_rate(self,baudrate):
        if(baudrate == 1200):
            self.EPC_client.write_coils_15(4,Convertor.convert_8bit_val_to_list(10),8,15)
        elif(baudrate == 9600):
            self.EPC_client.write_coils_15(4,Convertor.convert_8bit_val_to_list(13),8,15)
    def get_current_baudrate(self):
        return self.EPC_client.read_coils_01(4,0,7,"msb")
    def write_to_eeprom_allowed(self, is_allowed):
        if is_allowed:
            self.EPC_client.write_coils_15(3,[1],0,0)
        else:
            self.EPC_client.write_coils_15(3,[0],0,0)
    def sw_reset_allowed(self, is_allowed):
        if is_allowed:
            self.EPC_client.write_coils_15(3, [1], 1, 1)
        else:
            self.EPC_client.write_coils_15(3, [0], 1, 1)
    def sw_reset(self):
        self.EPC_client.write_coils_15(1002, [1], 0, 0)
    def get_actual_presence_mode(self):
        mode = self.EPC_client.read_coils_01(25,0,2,"lsb")
        if mode == [1,0,0]:
            presence_mode = "off"
        elif mode == [0,1,0]:
            presence_mode = "night"
        elif mode == [0,0,1]:
            presence_mode = "day"
        else:
            presence_mode = -1
        return presence_mode

    def set_presence_mode(self, mode): # Jelikož se v jeden moment musí zapsat více bitů - konkrétně bity na pozici 1-2 a 15, musí být použita funkce 16, která zapisuje najednou celé 16 bitové slovo.
        mode = mode.lower()
        if mode == "day":
            self.EPC_client.write_register_16(23,32769)
        elif mode == "night":
            self.EPC_client.write_register_16(23,32770)
        elif mode == "off":
            self.EPC_client.write_register_16(23,32772)

    def allow_DI_on_presence_mode(self, is_allowed):
        if is_allowed == True:
            self.EPC_client.write_coils_15(26, [1], 9, 9)
        if is_allowed == False:
            self.EPC_client.write_coils_15(26, [0], 9, 9)

    def is_DI_allowed_on_presence_mode(self):
        return self.EPC_client.read_coils_01(26,1,1,"msb")

    def manual_heat_allowed(self,is_allowe):
        if(is_allowe == True):
            self.EPC_client.write_coils_15(10, [1], 1, 1)
        if (is_allowe == False):
            self.EPC_client.write_coils_15(10, [0], 1, 1)

        # print(self.EPC_client.read_coils_01(23,0,15,"whole"))
    def manual_heat_value(self,value):
        value_list = Convertor.convert_8bit_val_to_list(value)
        return self.EPC_client.write_coils_15(11, value_list, 0, 7)
    def set_valve_polarity(self,polarity):
        polarity = polarity.lower()
        if polarity == "nc": # když regulátor topí - na výstupu je napětí
            self.EPC_client.write_coils_15(26, [0],5,5)
        elif polarity == "no": # když regulátor topí - na výstupu není napětí
            self.EPC_client.write_coils_15(26, [1],5,5)
    def get_valve_polarity(self):
        polarity = self.EPC_client.read_coils_01(26,5,5,"lsb")[0]
        if polarity == 1:
            return "no"
        elif polarity == 0:
            return "nc"

    def get_DI_state(self): # vrátí aktuální hodnotu DI z EPC102
        bit_list = self.EPC_client.read_coils_01(7,1,1,"msb")
        bit = bit_list[0]
        if bit == 1:
            return True
        else:
            return False
    def get_sensor_state(self): #když je odpojeno čidlo - 3.bit == 1
        bit_list = self.EPC_client.read_coils_01(7, 3, 3, "msb")

        bit = bit_list[0]
        if bit == 1:
            return False
        else:
            return True
    # def pwm_control(self):
    #     last_time = 0
    #     last_val = 0
    #     while True:
    #         new_val = self.do_1_state()
    #
    #         new_time = time.time()
    #
    #         if last_val != new_val:
    #             print(new_time-last_time)
    #             if(last_val==0):
    #                 print(0)
    #             elif(last_val==1):
    #                 print(1)
    #             print("hodnota se změnila")
    #             last_time = new_time
    #             last_val = new_val
    #         # time.sleep(1)