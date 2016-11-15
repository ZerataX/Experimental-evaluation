import math
l = [0.421, 0.521, 0.661, 0.721, 0.96, 1.009, 1.121]
tsq = [1.69, 2.22, 2.69, 2.96, 4.41, 4.45, 4.53]
sigmT = [0.05, 0.3, 0.07, 0.34, 0.42, 0.46, 0.09]


def summe(arr1, arr2):
    summ = 0
    for i, j in zip(arr1, arr2):
        summ += (i-0.13-4.04*j)**2
        print(str(i) + " & " + str(j) + "\\\\")
    return summ


def delta(sigm, x):
    segment1 = 0
    segment2 = 0
    segment3 = 0
    # for i in sigm:
    #    segment1 += 1/i**2
    for i, j in zip(sigm, x):
        segment1 += 1 / i ** 2
        segment2 += (j/i)**2
        segment3 += (j/(i**2))
    return segment1 * segment2 - segment3 ** 2


def slope(sigm, x, y): # for y=slope*x+b
    part1 = 0
    part2 = 0
    part3 = 0
    part4 = 0
    # for i in sigm:
    #   part1 += 1 / i ** 2
    for si, xi, yi in zip(sigm, x, y):
        part1 += 1 / si ** 2
        part2 += (xi*yi)/(si**2)
        part3 += xi/(si**2)
        part4 += yi/(si**2)
    return (part1*part2-part3*part4)/delta(sigm,x)


def y_tic(sigm, x, y):
    parts = [0, 0, 0, 0]
    for si, xi, yi in zip(sigm, x, y):
        parts[0] += (xi**2)/(si**2)
        parts[1] += yi/(si**2)
        parts[2] += xi/(si**2)
        parts[3] += (yi*xi)/(si**2)
    return (parts[0]*parts[1] - parts[2]*parts[3])/delta(sigm, x)

def b_uncertain(sigm, x):
    part1 = 0
    for si in sigm:
        part1 += 1/si**2
    return part1/delta(sigm, x)

print("delta: " + str(delta(sigmT,l)))
print("slope: " + str(slope(sigmT, l, tsq)))
print("y-achsenabschnit: " + str(y_tic(sigmT,l,tsq)))
print("m Unsicherheit: " + str(b_uncertain(sigmT,l)))
