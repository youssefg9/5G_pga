import random

class Payload:
    def __init__(self):
        pass

    def pay_load_data(self,choice, size_in_bytes):
        if choice == "RANDOM":
            hex_chars = "0123456789ABCDEF"
            random.seed()
            payload = ""
            for _ in range(int(size_in_bytes)):
                byte_value = random.randint(0, 255)
                payload += format(byte_value, '02X')
        else:
            payload = choice
        return payload