from Bin2Hex import Bin2Hex

class eCpriCommonHeader:
    def __init__(self, bin2hex):
        self.bin2hex = bin2hex

    def generate_common_header(self, cBit, msgType, payload_size):
        # Prepare the binary representation of the common header fields
        protocol_rev = "0010"
        reserved = "000"
        payload_size_binary = format(payload_size, '016b')

        # Construct the common header
        common_header_binary = protocol_rev + reserved + str(cBit) + msgType + payload_size_binary

        # Convert the binary representation to hexadecimal
        common_header_hex = self.bin2hex.convert_bin_to_hex(common_header_binary)

        return common_header_hex