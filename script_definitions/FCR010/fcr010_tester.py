from script_definitions.convertor import Convertor
import time
class FCR010Tester: #metody pro testování FCR010
    def __init__(self,R500_client, RMIO_client, R430_client, EPC_client):
        self.R500_client = R500_client
        self.RMIO_client = RMIO_client
        self.R430_client = R430_client
        self.FCR10_client = EPC_client
    def device_power(self,is_allowed):
        if (is_allowed == True):
            self.RMIO_client.write_coils_15(9, [1], 0, 0)
        elif (is_allowed == False):
            self.RMIO_client.write_coils_15(9, [0], 0, 0)

    def slave_device_power(self,is_allowed):
        if (is_allowed == True):
            self.RMIO_client.write_coils_15(9, [1], 1, 1)
        elif (is_allowed == False):
            self.RMIO_client.write_coils_15(9, [0], 1, 1)

    def set_new_modbus_address(self, address):
        self.FCR10_client.write_coils_15(4, Convertor.convert_8bit_val_to_list(address), 0, 7)

    def set_baud_rate(self,baudrate):
        if(baudrate == 1200):
            self.FCR10_client.write_coils_15(4, Convertor.convert_8bit_val_to_list(10), 8, 15)
        elif(baudrate == 9600):
            self.FCR10_client.write_coils_15(4, Convertor.convert_8bit_val_to_list(13), 8, 15)


    def get_current_baudrate(self):
        return self.FCR10_client.read_coils_01(4, 0, 7, "msb")

    def get_modbus_address(self):
        return Convertor.binary_list_to_decima(self.FCR10_client.read_coils_01(4, 0, 7, "lsb"))
    def write_to_eeprom_allowed(self, is_allowed):
        if is_allowed:
            self.FCR10_client.write_coils_15(3, [1], 0, 0)
        else:
            self.FCR10_client.write_coils_15(3, [0], 0, 0)

    def get_slave_communication_state(self):    #Když je regulátor odpojen - communication_state = True
        communication_state = self.FCR10_client.read_coils_01(9, 0, 0, "msb")[0]
        if(communication_state == 0):
            return True
        elif(communication_state == 1):
            return False


    def sw_reset_allowed(self, is_allowed):
        if is_allowed:
            self.FCR10_client.write_coils_15(3, [1], 1, 1)
        else:
            self.FCR10_client.write_coils_15(3, [0], 1, 1)

    def sw_reset(self):
        self.FCR10_client.write_coils_15(1002, [1], 0, 0)


    def slave_modbus_communication(self,is_allowed):
        if(is_allowed==True):
            self.RMIO_client.write_coils_15(9, [1], 4, 4)
        elif(is_allowed==False):
            self.RMIO_client.write_coils_15(9, [0], 4, 4)
    def modbus_communication(self,is_allowed):
        if(is_allowed==True):
            self.RMIO_client.write_coils_15(9, [1], 3, 3)
        elif(is_allowed==False):
            self.RMIO_client.write_coils_15(9, [0], 3, 3)
    def window_contact(self,connected):
        if (connected == True):
            self.RMIO_client.write_coils_15(9, [1], 5, 5)
        elif (connected == False):
            self.RMIO_client.write_coils_15(9, [0], 5, 5)
    def do_1_state(self):
        return(self.R430_client.read_coils_01(5,0,0,"msb")[0])
    def do_2_state(self):
        return(self.R430_client.read_coils_01(5,1,1,"msb")[0])
    def manual_heat(self,is_allowe):
        if(is_allowe == True):
            self.FCR10_client.write_coils_15(10, [1], 1, 1)
        if (is_allowe == False):
            self.FCR10_client.write_coils_15(10, [0], 1, 1)
    def manual_heat_value(self,value):
        value_list = Convertor.convert_8bit_val_to_list(value)
        return self.FCR10_client.write_coils_15(11, value_list, 0, 7)
    def get_DI_state(self): # vrátí aktuální hodnotu DI z EPC102
        return self.FCR10_client.read_coils_01(7, 1, 1, "MSB")
    def pwm_control(self):
        last_time = 0
        last_val = 0
        while True:
            new_val = self.do_1_state()

            new_time = time.time()

            if last_val != new_val:
                print(new_time-last_time)
                if(last_val==0):
                    print(0)
                elif(last_val==1):
                    print(1)
                print("hodnota se změnila")
                last_time = new_time
                last_val = new_val
            # time.sleep(1)
    def get_module_id(self):
        bi_list = self.FCR10_client.read_coils_01(1, 0, 15, mode ="whole")
        return Convertor.binary_list_to_decima(bi_list)



