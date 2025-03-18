class Convertor():
    @staticmethod
    def convert_8bit_val_to_list(input_value):
        if(input_value>=0 and input_value <=255):
            binval = bin(input_value)[2:].zfill(8)
            output_list = []
            for bit in binval:
                output_list.append(bit)
            list_intu = list(map(int, output_list))
            return(list_intu)
        else:
            return(-1)

    @staticmethod
    def convert_16bit_val_to_list(input_value):
        if (input_value>=0 and input_value <= 65535):
            binval = bin(input_value)[2:].zfill(8)
            output_list = []
            for bit in binval:
                output_list.append(bit)
            list_intu = list(map(int, output_list))
            return (list_intu)
        else:
            return (-1)
    @staticmethod
    def binary_list_to_decima(binary_list):
        decimal_value = 0
        for bit in binary_list:
            decimal_value = decimal_value * 2 + bit
        return decimal_value
