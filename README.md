# 5G_pga
how to run the code:
--------------------
  1-main.py is the function containing the needed classes and imports , it contains the following :
    a-generatorFunc function of class FrameGenerator()
    IN  : 
      1- input config file 
      2- is_IQ_data _if True then we can encapsulate ecpri type0 msg inside ethernet frame simulating fronthaul process_ 
      3- iq_payload  
      4- payload Total Size (random payload if is_IQ_data = False)
      5- crc Gen Polynomial _normally 100000100110000010001110110110111 in 802.3 but i made it dynamic for future updates_
      6- line Rate _used to convert from time to bytes_
    OUT : 
      802.3 std frames in 2 files ( explained below ) 
 -----------------------------------------------------------------------------------------------------------------------------     
    b-generate_ecpri_message function of class ecpriMessageGenerator() :
      IN  :
        iq_file that will be the payload of the ecpri message alongside the common header        
      OUT :
        ecpri message type 0
 -----------------------------------------------------------------------------------------------------------------------------       
    c-generateOutput function of class writeOutputFiles()
      IN: 
        1-string data to Be written on OutputFile 
        2-output file name
      OUT:
        1-one file called 4_bytes allinged is for ease of reviewing the files
        2-another normal non allinged file if needed








-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## some therotical explanations and assumptions in the code:
-------------------------------------------------------------

Assumptions:
1-line rate = 10 Gbps (helps in converting stream/burst periods to bytes sized capacities)
2-MTU for 802.3 --> min =64 bytes (46B payload) | max = 1518 bytes (1500B payload) 
but in our case we have a paramter called MAX_PACKET_SIZE defines the MTU , this is useful as we can use _jumbo frames_ instead of normal frames by tuning this value as we want
3-After sending the required burst frames , IFGs are sent as padding till the end of stream period
4-If bursts to be interrupted due to end of streaming time, 
Consider the following parameters:

Line rate = 10 Gbps
Total streaming duration: 47 us --> stream capacity=470 kb
Burst period: 5 us --> burst capacity=50 kb
frame period : 0.7us --> frames capacity = 7 kb
Frames per burst: 5 
In this scenario, Given that, in the last burst, the remaining streaming duration is 2us, so you can only transmit 2 frames worth 1.4us because the third frame would require 2.1us 
or it terms of bytes , 20 Kb is remaining before end of stream period ,which allows only for 2 frames transmission worth 14 kb and the remaining 6 kb are sent as IFGs 

Let's break down the transmissions within the 47 us stream period:
-bursts from 0 - 9  (45 us duration) sent 450 kb frames
-last burst: (2 us duration) sent 14 kb frames + 6 kb IFGs

5-Addresses class:
By encapsulating the addresses within a class, it can provide a clear and organized structure for managing related data, even if there are no additional methods or functionality at the moment. It also allows for potential future extensions where you might want to add more functionality to the class, such as validation or manipulation of the addresses.


eCPRI message:

eCPRI Message = Common Header + Payload
Common Header = Protocol Revision (8 bits) + Reserved (8 bits) + C-Bit (1 bit) + Message Type (8 bits) + Payload Size (16 bits)
Payload = Specific Payload

The Common Header is the same for all eCPRI messages. It contains the following fields:
-Protocol Revision: This field indicates the version of the eCPRI protocol.
-Reserved: This field is reserved for future use.
-C-Bit: This bit indicates whether the message is the first message in a sequence of eCPRI messages.
-Message Type: This field indicates the type of the eCPRI message.
-Payload Size: This field indicates the size of the payload in bytes.
-The Payload is specific to the type of eCPRI message. For example, the payload for an eCPRI Message Type 0 message contains the following fields: PCID + Sequence ID + IQ Data


Here is the structure of an eCPRI Message Type 0 format:
eCPRI Message Type 0 = Common Header + PCID + Sequence ID + IQ Data

-The PCID field is a 16-bit field that identifies the processing chain ID. 
-The Sequence ID field is a 16-bit field that identifies the sequence number of the message. 
-The IQ Data field is a variable-length field that contains the IQ data.

The common header is only sent with the first message in a burst. This is because the common header contains information about the burst, such as the number of messages in the burst and the size of the payload. This information is only needed for the first message, so it is not sent with the subsequent messages in the burst.

The C-bit (Continuation Bit) in the common header indicates whether the message is the first message in a sequence of eCPRI messages. If the C-bit is set to 1, then the message is the first message in the sequence. If the C-bit is set to 0, then the message is not the first message in the sequence.

The C-bit is used by the receiver to determine whether the message is the first message in the sequence. If the C-bit is set to 1, then the receiver must read the common header to get the information about the burst. If the C-bit is set to 0, then the receiver does not need to read the common header, because the information about the burst is already known.


