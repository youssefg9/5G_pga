from collections import defaultdict

#hex charachters consists of 4 bits () 
class Bin2Hex:


    @staticmethod
    def __create_map__():
        um = defaultdict(str)
        um["0000"] = '0'
        um["0001"] = '1'
        um["0010"] = '2'
        um["0011"] = '3'
        um["0100"] = '4'
        um["0101"] = '5'
        um["0110"] = '6'
        um["0111"] = '7'
        um["1000"] = '8'
        um["1001"] = '9'
        um["1010"] = 'A'
        um["1011"] = 'B'
        um["1100"] = 'C'
        um["1101"] = 'D'
        um["1110"] = 'E'
        um["1111"] = 'F'
        return um

    def convert_bin_to_hex(self, bin_string):
        l = len(bin_string)
        t = bin_string.find('.')

        len_left = t if t != -1 else l

        for i in range((4 - len_left % 4) % 4):
            bin_string = '0' + bin_string

        if t != -1:
            len_right = l - len_left - 1

            for i in range((4 - len_right % 4) % 4):
                bin_string = bin_string + '0'

        bin_hex_map = self.__create_map__()

        i = 0
        hex_string = ""

        while True:
            hex_string += bin_hex_map[bin_string[i:i+4]]
            i += 4

            if i == len(bin_string):
                break

            if bin_string[i] == '.':
                hex_string += '.'
                i += 1

        return hex_string
