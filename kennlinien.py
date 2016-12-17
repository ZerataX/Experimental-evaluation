import numpy as np
import math
import csv
import os.path
import glob


def export_csv(v1, v2, v3, v4, filename):
    csvpath = "changed_"+filename
    try:
        np.savetxt(
           csvpath,
           np.c_[v1, v2, v3, v4],
           fmt=['%.4f','%.7f', '%.4f', '%.8f'],
           delimiter=',',
           newline='\n',
           # footer='end of file',
           # comments='# ',
           #header='X , MW'
        )
    except TypeError:
        print("TypeError occured")
        print(v1)
        print(v2)
        print(v3)
        print(v4)


for file in glob.glob("*.csv"):
    if not file.startswith(("changed", "wheatstone")):
        U_values = []
        U_uncertain = []
        A_values = []
        A_uncertain = []
        f = lambda x: x/(2*math.sqrt(3))
        sub = lambda stri: stri[:-1]
        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                if not row[0].startswith("#"):
                    try:
                        U_values.append(str(row[0]))
                        A_values.append(str(row[1]))
                    except:
                        print("ERROR: " + file)
                        print(row)
        for index, a in enumerate(A_values):
            if a[-1:] == 'u':
                #A_values[index] = float(sub(a))*(10**(-6))
                A_values[index] = float(sub(a))*10**3
                A_uncertain.append(f(5e-8))
            elif a[-1:] == 'm':
                #A_values[index] = float(sub(a))*(10**(-3))
                A_values[index] = float(sub(a))
                if float(sub(a)) < 2:
                    A_uncertain.append(f(5e-7))
                elif float(sub(a)) < 20:
                    A_uncertain.append(f(5e-6))
                else:
                    A_uncertain.append(f(5e-5))
            elif a == '0':
                A_uncertain.append(0)
                A_values[index] = 0.0
            else:
                A_uncertain.append(0)
                A_values[index] = 999.999
        for index, u in enumerate(U_values):
            if "." not in u:
                if u == "0":
                    U_uncertain.append(0)
                else:
                    print("Error at {} in {}".format(str(index), file))
                    U_uncertain.append("##")
            else:
                U_uncertain.append(5*10**(-1-len(u.split(".")[-1:][0])))
                U_values[index] = float(u)
        #print(U_values)
        #print(U_uncertain)
        #print(A_values)
        #print(A_uncertain)
        export_csv(U_values, A_values, U_uncertain, A_uncertain, file)
