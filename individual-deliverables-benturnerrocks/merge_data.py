import sys
import csv

datasetsLoc = ['Data (CS257)/netflix_titles.csv','Data (CS257)/hulu_titles.csv','Data (CS257)/disney_plus_titles.csv','Data (CS257)/amazon_prime_titles.csv']
# open the file in the write mode
f = open('Data (CS257)/streaming_services.csv', 'w')

# create the csv writer
writer = csv.writer(f)
for i,file in enumerate(datasetsLoc):

    with open(file, newline='') as csvfile:
        
        streamingData = csv.reader(csvfile)
        
        #look at each row and if it is from a certain file then add the corresponding service
        for j,row in enumerate(streamingData):
            if i==0 and j==0:
                row.append("streaming_service")
            elif i==0 and j>0:
                row.append("Netflix")
            elif i==1 and j>0:
                row.append("Hulu")
            elif i==2 and j>0:
                row.append("Disney Plus")
            elif i==3 and j>0:
                row.append("Amazon Prime")
            
            if j!=0 or i==0:
                # write a row to the csv file
                writer.writerow(row)

# close the file
f.close()