#Need to prepare data 9 stock days before first actual tweet day| 1 stock day after last actual tweet day
#Try predicting three days

import csv
import math

def movingAverage10(listVal10):
    temp = 0
    for i in listVal10:
        temp += i
    return (temp/10)

def movingAverage9(listVal9):
    temp = 0
    for i in listVal9:
        temp += i
    return (temp/9)

def movingAverage5(listVal5):
    temp = 0
    for i in listVal5:
        temp += i
    return (temp/5)

def momentum5(day0, day5):
    return (day5 - day0)

def momentum3(day0, day3):
    return (day3 - day0)

#Date  Open  High  Low  Close  AdjClose  Volume
#Column represents Day while Row represents Indicators

with open('NASDAQ (Jan 3 2000 - Dec 31 2018).csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    matrix = []

    for row in readCSV:
        matrix.append(row)
    matrix.pop(0)

for row in matrix:
    row[1] = float(row[1])
    row[2] = float(row[2])
    row[3] = float(row[3])
    row[4] = float(row[4])
    row[5] = float(row[5])
    row[6] = float(row[6])


fileObj = open("TechnicalIndicators.txt", "w")

#10 Day Simple Moving Average
for i in range (9, len(matrix)-1):
    tempList = [matrix[i-9][4], matrix[i-8][4], matrix[i-7][4], matrix[i-6][4], matrix[i-5][4], matrix[i-4][4], matrix[i-3][4], matrix[i-2][4], matrix[i-1][4], matrix[i][4]]
    fileObj.write(str(movingAverage10(tempList)))
    fileObj.write(" ")
fileObj.write("\n")

#5 Day Simple Moving Average
for i in range (9, len(matrix)-1):
    tempList = [matrix[i-4][4], matrix[i-3][4], matrix[i-2][4], matrix[i-1][4], matrix[i][4]]
    fileObj.write(str(movingAverage5(tempList)))
    fileObj.write(" ")
fileObj.write("\n")

#5 Day Momentum
for i in range (9, len(matrix)-1):
    fileObj.write(str(momentum5(matrix[i-5][4], matrix[i][4])))
    fileObj.write(" ")
fileObj.write("\n")

#3 Day Momentum
for i in range (9, len(matrix)-1):
    fileObj.write(str(momentum3(matrix[i-3][4], matrix[i][4])))
    fileObj.write(" ")
fileObj.write("\n")

#10 Day RSI
for i in range (9, len(matrix)-1):
    gain = 0
    loss = 0
    for j in range (0, 9):
        diff = matrix[i-j][4] - matrix[i-j-1][4]
        if (diff > 0):
            gain += diff
        elif (diff < 0):
            loss -= diff
    if (loss == 0):
        RS = 100
    else:
        RS = gain/loss
    RSI = 100 - ((100)/(1+RS))
    fileObj.write(str(RSI))
    fileObj.write(" ")
fileObj.write("\n")

#9 Day RSI Move
for i in range (9, len(matrix)-1):
    gain = 0
    loss = 0
    for j in range (0, 8):
        diff = matrix[i-j][4] - matrix[i-j-1][4]
        if (diff > 0):
            gain += diff
        elif (diff < 0):
            loss -= diff
    if (loss == 0):
        RS1 = 100
    else:
        RS1 = gain/loss
    RSI1 = 100 - ((100)/(1+RS1))

    gain = 0
    loss = 0
    for j in range (1, 9):
        diff = matrix[i-j][4] - matrix[i-j-1][4]
        if (diff > 0):
            gain += diff
        elif (diff < 0):
            loss -= diff
    if (loss == 0):
        RS2 = 100
    else:
        RS2 = gain/loss
    RSI2 = 100 - ((100)/(1+RS2))

    fileObj.write(str(RSI1 - RSI2))
    fileObj.write(" ")
fileObj.write("\n")


#9 Day Money Flow Index
for i in range (9, len(matrix)-1):
    gain = 0
    loss = 0
    for j in range (0, 9):
        typicalPrice1 = (matrix[i-j-1][2] + matrix[i-j-1][3] + matrix[i-j-1][4]) / 3
        moneyFlow1 = typicalPrice1 * matrix[i-j-1][6]
        typicalPrice2 = (matrix[i-j][2] + matrix[i-j][3] + matrix[i-j][4]) / 3
        moneyFlow2 = typicalPrice2 * matrix[i-j][6]
        diff = typicalPrice2 - typicalPrice1
        if (diff > 0):
            gain += moneyFlow2
        elif (diff < 0):
            loss += moneyFlow2
    if (loss == 0):
        moneyFlowRatio = 100
    else:
        moneyFlowRatio = gain/loss
    MFI = 100 - ((100)/(1+moneyFlowRatio))
    fileObj.write(str(MFI))
    fileObj.write(" ")
fileObj.write("\n")

#8 Day Money Flow Index Move
for i in range (9, len(matrix)-1):
    gain = 0
    loss = 0
    for j in range (0, 8):
        typicalPrice1 = (matrix[i-j-1][2] + matrix[i-j-1][3] + matrix[i-j-1][4]) / 3
        moneyFlow1 = typicalPrice1 * matrix[i-j-1][6]
        typicalPrice2 = (matrix[i-j][2] + matrix[i-j][3] + matrix[i-j][4]) / 3
        moneyFlow2 = typicalPrice2 * matrix[i-j][6]
        diff = typicalPrice2 - typicalPrice1
        if (diff > 0):
            gain += moneyFlow2
        elif (diff < 0):
            loss += moneyFlow2
    if (loss == 0):
        moneyFlowRatio1 = 100
    else:
        moneyFlowRatio1 = gain/loss
    MFI1 = 100 - ((100)/(1+moneyFlowRatio1))

    gain = 0
    loss = 0
    for j in range (1, 9):
        typicalPrice1 = (matrix[i-j-1][2] + matrix[i-j-1][3] + matrix[i-j-1][4]) / 3
        moneyFlow1 = typicalPrice1 * matrix[i-j-1][6]
        typicalPrice2 = (matrix[i-j][2] + matrix[i-j][3] + matrix[i-j][4]) / 3
        moneyFlow2 = typicalPrice2 * matrix[i-j][6]
        diff = typicalPrice2 - typicalPrice1
        if (diff > 0):
            gain += moneyFlow2
        elif (diff < 0):
            loss += moneyFlow2
    if (loss == 0):
        moneyFlowRatio2 = 100
    else:
        moneyFlowRatio2 = gain/loss
    MFI2 = 100 - ((100)/(1+moneyFlowRatio2))

    fileObj.write(str(MFI1 - MFI2))
    fileObj.write(" ")
fileObj.write("\n")

#10 Day 1.5 SD Bollinger Upper Band
for i in range (9, len(matrix)-1):
    tempList = [matrix[i-9][4], matrix[i-8][4], matrix[i-7][4], matrix[i-6][4], matrix[i-5][4], matrix[i-4][4], matrix[i-3][4], matrix[i-2][4], matrix[i-1][4], matrix[i][4]]
    SMA = movingAverage10(tempList)
    for j in range(0, 10):
        summation = 0
        summation += (matrix[i-j][4] - SMA)**2
    average = summation/10
    SD = math.sqrt(average)
    upperBand = SMA + 1.5*SD
    fileObj.write(str(upperBand))
    fileObj.write(" ")
fileObj.write("\n")

#10 Day 1.5 SD Bollinger Lower Band
for i in range (9, len(matrix)-1):
    tempList = [matrix[i-9][4], matrix[i-8][4], matrix[i-7][4], matrix[i-6][4], matrix[i-5][4], matrix[i-4][4], matrix[i-3][4], matrix[i-2][4], matrix[i-1][4], matrix[i][4]]
    SMA = movingAverage10(tempList)
    for j in range(0, 10):
        summation = 0
        summation += (matrix[i-j][1] - SMA)**2
    average = summation/10
    SD = math.sqrt(average)
    lowerBand = SMA - 1.5*SD
    fileObj.write(str(lowerBand))
    fileObj.write(" ")
fileObj.write("\n")

#10 Day Stochastic Oscillator
for i in range (9, len(matrix)-1):
    lowest = matrix[i-9][4]
    highest = matrix[i-9][4]
    for j in range (0, 10):
        if (matrix[i-j][4] < lowest):
            lowest = matrix[i-j][4]
        if (matrix[i-j][4] > highest):
            highest = matrix[i-j][4]
    stochastic10 = ((matrix[i][4]-lowest) / (highest - lowest)) * 100
    fileObj.write(str(stochastic10))
    fileObj.write(" ")
fileObj.write("\n")

#10 Day Williams %R
for i in range (9, len(matrix)-1):
    lowest = matrix[i-9][4]
    highest = matrix[i-9][4]
    for j in range (0, 10):
        if (matrix[i-j][4] < lowest):
            lowest = matrix[i-j][4]
        if (matrix[i-j][4] > highest):
            highest = matrix[i-j][4]
    williams = ((highest - matrix[i][4]) / (highest - lowest)) * (-100)
    fileObj.write(str(williams))
    fileObj.write(" ")
fileObj.write("\n")

#Closing Price
for i in range (9, len(matrix)-1):
    fileObj.write(str(matrix[i][4]))
    fileObj.write(" ")
fileObj.write("\n")

#Opening Price
for i in range (9, len(matrix)-1):
    fileObj.write(str(matrix[i][1]))
    fileObj.write(" ")
fileObj.write("\n")

#High Price
for i in range (9, len(matrix)-1):
    fileObj.write(str(matrix[i][2]))
    fileObj.write(" ")
fileObj.write("\n")

#Low Price
for i in range (9, len(matrix)-1):
    fileObj.write(str(matrix[i][3]))
    fileObj.write(" ")
fileObj.write("\n")

#Label with Increase or Decrease between Closing Dates
for i in range (9, len(matrix)-1):
    outcome = matrix[i+1][4] - matrix[i][4]
    if (outcome >= 0 ):
        fileObj.write("1")
        fileObj.write(" ")
    else:
        fileObj.write("-1")
        fileObj.write(" ")
fileObj.write("\n")

fileObj.close()