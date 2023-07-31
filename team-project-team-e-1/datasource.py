import csv
import sys
import random
import psycopg2
import psqlConfig as config

def formatToList(movies, returnTitles, isPopular):
    """
        @description: Helper method to change tupled list from database into list
        @params: a list of movies and a booleans indicating if we want to return only titles and if the list is from the popular data base
        @returns: a list of all the titles or movies.
    """
    allMovies = []
    i = 0
    numMovies = len(movies)
    #helper fcn lists of tuples containing all the info for each movie, and we just want the title
    while i < numMovies:
        movie = list(movies[i])
        if returnTitles:
            movie = movie[not isPopular]
        allMovies.append(movie)
        i = i + 1

    return allMovies

class DataSource:
        
    def __init__(self):
         self.connection = self.connect()

    def connect(self):
        try:
            connection = psycopg2.connect(database=config.database, user=config.user, password=config.password, host="localhost")
        except Exception as e:
            print("Connection error: ", e)
            exit()
        return connection

    def searchByTitle(self, title):
        """
            @description: Uses database query to return database row matching inputted title
            @params: A user inputted title
            @returns: movieDetails - a list of all the information pertaining to the certain movie
        """
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM movies WHERE title = %s"
            cursor.execute(query, (title,))
            movieDetails = formatToList(cursor.fetchall(),returnTitles=False,isPopular=False)[0]
        except Exception as e:
            print("ERROR:Title not found.", file = sys.stderr)
            sys.exit(title)

        return movieDetails   
        
    def getTopTenMovies(self):
        """
            @description: Uses database query to find ten movies with highest popularity 
            @params: None
            @returns: topTenMovies - list of tuples containing the ten most popular movies
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT title FROM populartitles ORDER BY popularity DESC LIMIT 10")
        topTenMovies = cursor.fetchall()

        return topTenMovies

    def incrementMoviePopularity(self,title):
        """
            @description: Uses database query to increment popularity of 
            @params: title - the movie that was just searched for in getMovie()
            @returns: None
        """
        cursor = self.connection.cursor()
        cursor.execute("UPDATE populartitles SET popularity = popularity + 1 WHERE title = %s",(title,))
        
    def findMatchingMoviesHelper(self, parsedArgs):
        """
            @description: Uses database query to find movies matching the given filters
            @params: parsedArgs - the filters we are searching for
            @returns: movies - the tupled list of matching movies
        """
        query = "SELECT * FROM movies"
        if not parsedArgs.isEmpty():
            query = query + " WHERE"

        categories = parsedArgs.getCategories()
        criteria = parsedArgs.getArgs()

        firstCategory = True
        for i in range(len(categories)):
            if criteria[i] != [] and criteria[i] != [''] :
                if firstCategory:
                    query = query + " {} ILIKE '%{}%'"
                    query = query.format(categories[i], str(criteria[i][0]))
                    firstCategory = False    
                else:        
                    query = query + " AND {} ILIKE '%{}%'"
                    query = query.format(categories[i], str(criteria[i][0]))
        try:
            cursor = self.connection.cursor()
            cursor.execute(query,)
            movies = cursor.fetchall()
        except Exception as e:
            print("ERROR: Parsed Args.", file = sys.stderr)
            print(e)
            sys.exit()

        return movies 
    
    def getAllMovies(self, returnTitles=False):
        """
            @description: Uses database query to retrieve all movies in the database
            @params: None
            @returns: allmovies - formatted to list of lists
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM movies")
        allMovies = cursor.fetchall()
        return formatToList(allMovies,returnTitles=returnTitles,isPopular=False)

    def getAllTitles(self):
        """
            @description: Uses database query to retrieve all titles in the database
            @params: None
            @returns: alltitles - formatted to list of lists
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT title FROM movies")
        allMovies = list(cursor.fetchall())
        allMovies = formatToList(allMovies,returnTitles=False,isPopular=False)
        allMovies = sum(allMovies,[])
        return allMovies