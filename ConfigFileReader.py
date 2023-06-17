class ConfigFileReader:
    def file_reader(config_file):
        # Open the configuration file
        with open(config_file, 'r') as file:
            lines = file.readlines()

        # Process each line in the file
        parameter_values = []
        for line in lines:
            # Remove comments after "//"
            line = line.split('//')[0]

            # Remove spaces and split the line at "=" sign
            line = line.replace(" ", "").split("=")

            # Check if the line has valid content
            if len(line) == 2:
                value = line[1]

                # Remove "0x" prefix if present
                if value.startswith("0x"):
                    value = value[2:]

                parameter_values.append(value)

        return parameter_values
