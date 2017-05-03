import os.path
import reader
import sys

def load_config(config_path):

    #loadconfig
    config_dir = os.path.dirname(config_path)
    config_name = os.path.splitext(config_path)[0]

    if len(config_dir) != 0:
        config_dir += "/"
    with open(config_path) as f:
        config = f.readlines()
        for line in config:
            #assigns values from config as variables
            line = line.split(' ')
            variable = line[0]
            if line[0] == "ignore":
                for arguments in line[1:]:
                    ignore.append(config_dir + arguments.strip())
            else:
                if line[0].startswith(("label", "output")):
                    argument = " ".join(str(x) for x in line[1:]).strip()
                else:
                    if "." in line[1]:
                        try:
                            argument = float(line[1])
                        except ValueError:
                            print(variable + " should be a float")
                    else:
                        try:
                            argument = int(line[1])
                        except ValueError:
                            print(variable + " should be an integer")
                exec(variable + ' = argument')
