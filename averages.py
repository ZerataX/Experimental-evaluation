import numpy as np
import math
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import csv


def average(values):
    averages = []
    while True:
        print("-{}. Enter a value or a command".format(str(len(values) + 1)))
        user_input = input()
        try:
            values.append(float(user_input))
            averages.append(sum(values) / len(values))
            print("Ø: " + str(averages[len(values) - 1]))
        except ValueError:
            command = user_input.lower().split(" ")
            if command[0] == "print":
                print("############################")
                for index, (value, average) in enumerate(zip(values, averages)):
                    print("{}. Value: {} \n   Ø: {}".format(index + 1, value, average))
                print("############################")
                if len(command) == 2:
                    if command[1] == "matlab":
                        sigma = np.std(np.array(values))*math.sqrt(len(values))/math.sqrt(len(values)-1)
                        show_matlab(values, averages[-1], sigma)
                if len(command) > 2:
                    print("Too many argurments\nEg: print gnuplot")
            if command[0] == "export":
                if len(command) < 2:
                    print("Too few argurments\nEg: export gnuplot")
                # if len(command) > 2:
                #    print("Too many argurments\nEg: export gnuplot")
                if len(command) == 2:
                    if command[1] == "csv":
                            print("Input file name to save")
                else:
                    if command[1] == "csv":
                        filename = command[2]
                        if isinstance(filename, str):
                            export_csv(values, averages, filename)
                        else:
                            print("Filename is no string")
                    else:
                        print("Unknown command. Try gnuplot or csv")
            if command[0] == "set":
                try:
                    command[1] = int(command[1])
                    if len(command) > 3:
                        print("Too many argurments\nEg: set 5 20")
                    elif len(command) < 3:
                        print("Too few argurments\nEg: set 5 20")
                    elif command[1] <= len(values):
                        values[command[1] - 1] = float(command[2])
                        i = len(averages) - 1
                        while i > (command[1] - 1):
                            averages[i] = sum(values[:i]) / i + 1
                            i -= 1
                        print("Value set")
                    else:
                        print("Value does not yet exist")
                except ValueError:
                    print("Only use numbers:\nEg: \nEg: set 5 20")
            if command[0] == "exit" or command[0] == "q":
                break


def show_matlab(array, mu, sigma):

    x = mu + sigma * np.array(array)
    # the histogram of the data
    n, bins, patches = plt.hist(x, math.floor(1+math.log(len(array), 2)), normed=1, facecolor='green', alpha=0.75)

    # add a 'best fit' line
    y = mlab.normpdf(bins, mu, sigma)
    l = plt.plot(bins, y, 'r--', linewidth=1)

    plt.xlabel('X')
    plt.ylabel('Probability')
    plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=%d,\ \sigma=%d$' % (mu, sigma))
    plt.subplots_adjust(left=0.15)
    plt.grid(True)

    plt.show()

def export_csv(values, averages, filename):
    csvpath = filename+'.csv'

    np.savetxt(
        csvpath,
        np.c_[values, averages],
        fmt='%.2f',
        delimiter=',',
        newline='\n',
        # footer='end of file',
        # comments='# ',
        header='X , MW'
    )

values = []

average(values)
