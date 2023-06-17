from FrameGenerator import FrameGenerator
from ecpriMessageGenerator import ecpriMessageGenerator
from writeOutputFiles import writeOutputFiles
import os

# CRC GenPolynomial (this is the standard CRC-32 generator polynomial used for 802.3 error detection and correction)
crcGenPolynomial = "100000100110000010001110110110111"
# Total Payload size of the randomly generated payload data (in bytes)
randomPayloadTotalSize = 1000
# Line rate in Gbps
lineRate = 10

# ecpri data
file_path = "iq_data.txt"  # Replace with the actual file path

# Create an instance of the FrameGenerator class
frame_gen = FrameGenerator()
ecpri= ecpriMessageGenerator()
out= writeOutputFiles()

# Call the generatorFunc method with the desired arguments
ecpriMsg=ecpri.generate_ecpri_message(iq_file=file_path)
out.generateOutput(dataToBeWrittenOnOutputFile=ecpriMsg,output_file="ecpriMsgOutput")

ethernetFrames=frame_gen.generatorFunc(inputFile='input_config.txt',is_IQ_data=True,iq_payload=ecpriMsg, payloadTotalSize=randomPayloadTotalSize, crcGenPolynomial=crcGenPolynomial,lineRate= lineRate)
out.generateOutput(dataToBeWrittenOnOutputFile=ethernetFrames,output_file="ethernetFramesOutput")



