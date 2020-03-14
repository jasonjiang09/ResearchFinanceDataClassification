from xlutils.copy import copy
from xlrd import open_workbook
from xlwt import easyxf

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import datetime
import operator

filePath = "Tweet Data.xls"
analyser = SentimentIntensityAnalyzer()

readBook = open_workbook(filePath)
readSheet = readBook.sheet_by_index(0)

writeBook = copy(readBook)
writeSheet = writeBook.get_sheet(0)

fileObj = open("Matrix.txt", "w+")

row = 0
matrix = []
count = 2

for i in range (1, readSheet.nrows):
    tweet = TextBlob(readSheet.cell(i, 3).value)
    value = readSheet.cell(i, 3).value
    timeStr = readSheet.cell(i, 5).value
    timeObj = datetime.datetime.strptime(timeStr, '%Y-%m-%d %H:%M:%S')
    marketOpenTime = datetime.datetime(timeObj.year, timeObj.month, timeObj.day, 8, 30, 0)
    marketCloseTime = datetime.datetime(timeObj.year, timeObj.month, timeObj.day, 14, 50, 0)

    if ((timeObj > marketOpenTime) and (timeObj < marketCloseTime) and (timeObj.weekday() < 5)):
        '''
        data.append(readSheet.cell(i, 0).value)
        data.append(readSheet.cell(i, 9).value)
        data.append(readSheet.cell(i, 10).value)
        data.append(tweet.sentiment.polarity)
        data.append(tweet.sentiment.subjectivity)
        data.append(analyser.polarity_scores(value)["neg"])
        data.append(analyser.polarity_scores(value)["neu"])
        data.append(analyser.polarity_scores(value)["pos"])
        data.append(analyser.polarity_scores(value)["compound"])
        data.append(timeObj.date())
        

        matrix.append([])
        matrix[row].append(readSheet.cell(i, 0).value)
        matrix[row].append(readSheet.cell(i, 9).value)
        matrix[row].append(readSheet.cell(i, 10).value)
        matrix[row].append(tweet.sentiment.polarity)
        matrix[row].append(tweet.sentiment.subjectivity)
        matrix[row].append(analyser.polarity_scores(value)["neg"])
        matrix[row].append(analyser.polarity_scores(value)["neu"])
        matrix[row].append(analyser.polarity_scores(value)["pos"])
        matrix[row].append(analyser.polarity_scores(value)["compound"])
        matrix[row].append(timeObj.date().year)
        matrix[row].append(timeObj.date().month)
        matrix[row].append(timeObj.date().day)
        '''

        score = readSheet.cell(i, 0).value + readSheet.cell(i, 9).value + readSheet.cell(i, 10).value
        if (score == 0):
            weight = 1
        elif ((score >= 1) and (score <= 3)):
            weight = 2
        elif ((score >= 4) and (score <= 9)):
            weight = 4
        elif (score >= 10):
            weight = 5

        #Try storing in variables and then calling them
        fileObj.write("%s %s %s %s %s %s %s %s %s %d%d%d %d\n" % (readSheet.cell(i, 0).value, readSheet.cell(i, 9).value, readSheet.cell(i, 10).value, tweet.sentiment.polarity, tweet.sentiment.subjectivity, analyser.polarity_scores(value)["neg"], analyser.polarity_scores(value)["neu"], analyser.polarity_scores(value)["pos"], analyser.polarity_scores(value)["compound"], timeObj.date().year, timeObj.date().month, timeObj.date().day, weight))
        
        print("%d %d %d %d %d" % (count, timeObj.date().day, timeObj.time().hour, timeObj.time().minute, timeObj.time().second))

        count += 1

        #tempMatrix[row].append(data)
        #data.clear()

        #Take action and store date, polarity, subjectivity, neg score, neutral score, pos score, and compound score in matrix
        #Store in temp list/matrix and then output in txt file
        #Format separated by spaces and new line
        #Each row is a tweet
        #Fixed number of tweets per day

    polarity = tweet.sentiment.polarity
    writeSheet.write(0, 11, "Polarity")
    writeSheet.write(i, 11, polarity)

    subjectivity = tweet.sentiment.subjectivity
    writeSheet.write(0, 12, "Subjectivity")
    writeSheet.write(i, 12, subjectivity)

    score = analyser.polarity_scores(value)

    writeSheet.write(0, 13, "Negative Score (0 to 1)")
    writeSheet.write(i, 13, score["neg"])

    writeSheet.write(0, 14, "Neutral Score (0 to 1)")
    writeSheet.write(i, 14, score["neu"])

    writeSheet.write(0, 15, "Positive Score (0 to 1)")
    writeSheet.write(i, 15, score["pos"])

    writeSheet.write(0, 16, "Compound Score (Overall score: -1 to 1)")
    writeSheet.write(i, 16, score["compound"])

'''
count = 2
for i in matrix:
    #print(i[0], " ", i[1], "", i[2], " ", i[3], " ", i[4], " ", i[5], " ", i[6], " ", i[7], " ", i[8], " ", i[9])
    print(count)
    fileObj.write("%s %s %s %s %s %s %s %s %s" % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]))
    fileObj.write("\n")
    count += 1
'''

fileObj.close()
writeBook.save("Sentimental Results.xls")

#Account for difference in day
'''
numDates = 0
dateList = []
for i in range (0, row):
    dateList.append(tempMatrix[i][9])

tempDateObj = datetime.datetime.strptime(dateList[0], '%Y-%m-%d %H:%M:%S')
tweetPerDay = 0
tweetNumList = []


for i in dateList:
    day = datetime.datetime.strptime(i, '%Y-%m-%d %H:%M:%S')
    if (tempDateObj.date() != day.date()):
        numDates += 1
        tweetNumList.append(tweetPerDay)
        tempDateObj = day
        tweetPerDay = 0
    tweetPerDay += 1
    if (i == dateList[-1]):
        numDates += 1
        tweetNumList.append(tweetPerDay)
        tempDateObj = day
        tweetPerDay = 0


currentTweet = 0
topValIndex = 0

#Change this variable to change num tweets accepted per day
constNumTweetsPerDay = 3

for numDays in range (0, numDates):
    valList = []
    for numTweets in range (0, tweetNumList[numDays]):
        tempTuple = (numTweets, tempMatrix[currentTweet][0] + tempMatrix[currentTweet][1] + tempMatrix[currentTweet][2])
        valList.append(tempTuple)
        if (tweetNumList[numDays]-1 == numTweets):
            currentTweet += 1
            break
        currentTweet += 1
    valList.sort(key = operator.itemgetter(1), reverse = True)

    for index in range(0, constNumTweetsPerDay):
        topValIndex += valList[index][0]
        matrix.append(tempMatrix[topValIndex])
    topValIndex = currentTweet
'''