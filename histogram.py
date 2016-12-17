import csv
import glob
import math
import numpy as np
import os.path

import config
import uncertainties as unc

if not len(sys.argv) == 2:
    print("please give one configuration file\nEg: python histogram.py example.conf")
else:

    config.load_config(sys.argv[1])

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

            #write down variables
            with open(file[:-3] + "vars", "w") as text_file:
                text_file.write("rows " + str(len(values)) + "\n" +
                                "max " + str(max(values)) + "\n" +
                                "min " + str(min(values)) + "\n" +
                                "mu " + str(unc.mu(values)) + "\n" +
                                "sigma " + str(unc.sigm(values)) + "\n" +
                                "sigmaround " + str(round(unc.sigm(values), round_to_n)) + "\n" +
                                "muround " + str(round(np.mean(np.array(values)), round_to_n)) + "\n" +
                                "upper " + str(max(values)+(max(values)-min(values))*whitespace) + "\n" +
                                "lower " + str(min(values)-(max(values)-min(values))*whitespace) + "\n" +
                                "bars " + str(math.floor(1+math.log(len(values), round_to_n-1))) + "\n"
                                )
