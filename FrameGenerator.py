import math
from ConfigFileReader import ConfigFileReader
from Preamble import Preamble
from Bin2Hex import Bin2Hex
from Payload import Payload
from Preamble import Preamble
from Addresses import Addresses
from Crc import Crc
from InterFrameGap import InterFrameGap





class FrameGenerator:

    def __init__(self):
        pass

    def process_file(self,input_file, output_file):
        with open(input_file, "r") as input_file, open(output_file, "w") as output_file:
            for line in input_file:
                line = line.strip()  # Remove leading/trailing whitespace
              # Split the line into chunks of 8 characters
                chunks = [line[i:i+8] for i in range(0, len(line), 8)]

              # Write each chunk as a separate line in the output file
                for chunk in chunks:
                    output_file.write(chunk + "\n")


    def generatorFunc(self,inputFile, payloadTotalSize,is_IQ_data,iq_payload ,crcGenPolynomial, lineRate):

        # Reading inputs from text file
        inputsFromTextFile = ConfigFileReader.file_reader(inputFile)
        streamPeriod = float(inputsFromTextFile[0])
        ifgs=float(inputsFromTextFile[1])
        sourceAddress = inputsFromTextFile[2]
        destinationAddress = inputsFromTextFile[3]
        etherType = inputsFromTextFile[4]
        payloadChoice = inputsFromTextFile[5]
        FrameSize = float(inputsFromTextFile[6])
        burstSize = int(inputsFromTextFile[7])
        burstPeriod = float(inputsFromTextFile[8])

        burstPeriod = burstPeriod * math.pow(10.0, -6)
        streamPeriod = streamPeriod * math.pow(10.0, -3)
        lineRate = lineRate * math.pow(10.0, 9)
        lineRate = lineRate /8

        # Creating instances of other classes
        preamble = Preamble()
        bin2Hex = Bin2Hex()
        
        # Setting destination & source addresss

        addresses= Addresses(destinationAddress,sourceAddress)
        destAddress = addresses.destAddress
        srcAddress = addresses.srcAddress
        payload = Payload()
        crc = Crc()

#____________this part converts the logic from time to bits/bytes and works with capactities instead of time_____________________________________________

        #Ex::change the 1ms streaming duration to it’s equivalent number of bytes, and same for burst period
        #this needs the lineRate parameter for calculations
        
    
        # Calculate stream and burst capacities in bytes
        streamCapacity = lineRate * streamPeriod  
        burstCapacity = lineRate * burstPeriod

        # Check if frame size * burst size exceeds burst capacity
        if (FrameSize) * burstSize > burstCapacity:
            raise Exception("Bad configuration file : number of frames in a burst multiplied by the frame duration is bigger than the burst period ,please update configuration file")
       
    #____If the period or the total streaming duration has ended while an ethernet packet is being generated, the packet should be discarded and IFGs are sent instead
        #If bursts to be interrupted due to end of streaming time, 
        
          
        dataLeftFromLastBurst=0.0
        lastBurstData=0.0

        if(streamCapacity%burstCapacity!=0):
            for i in range(burstSize):
                lastBurstData+=(FrameSize)
                if lastBurstData>(streamCapacity%burstCapacity):
                    dataLeftFromLastBurst=lastBurstData-(FrameSize)
                    break
            
        dataToBeWrittenOnOutputFile = ""

  #__________ check the size of data needed to be transmitted vs the MTU in 802.3 std = 1522 Bytes (1496 payload + 26 bytes overhead)__________
        #overhead given as Preamble: 8 bytes | Destination MAC address: 6 bytes | Source MAC address: 6 bytes | EtherType: 2 bytes | CRC (Cyclic Redundancy Check): 4 bytes 
        if(is_IQ_data):
            payloadTotalSize=len(iq_payload)/2

        numOfSegments= math.ceil(payloadTotalSize/FrameSize)
        
        while payloadTotalSize > 0 and numOfSegments>0:

            # Generate payload data
                # Generate payload data
            if is_IQ_data:
                if is_IQ_data:
                    if numOfSegments > 1:
                        payloadData = iq_payload[:(int(FrameSize) - 26)*2]
                        iq_payload = iq_payload[(int(FrameSize) - 26)*2:]  # Update iq_payload by removing the processed portion
                    else:
                        payloadData = iq_payload[:(int(FrameSize) - 26)*2]  # Subtract additional overhead for the last segment
            else:
                if numOfSegments > 1:
                    payloadData = payload.pay_load_data(payloadChoice, (FrameSize - 26))
                else:
                    payloadData = payload.pay_load_data(payloadChoice, payloadTotalSize)

            # Generate CRC data
            crcPart = crc.encodeData(
                destAddress + srcAddress + etherType + payloadData,
                crcGenPolynomial
            )
            crcPart = bin2Hex.convert_bin_to_hex(crcPart)

            # Generate complete Ethernet frame
            ethernetFrameFromPreambleTillCrc = (
                preamble.preambleFormation() + destAddress + srcAddress + etherType + payloadData + crcPart
            )

            # Insert data into the output string
            dataToBeWrittenOnOutputFile += ethernetFrameFromPreambleTillCrc      

            
            IFG = InterFrameGap()
            ifg = ""
            ifgPad = 0
            
            #Case 1: no frames are remaining from bursts
            if lastBurstData==0:
                #the ifg_static are static in every frame given in configuration file as IFGs = value
                #so we can add here 2 IFGs (static - padding)
                ifg_static = IFG.ifg_function(ifgs, 0)
                frameLen=FrameSize+int(ifgs)
                ifgPadSize=0
                if frameLen % 4 != 0:
                    ifgPadSize = (4 - (frameLen % 4)) % 4
                    ifgPadBytes = IFG.ifg_function(0, ifgPadSize)
                    totalIFGs=ifg_static+ifgPadBytes
                else :
                    totalIFGs=ifg_static
                dataToBeWrittenOnOutputFile += totalIFGs

            # Case 2: some frames are left as the stream period endded while transmitting last frames 
            #so we can add here 3 IFGs (static - padding ifgs - discarded data ifgs)
            elif lastBurstData!=0:
                #the ifg_static are static in every frame given in configuration file as IFGs = value
                ifg_static = IFG.ifg_function(ifgs, 0)
                frameLen=FrameSize+int(ifgs)
                ifgPadSize=0
                if frameLen % 4 != 0:
                    ifgPadSize = (4 - (frameLen % 4)) % 4
                    ifgPadBytes = IFG.ifg_function(0, ifgPadSize)
                    totalIFGs=ifg_static+ifgPadBytes
                else :
                    totalIFGs=ifg_static
                ExtraIfgs = IFG.ifg_function(dataLeftFromLastBurst, 0)
                totalIFGs=totalIFGs+ExtraIfgs
                dataToBeWrittenOnOutputFile += totalIFGs
                
            # Check if frame length after adding IFGs is divisible by 4
            frameLength = len(dataToBeWrittenOnOutputFile)/2      #divide by 2 as 2 hex chars = 1 Byte
            totalFramePaddingBytes=""
            paddingSize=0
            # Calculate the padding size needed to align the frame length to the next multiple of 4
            if frameLength % 4 != 0:
                addition = 4 - frameLength % 4
                paddingSize += addition
            # Add padding bytes to the frame
            totalFramePaddingBytes = IFG.ifg_function(0, paddingSize)   #divide by 2 as 2 hex chars = 1 Byte
            dataToBeWrittenOnOutputFile += totalFramePaddingBytes
            
            payloadTotalSize -= FrameSize
            numOfSegments -= 1

        return dataToBeWrittenOnOutputFile

