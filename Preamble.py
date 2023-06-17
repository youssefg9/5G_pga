from Bin2Hex import Bin2Hex

class Preamble:
    def __init__(self):
        pass

    def preambleFormation(self):
        preamble_string = ""
        pre = "10101010101010101010101010101010101010101010101010101010"
        sfd = "10101011"
        binToHex = Bin2Hex()
        preamble_string = binToHex.convert_bin_to_hex(pre+sfd)
        return preamble_string