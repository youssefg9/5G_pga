class InterFrameGap:
    def __init__(self):
        pass

    def ifg_function(self, ifg_length, ifg_padding):
        ifg = ""
        one_byte = "07"  # Hex representation of 00000111

        for _ in range(int(ifg_length)):
            ifg += one_byte

        if ifg_padding != 0:
            padding_bytes = one_byte * int(ifg_padding)
            ifg += padding_bytes

        return ifg
