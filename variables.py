import csv
import glob
import math
import numpy as np
import os.path
import parser
import re
import sys

import uncertainties

#functions
def sigm(valuearray):
    return np.std(np.array(valuearray))*math.sqrt(len(valuearray))/math.sqrt(len(valuearray)-1)

def mu(valuearray):
    return np.mean(np.array(valuearray))

def function_array(valuearray):
    print("test")

if not len(sys.argv) == 2:
    print("please give one configuration file\nEg: python variables.py example.conf")
else:

    #variables
    paramaters= []
    xvalues= []
    yvalues= []
    ignore = []

    #loadconfig
    config_path = sys.argv[1]
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
        #turn str axis into an actual function
        yaxis = parser.expr(label_axis_y).compile()
        xaxis = parser.expr(label_axis_x).compile()

    #write histogram variables
    for file in glob.glob(config_dir + "*.csv"):
        if not file in ignore:
            values = []
            with open(file, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in reader:
                    try:
                        values.append(float(row[0]))
                    except ValueError:
                        pass

            #use filenames to create paramters
            paramaters.append(re.findall('(\d+-?\d*)([a-zA-Z]+)', os.path.basename(file)))
            for parameter in paramaters[-1]:
                if "-" in parameter[0]:
                    argument = float(parameter[0].replace("-", "."))
                else:
                    argument = int(parameter[0])
                exec(parameter[1] + ' = argument')

            #create x and y values
            x=eval(xaxis)
            xvalues.append(x)
            y=mu(values)
            y=eval(yaxis)
            yvalues.append(y)

            #write down variables
            with open(file[:-3] + "vars", "w") as text_file:
                text_file.write("rows " + str(len(values)) + "\n" +
                                "max " + str(max(values)) + "\n" +
                                "min " + str(min(values)) + "\n" +
                                "mu " + str(mu(values)) + "\n" +
                                "sigma " + str(sigm(values)) + "\n" +
                                "sigmaround " + str(round(sigm(values), round_to_n)) + "\n" +
                                "muround " + str(round(np.mean(np.array(values)), round_to_n)) + "\n" +
                                "upper " + str(max(values)+(max(values)-min(values))*whitespace) + "\n" +
                                "lower " + str(min(values)-(max(values)-min(values))*whitespace) + "\n" +
                                "bars " + str(math.floor(1+math.log(len(values), round_to_n-1))) + "\n"
                                )

    #write regression values
    with open(config_name + ".dat", "w") as text_file:
        # doesn't fullfil our uncertainties requirements
        text = ""
        for x,y in zip(xvalues, yvalues):
            text += "{} {}\n".format(round(x,3),round(y,3))
        text_file.write(text)

    #write regression variables
    with open(config_name + ".vars", "w") as text_file:
        # polyfit doesn't fullfil our uncertainties requirements
        fit = np.polyfit(xvalues, yvalues, 1)
        text_file.write("slope " + str(fit[0]) + "\n" +
                        "ydistance " + str(fit[1]) + "\n" +
                        "upper " + str(max(xvalues)+(max(xvalues)-min(xvalues))*whitespace) + "\n" +
                        "lower " + str(min(xvalues)-(max(xvalues)-min(xvalues))*whitespace) + "\n"
                        )
