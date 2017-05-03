import math
import numpy as np
import os.path
import parser
import re
import reader

import config
import uncertainties as unc

if not len(sys.argv) == 2:
    print("please give one configuration file\nEg: python regression.py example.conf")
else:

    config.load_config(sys.argv[1])

    #variables
    paramaters= []
    xvalues= []
    yvalues= []
    ignore = []

    #turn str axis into an actual function
    yaxis = parser.expr(label_axis_y).compile()
    xaxis = parser.expr(label_axis_x).compile()

    #open csvs and load values
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
        y=unc.mu(values)
        y=eval(yaxis)
        yvalues.append(y)

    #write regression values
    with open(config_name + ".dat", "w") as text_file:
        # doesn't fullfil our uncertainties requirements
        text = ""
        for x,y in zip(xvalues, yvalues):
            text += "{} {}\n".format(round(x,round_to_n),round(y,round_to_n))
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
