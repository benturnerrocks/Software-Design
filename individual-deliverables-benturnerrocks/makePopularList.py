import csv
import sys

with open('Data (CS257)/streaming_services.csv', newline='') as csvfile:
    data = csv.reader(csvfile)
    dataArray = []
    for row in data:
        dataArray.append(row)

movieFile = open("popularTitles.txt", "w")
for row in range(1,len(dataArray)):
    movieFile.write(dataArray[row][1])
    movieFile.write("|")
    movieFile.write(dataArray[row][2])
    movieFile.write("|")
    movieFile.write("0|")
    movieFile.write("\n")
movieFile.close()

