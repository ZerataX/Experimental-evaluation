#import scipy.optimize as optimize
#import scipy.fftpack as fftpack
import csv
from numpy.fft import fft, fftshift
import numpy as np
import matplotlib.pyplot as plt
import glob

def w_guess(ydata):
    N = len(ydata)
    ynData = np.array(ydata) #numpy array

    window = np.hanning(N)
    ynData = window * ynData

    fs = 10  # Messdaten wurden mit 10 Hz aufgenommen

    fftx = np.fft.rfft(ynData)  # Reelle messwerte -> rfft gibt Array der N/2 Fourierkoeffizienten aus
    # Weitere N/2 Fourierkoeffizienten ergebne keine neue Informationen, da
    # sie lediglich komplex konjugierte der ersten sind.

    freq_fftx = np.linspace(0, fs / 2, len(fftx))
    # Frequenzen, zugehörig zu den Fourierkoeffizienten
    # Diese gehen von 0Hz....fs/2 Hz. in insgesamt N/2 Schritten.
    # Einzelne Werte errechnen sich wie folgt:
    # f_k = k/n * (fs/2), mit n = N/2 und k Index des Fourierkoeffizient
    fftx[0] = 0
    fftx[1] = 0
    # unschoen.... setzt die ersten Fourierkoeffizienten auf Null, um unsinnige Peaks bei Null loszuwerden.

    xmax = abs(fftx).argmax() # returns: Index von Element aus fftx mit größtem Betrag.

    ft = abs(fftx) # Beträge der Fourierkoeffizienten

    # Errechnet Mittelwert der Frequenz um den Peak, gewichtet mit den Fourierkoeffizienten.
    meanfreq = (
        (ft[xmax - 1] * freq_fftx[xmax - 1] + ft[xmax] * freq_fftx[xmax] + ft[xmax + 1] * freq_fftx[xmax + 1]) /
        (ft[xmax - 1] + ft[xmax] + ft[xmax + 1])
    )
    return meanfreq


def a_guess(ydata):
    return (min(yReal)-max(yReal))/2


for file in glob.glob("*.txt_fixed"):
    yReal = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            yReal.append(float(row[1]))
    name = file.split(".")[:1]
    values = [w_guess(yReal), a_guess(yReal)]
    print(name[0] + " w_guess = " + str(values[0]))
    print(name[0] + " a_guess = " + str(values[1]))
    f1name = name[0] + ".guess"
    f1 = open(f1name, 'w')
    values[0] = 2*np.pi*values[0]
    output = ["w_guess " + str(values[0]), "a_guess " + str(values[1])]
    for v in output:
        f1.write(v + "\n")
    f1.close()


#print(freq_fftx)

#print("a: " + str(a_guess))
#print("freq: " + str(meanfreq))
#print("period: " + str(1 / meanfreq))
