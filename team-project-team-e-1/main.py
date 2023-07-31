import csv
import sys
import random
import psycopg2
import psqlConfig as config
import datasource




class Parser:
    '''
        @description: a class that takes command-line arguments from the user, tests them for correct format, and stores them to use in functions
        @args: command line filters inputted by the user at runtime
        @returns: None: creates object containing the inputted category and criterion
    '''
    
    def __init__(self, args):
        self.numArgs = len(args)
        self.noArgs = all(x == "" for x in args[1::2])
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
        self.service = []

        
        i = 0
        while i < self.numArgs and not self.noArgs:
            if isCategory(args[i]):
                category = args[i]
                i += 1
                while (i < self.numArgs) and not isCategory(args[i]):
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
                        self.description.append(args[i])
                    elif category in ["-ser","-service"]:
                        self.service.append(args[i])    
                    else:
                        print("ERROR:Invalid command line arguments.")
                        printUsage("filters")
                    i += 1
            else:
                print("ERROR:Invalid command line arguments.")
                printUsage("filters")
            
    #to access all the instance variables
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
    def getService(self):
        return self.service
    def isEmpty(self):
        return self.noArgs
    def getArgs(self):
        criteria = [[], [], [], [], [], [], [], [], [], [], [], []]
        criteria[0] = self.getType()
        criteria[1] = self.getTitle()
        criteria[2] = self.getDirector()
        criteria[3] = self.getCast()
        criteria[4] = self.getCountry()
        criteria[5] = self.getDateAdded()
        criteria[6] = self.getYear()
        criteria[7] = self.getRating()
        criteria[8] = self.getDuration()
        criteria[9] = self.getListedIn()
        criteria[10] = self.getDescription()
        criteria[11] = self.getService()
        return criteria
    def getCategories(self):
        categories = ["showtype", "title", "director", "actors", "country", "dateadded", "releaseyear", "rating", "duration", "genre", "synopsis", "platform"]
        return categories

def getMovie(parsedArgs):
    """
        @description: takes in a movie title, initializes the data, and searches for and returns a list containing all the info 
        pertaining to that movie
        @params: title - a Parser object that provides the title of the movie
        @returns: movieInformation - a list that has the information of a movie
    """
    titleList = parsedArgs.getTitle()
    isEmpty = len(titleList)<1

    if (isEmpty):
        printUsage("getMovie")

    title = titleList[0].strip()
    isTitle = len(title)>0

    if not isTitle:
        print("ERROR: Function getMovie needs a title argument (-ti \"title\"). ")
        sys.exit(title)

    database = datasource.DataSource()
    movieInformation = database.searchByTitle(title) #need to call dataSearch before increaseMoviePopularity
    increaseMoviePopularity(title)
    return movieInformation #Definitely clearer, not sure if it's actually less code


def getRandomMovie(parsedArgs):
    """
        @description: gives a random movie suggestion based off given criteria (uses getMovie and findMatchingMovies)
        @params: parsedArgs - a Parser object containing the search criteria as specified in the command line
        @returns:  getMovie - a list of the movie info using the function getMovie() as a helper
    """
    
    if parsedArgs.isEmpty():
        database = datasource.DataSource()
        movieArray = database.getAllTitles()
    else:
        movieArray = findMatchingMovies(parsedArgs)
    
    numMovies = len(movieArray)
    if numMovies == 0:
            return []

    randInt = random.randint(0,numMovies-1)
    parsedArgs = Parser(["-ti", movieArray[randInt]])

    return getMovie(parsedArgs)


def getPopularMovies():
    """
        @description: gives the most popular movie suggestions based off how often they have been searched for using getMovie and getRandomMovie
        @params: None
        @returns: popularMovieList - a list of the top 10 most popular movies as recorded in the populartitles database
    """
    database = datasource.DataSource()
    popularMovieList = database.getTopTenMovies()

    return datasource.formatToList(popularMovieList,returnTitles=True,isPopular=True)


def increaseMoviePopularity(movieTitle):
    """
        @description: Helper function for getMovie() - Updates populartitles database when a movie is viewed (increases movie's popularity by 1)
        @params: movieTitle - the movie that was just searched for in getMovie()
        @returns: None
    """
    database = datasource.DataSource()
    database.incrementMoviePopularity(movieTitle)


def isCategory(category):
    """
        @description: Helper function for Parser class - helps determine if a category is one of the listed headings in the dataset
        @params: category - given category shorthand we are testing
        @returns: Boolean representing if the category was valid or not
    """
    if category in ["-ty","-type", "-ti",
        "-title", "-di", "-director", "-ca","-a", 
        "-cast","-co","-country","-da","-date_added", "-y", "-year", "-r", "-rating","-du","-duration","-g","-genre","-de","-description","-ser","-service"]:
        return True
    return False


def findMatchingMovies(parsedArgs):
    """
        @description: gives a list of titles of movies matching the given filters; does an AND search, so any title returned
        must match all of the criteria
        @params: parsedArgs - the filters we are searching for
        @returns: matchingMovies - a list of movies matching the criteria
    """
    dataSource = datasource.DataSource()
    movies =  dataSource.findMatchingMoviesHelper(parsedArgs)
    return datasource.formatToList(movies,returnTitles=True,isPopular=False)



def Usage():
    """
        @description: Loads the usage statement as an array so that we may index the txt file
        @params: None
        @return: array containing each line of the usage statement as an element
    """
    with open("usage_message.txt") as f: # The with keyword automatically closes the file when you are done
        usageArray = []
        line = f.readline()
        while line:
         usageArray.append(line.strip())
         line = f.readline()
        
        return usageArray


def printUsage(functionName):
    """
        @descrption: prints either the general usage statement, or the statement
        for the desired function
        @params: function name
        @returns: None
    """
    usage = Usage()
    for i in range(0, 3):
        print(usage[i])
    if functionName == "general":
        for i in range(3, 24):
            print(usage[i])
    if functionName == "getMovie":
        for i in range(24, 30):
            print(usage[i])
    
    if functionName == "getRandomMovie":
        for i in range(30, 42):
            print(usage[i])
    
    if functionName == "findMatchingMovies":
        for i in range(42, 54):
            print(usage[i])
    
    if functionName == "getPopularMovie":
        for i in range(54, 61):
            print(usage[i])
    
    if functionName == "filters":
        for i in range(61, 83):
            print(usage[i])
    sys.exit(sys.argv)


def processUsage(system_args):
    potentialFunctions = ["getMovie", "findMatchingMovies", "getRandomMovie", "getPopularMovies"]
    #print usage statements
    if(len(system_args) < 2):
        printUsage("general")
    if (system_args[1] not in potentialFunctions):
        if system_args[1] in ["help", "-help", "usage", "-usage"]:
            if(len(system_args) < 3):
                printUsage("general")
            functionName = system_args[2]
            if functionName in potentialFunctions:
                printUsage(functionName)
            if functionName == "filters":
                printUsage(functionName)
            else:
                printUsage("general")
        else:
            printUsage("general")


def callFunction(system_args):
    functionName = system_args[1]
    parsedArgs = Parser(system_args[2:])
    if functionName == "getMovie":
        if (len(system_args) < 3):
            printUsage("getMovie")
        print(getMovie(parsedArgs))
    elif functionName == "findMatchingMovies":
        print(findMatchingMovies(parsedArgs))
    elif functionName=="getRandomMovie":
        print(getRandomMovie(parsedArgs))
    elif functionName == "getPopularMovies":
        print(getPopularMovies())   
    else:
        print("You should not be here... it is not possible. You have broken logic.", file = sys.stderr)
        sys.exit(functionName)


def main():
    """
        @description: our main method that runs when main.py is called; checks if user input is incomplete and calls an error, 
        if not puts arguments into the Parser class and calls the correct function
        @params: None
        @returns: None
    """
    potentialFunctions = ["getMovie", "findMatchingMovies", "getRandomMovie", "getPopularMovies"]
    if (len(sys.argv) < 2 or sys.argv[1] not in potentialFunctions):
        processUsage(sys.argv)
    else:
        callFunction(sys.argv)
    #pull function and args


if __name__ == '__main__':
    main()
