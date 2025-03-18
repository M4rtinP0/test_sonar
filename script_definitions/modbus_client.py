import minimalmodbus

class ModbusClient:

    def __init__(self, port,device_address,current_boudrate = 9600,parity = "N"):
        # self.modbus_boudrates = [300, 600, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]
        self.instrument = minimalmodbus.Instrument(port, device_address)
        self.instrument.serial.baudrate = current_boudrate
        self.instrument.serial.parity = parity
        self.instrument.serial.stopbits = 1
        self.instrument.serial.bytesize = 8

    def read_coils_01(self,start_register, start_bit, end_bit, mode="whole"):
        mode = mode.lower()
        try:
            if (mode == "whole"):
                start_register-=1
                end_bit +=1
                values = self.instrument.read_bits((start_register*16)+start_bit,end_bit-start_bit,functioncode=1)
                output_value = list(reversed(values))
                return (output_value)
            if(mode == "lsb"):
                start_register -= 1
                end_bit += 1
                values = self.instrument.read_bits((start_register * 16) + start_bit, end_bit - start_bit,
                                                   functioncode=1)
                output_value = list(reversed(values))
                return (output_value)
            if(mode == "msb"):
                start_register -= 1
                end_bit += 1
                values = self.instrument.read_bits((start_register * 16) + start_bit+8, end_bit - start_bit,
                                                   functioncode=1)
                output_value = list(reversed(values))
                return (output_value)
        except Exception as e:
                return (False,e)
        finally:
            self.instrument.serial.close()
    def write_coils_15(self,start_register,bits_to_write, start_bit, end_bit):
        try:
            end_bit+=1
            bit_count = end_bit - start_bit
            start_register-=1
            bits_to_write = list(reversed(bits_to_write))
            if(bit_count == len(bits_to_write)):
                self.instrument.write_bits(start_register*16+start_bit, bits_to_write)
                return True
            e =""
            return (False, e)
        except Exception as e:
            return (False, e)
        finally:
            self.instrument.serial.close()
    def write_register_16(self,start_register,values_to_write,mode = "whole"):
        try:
            start_register-=1
            if(values_to_write>=0 and values_to_write<=65535):
                self.instrument.write_register(start_register, values_to_write,functioncode=16)
                return True
            e = ""
            return (False, e)
        except Exception as e:
            return (False, e)
        finally:
            self.instrument.serial.close()


def read_coils_01(self, start_register, start_bit, end_bit, mode="whole"):
    mode = mode.lower()
    values = []
    try:
        start_register -= 1
        end_bit += 1
        if mode == "whole" or "lsb":
            values = self.instrument.read_bits((start_register * 16) + start_bit, end_bit - start_bit, functioncode=1)
        elif mode == "msb":
            start_bit += 8
            values = self.instrument.read_bits((start_register * 16) + start_bit, end_bit - start_bit, functioncode=1)
        output_value = list(reversed(values))
        return output_value
    except Exception as e:
        return False, e