from Bin2Hex import Bin2Hex
from writeOutputFiles import writeOutputFiles
from eCpriCommonHeader import eCpriCommonHeader
import random
import numpy as np

class ecpriMessageGenerator:
    def __init__(self):
        self.real_iq = []
        self.complex_iq = []
        self.bin2hex = Bin2Hex()
        self.ecpri_common_header = eCpriCommonHeader(self.bin2hex)

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
        IQ_PayloadSize = len(self.complex_iq)
        sequence_num = 0
        ecpriMsgData = ""

        while IQ_PayloadSize > 0:
            if IQ_PayloadSize == 1:
                cBit = 0
            else:
                cBit = 1

            msgType = "00000000"
            pc_id = ''.join(random.choices('0123456789ABCDEF', k=4))

            payload_size = IQ_PayloadSize

            # Generate the common header using eCpriCommonHeader class
            common_header = self.ecpri_common_header.generate_common_header(cBit, msgType, payload_size)

            # Update sequence ID with the current sequence number
            sequence_id = self.bin2hex.convert_bin_to_hex(format(sequence_num, '016b'))

            # Convert the IQ data to hexadecimal representation for the current burst
            iq_data_hex = ""
            for iq in zip(self.real_iq[:IQ_PayloadSize], self.complex_iq[:IQ_PayloadSize]):
                real_hex = self.bin2hex.convert_bin_to_hex(np.binary_repr(np.float32(iq[0]).view(np.int32)))
                imag_hex = self.bin2hex.convert_bin_to_hex(np.binary_repr(np.float32(iq[1]).view(np.int32)))
                iq_data_hex += real_hex + imag_hex

            # Assemble the complete packet
            complete_packet = common_header + pc_id + sequence_id + iq_data_hex

            ecpriMsgData += complete_packet
            # Increment the sequence number
            sequence_num += 1

            # Reduce the payload size by the number of bursts processed
            IQ_PayloadSize -= 1

        return ecpriMsgData
