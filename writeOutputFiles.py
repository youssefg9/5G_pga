
import os
class writeOutputFiles:
    
    def __process_file__(self, inp, out):
        input_file = inp
        output_file = out + "_4_BytesAllinged" +".txt"  # Use a temporary file for processing

        with open(input_file, "r") as input_file, open(output_file, "w") as output_file:
            for line in input_file:
                line = line.strip()  # Remove leading/trailing whitespace
                # Split the line into chunks of 8 characters
                chunks = [line[i:i+8] for i in range(0, len(line), 8)]

                # Write each chunk as a separate line in the output file
                for chunk in chunks:
                    output_file.write(chunk + "\n")



    def generateOutput(self, dataToBeWrittenOnOutputFile, output_file):
        with open(output_file, "w") as out_file:
            out_file.write(dataToBeWrittenOnOutputFile)
        self.__process_file__(output_file, output_file)


                