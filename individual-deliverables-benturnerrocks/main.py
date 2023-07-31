import csv
import sys
import random


def initializeData():
    with open('Data (CS257)/netflix_titles.csv', newline='') as csvfile:
        data = csv.reader(csvfile)
        dataArray = []
        for row in data:
            dataArray.append(row)
    return dataArray

def printUsage():
    with open("usage_message.txt") as f: # The with keyword automatically closes the file when you are done
        print(f.read())

def processGetMovie(parsedArgs):
    title = parsedArgs.getTitle()
    if len(title)==0:
        print("ERROR: Function getMovie needs a title argument (-ti \"title\"). ")
        printUsage()
        sys.exit(title)
    title = title[0]
    print(title)
    filmInfo = getMovie(title)
    return filmInfo

def getMovie(title):
    title = title.strip()
    movieInfo = dataSearch(title)
    increaseMoviePopularity(title)
    return movieInfo #Definitely clearer, not sure if it's actually less code

def dataSearch(keyword):
    dataArray = initializeData()
    keyword = keyword.strip()
    curRow = 1
    curMovie = dataArray[curRow][2]
    while curMovie != keyword:
        if curRow+1 == len(dataArray):
            print("ERROR: Title not found. Please make sure the title is accurate.", file = sys.stderr)
            printUsage()
            sys.exit(keyword)
        curRow += 1
        curMovie = dataArray[curRow][2]
    return dataArray[curRow]

#provides a random movie given certain criteria
def getRandomMovie(parsedArgs):
    dataArray = initializeData()
    #first check if there are no args
    if parsedArgs.isEmpty():
        randInt = random.randint(0,len(dataArray)-1)
        #also return it for testing
        return getMovie(dataArray[randInt][2])

    else:
        #filter data using criteria in arguments (if no args, full data is used)
        filteredData = findMatchingMovies(parsedArgs)
        #generate random number for this filter data
        randInt = random.randint(0,len(filteredData)-1)
        #return/print the random row from the subsetted data
        return getMovie(filteredData[randInt])


def getPopularMovies():
    finalList = []
    popularTitlesList = open("popularTitles.txt", 'r')
    for line in popularTitlesList:
        currline = line.split('|')
        if currline[0] == "Movie":
            finalList = updatePopularMoviesList(finalList, currline)
    popularTitlesList.close()

    return finishedPopularMoviesList(finalList)


#Helper function for getPopularMovies()
def updatePopularMoviesList(movieList, currentMovie):
    #ensures that the popular list has only 10 movies 
    if len(movieList) != 10:
        movieList.append([currentMovie[1], currentMovie[2]])
        movieList = bubble_sort(movieList)            

    #checks popularity of current movie with that of the least popular movie currently in the final list
    #always sorts after a change so the movies are always listed in ascending popularity order
    else:
        if movieList[0][1] < currentMovie[2]:
            movieList[0] = [currentMovie[1], currentMovie[2]]
            movieList = bubble_sort(movieList)

    return movieList


#Helper function for getPopularMovies()
#reorganizes final list so only titles are printed (ie respective popularity ranks aren't shown)
def finishedPopularMoviesList(popularMovieList):    
    count = 0
    for title in popularMovieList:
        popularMovieList[count] = title[0]
        count += 1
    return popularMovieList


#Helper function for getMovie()
#Updates popularTitles.txt when a movie is viewed (increases movie's popularity)
def increaseMoviePopularity(movieTitle):
    file = open('popularTitles.txt', 'r')
    allMoviesList = file.readlines()

    movieNewPopularity = ""
    counter = 0

    #finds the movie that was viewed and adds 1 to its popularity tracker
    for movieInfo in allMoviesList:
        tempMovieInfo = movieInfo.split('|')
        if movieTitle == tempMovieInfo[1]:
            tempMovieInfo[2] = int(tempMovieInfo[2]) + 1
            tempMovieInfo[2] = str(tempMovieInfo[2])
            movieNewPopularity = '|'.join(tempMovieInfo)
            break

        counter += 1 

    #rewrites the popularTitles file to reflect the viewed movie's new popularity tracker
    allMoviesList[counter] = movieNewPopularity
    file = open('popularTitles.txt', 'w')
    file.writelines(allMoviesList)  
    file.close()        

'''
This sorting algorithm was made by Santiago Valdarrama 
and taken from https://realpython.com/sorting-algorithms-python/#the-bubble-sort-algorithm-in-python.
Only the indices in the if statement were changed from the original function.
'''
def bubble_sort(array):
    n = len(array)

    for i in range(n):
        # Create a flag that will allow the function to
        # terminate early if there's nothing left to sort
        already_sorted = True

        # Start looking at each item of the list one by one,
        # comparing it with its adjacent value. With each
        # iteration, the portion of the array that you look at
        # shrinks because the remaining items have already been
        # sorted.
        for j in range(n - i - 1):
            if array[j][1] > array[j + 1][1]:
                # If the item you're looking at is greater than its
                # adjacent value, then swap them
                array[j], array[j + 1] = array[j + 1], array[j]

                # Since you had to swap two elements,
                # set the `already_sorted` flag to `False` so the
                # algorithm doesn't finish prematurely
                already_sorted = False

        # If there were no swaps during the last iteration,
        # the array is already sorted, and you can terminate
        if already_sorted:
            break

    return array


def isCategory(category):
    if category in ["-ty","-type", "-ti",
        "-title", "-di", "-director", "-ca","-a", 
        "-cast","-co","-country","-da","-date_added", "-y", "-year", "-r", "-rating","-du","-duration","-g","-genre","-de","-description"]:
        return True
    return False

class Parser:
    #takes command line arguments and parses them, sorts into categories
    #of search criteria. will have expanded utility in later iterations of the program
    def __init__(self, args):
        self.noArgs = True
        self.type = []
        self.title = []
        self.director = []
        self.cast = []
        self.country = []
        self.date_added = []
        self.release_year = []
        self.rating = []
        self.duration = []
        self.listed_in = []
        self.description = []

        if len(args)>0:
            self.noArgs = False
        i = 0
        while i < len(args):
            if isCategory(args[i]):
                category = args[i]
                i += 1
                while (i < len(args)) and not isCategory(args[i]):
                    if category in ["-ty","-type"]:
                        self.type.append(args[i])
                    elif category in ["-ti","-title"]:
                        self.title.append(args[i])
                    elif category in ["-di","-director"]:
                        self.director.append(args[i])
                    elif category in ["-ca", "-a", "-cast"]:
                        self.cast.append(args[i])
                    elif category in ["-co", "-country"]:
                        self.country.append(args[i])
                    elif category in ["-da","-date_added"]:
                        self.date_added.append(args[i])
                    elif category in ["-y","-year"]:
                        self.release_year.append(args[i])
                    elif category in ["-r","-rating"]:
                        self.rating.append(args[i])
                    elif category in ["-du","-duration"]:
                        self.duration.append(args[i])
                    elif category in ["-g","-genre"]:
                        self.listed_in.append(args[i])
                    elif category in ["-de","-description"]:
                        self.duration.append(args[i])  
                    else:
                        print("ERROR:Invalid command line arguments.")
                        printUsage()
                        sys.exit(args[i])
                    i += 1
            else:
                print("ERROR:Incorrect definition of a category.")
                printUsage()
                sys.exit(args[i])


    def getType(self):
        return self.type
    def getTitle(self):
        return self.title
    def getDirector(self):
        return self.director
    def getCast(self):
        return self.cast
    def getCountry(self):
        return self.country
    def getDateAdded(self):
        return self.date_added
    def getYear(self):
        return self.release_year
    def getRating(self):
        return self.rating
    def getDuration(self):
        return self.duration
    def getListedIn(self):
        return self.listed_in
    def getDescription(self):
        return self.description
    def isEmpty(self):
        return self.noArgs



def findMatchingMovies(parsedArgs):
    dataArray = initializeData()

    matchingMovies = []
    criteria = [[], [], [], [], [], [], [], [], [], [], [], []]
    criteria[1] = parsedArgs.getType()
    criteria[2] = parsedArgs.getTitle()
    criteria[3] = parsedArgs.getDirector()
    criteria[4] = parsedArgs.getCast()
    criteria[5] = parsedArgs.getCountry()
    criteria[6] = parsedArgs.getDateAdded()
    criteria[7] = parsedArgs.getYear()
    criteria[8] = parsedArgs.getRating()
    criteria[9] = parsedArgs.getDuration()
    criteria[10] = parsedArgs.getListedIn()
    criteria[11] = parsedArgs.getDescription()

    #for each row in the csv, check the content in each column
    #and see if it matches at least one of the search criteria.
    row = 0 
    while row < len(dataArray):
        isMatch = True
        for column in range(12):
            item = dataArray[row][column]
            itemWords = item.split(",")
            for word in itemWords:
                for criterion in criteria[column]:
                    if criterion.lower() in word.lower(): 
                        title = dataArray[row][2]
                        matchingMovies.append(title)
        row += 1

    return matchingMovies


def main():
    potentialFunctions = ["getMovie", "findMatchingMovies", "getRandomMovie", "getPopularMovies"]
    if(len(sys.argv) < 2 or sys.argv[1] not in potentialFunctions):
        print("ERROR:No function in command line.")
        printUsage()
        sys.exit(sys.argv)
    #pull function and args
    functionName = sys.argv[1]
    parsedArgs = Parser(sys.argv[2:])
    if functionName == "getMovie":
        print(processGetMovie(parsedArgs))
    elif functionName == "findMatchingMovies":
        print(findMatchingMovies(parsedArgs))
    elif functionName=="getRandomMovie":
        print(getRandomMovie(parsedArgs))
    elif functionName == "getPopularMovies":
        print(getPopularMovies())
    else:
        print("Function name not recognized.", file = sys.stderr)
        printUsage()
        sys.exit(functionName)


if __name__ == '__main__':
    main()