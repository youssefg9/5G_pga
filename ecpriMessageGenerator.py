from Bin2Hex import Bin2Hex
from writeOutputFiles import writeOutputFiles
import random
import numpy as np
class ecpriMessageGenerator:
    def __init__(self):
        self.real_iq = []
        self.complex_iq = []

    def read_iq_data(self, file_path):
        # Read the IQ data from the file
        with open(file_path, "r") as file:
            # Read each line
            for line in file:
                # Split the line into parts and remove extra spaces
                parts = line.strip().split()

                # Ensure the line has two parts
                if len(parts) == 2:
                    # Convert the parts to float and create complex numbers
                    real = float(parts[0])
                    imag = float(parts[1])
                    iq = complex(real, imag)

                    # Append the complex number to the respective arrays
                    self.real_iq.append(iq.real)
                    self.complex_iq.append(iq.imag)
                else:
                    print(f"Ignoring invalid line: {line}")

    def generate_ecpri_message(self, iq_file):
        # Read IQ data from the file
        self.read_iq_data(iq_file)

        # Prepare the eCPRI Message common header part
        IQ_PayloadSize=len(self.complex_iq)
        bin2hex = Bin2Hex()
        sequence_num=0
        ecpriMsgData=""
        
        while IQ_PayloadSize > 0:
            # Protocol revision (4 bits put it v3 here) + reserved bits(3 bits=000) + cbit (0 for last msg, else =1) + msg type(1 byte = 0 for msg type 0) + payload size (given by user)
            protocol_rev = "0010"
            reserved = "000"
            if IQ_PayloadSize == 1:
                cBit = 0
            else:
                cBit = 1

            msgType = "00000000"
            pc_id = ''.join(random.choices('0123456789ABCDEF', k=4))

            payload_size = format(IQ_PayloadSize, '016b')

            # Create common header
            common_header = bin2hex.convert_bin_to_hex(protocol_rev + reserved + str(cBit) + msgType + payload_size)

            # Update sequence ID with the current sequence number
            sequence_id = bin2hex.convert_bin_to_hex(format(sequence_num, '016b'))

            # Convert the IQ data to hexadecimal representation for the current burst
            iq_data_hex = ""
            for iq in zip(self.real_iq[:IQ_PayloadSize], self.complex_iq[:IQ_PayloadSize]):
                real_hex = bin2hex.convert_bin_to_hex(np.binary_repr(np.float32(iq[0]).view(np.int32)))
                imag_hex = bin2hex.convert_bin_to_hex(np.binary_repr(np.float32(iq[1]).view(np.int32)))
                iq_data_hex += real_hex + imag_hex

            # Assemble the complete packet
            complete_packet = common_header + pc_id + sequence_id + iq_data_hex

            ecpriMsgData+= complete_packet
            # Increment the sequence number
            sequence_num += 1

            # Reduce the payload size by the number of bursts processed
            IQ_PayloadSize -= 1

        return ecpriMsgData


        