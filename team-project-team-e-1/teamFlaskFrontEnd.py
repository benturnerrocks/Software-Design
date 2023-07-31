import csv
from flask import Flask, render_template, request
import main
import datasource
 


app = Flask(__name__)
logosImg = ["https://cdn.vox-cdn.com/thumbor/Yq1Vd39jCBGpTUKHUhEx5FfxvmM=/39x0:3111x2048/1200x800/filters:focal(39x0:3111x2048)/cdn.vox-cdn.com/uploads/chorus_image/image/49901753/netflixlogo.0.0.png","https://upload.wikimedia.org/wikipedia/commons/e/e4/Hulu_Logo.svg","https://cdn.pastemagazine.com/www/articles/2019/10/18/disney-plus.jpg","https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Amazon_Prime_Video_logo.svg/2560px-Amazon_Prime_Video_logo.svg.png"]
logosLinks = ["https://www.netflix.com/browse","https://www.hulu.com","https://www.disneyplus.com/","https://www.amazon.com/Amazon-Video/b/?ie=UTF8&node=2858778011&ref_=nav_cs_prime_video"]
streamingDatabase = datasource.DataSource()

def getHomepage():
    """
        @description: displays the homepage text as given by the usage_message.txt file
        @params: None - the file is predetermined
        @return: the string to be displayed on the webpage for usage
    """
    with open("homepage.txt") as f: 
        return f.read()

def getCategories():
    """@description: Loads dropdown categories for the homepage by taking in the dataset
    and running through the list of genres and ratings
        @params:None
        @return: genres and ratings, which are the full list of genres and ratings used in the table"""
    genres = []
    ratings = []
    cursor = streamingDatabase.connection.cursor()
    ratings = getRatings(cursor)
    genres = getGenres(cursor)
    release_year = getYears(cursor)
    #cast = getCast(cursor)
    cast = []
    movies = makeUniqueList(streamingDatabase.getAllTitles(), reverse=False)
    countries = getCountries(cursor)
    return genres, ratings, release_year, movies, countries, cast

def getRatings(cursor):
    """@description: Helper function that loads list of unique ratings from database
        @params:Cursor pointing to database
        @returns: ratings
    """
    ratings = []
    ratingQuery = "SELECT rating FROM movies"
    cursor.execute(ratingQuery)
    ratingAggregate = list(cursor.fetchall())
    for rating in ratingAggregate:
        if rating[0] != None:
            rating = ', '.join(rating)
            rating = rating.strip()
            if rating not in ratings:
                ratings.append(rating)
    return ratings

def getGenres(cursor):
    """@description: Helper function that loads list of unique genres from database
        @params: Cursor pointing to database
        @returns: list of all genres
    """
    genres = []
    genreQuery = "SELECT genre FROM movies"
    cursor.execute(genreQuery)
    genreAggregate = list(cursor.fetchall())
    return makeUniqueList(genreAggregate, reverse = False)

def getCast(cursor):
    """@description: Helper function that loads list of unique cast members from database
        @params: Cursor pointing to database
        @returns: list of all cast members
    """
    cast = []
    castQuery = "SELECT actors FROM movies"
    cursor.execute(castQuery)
    castAggregate = list(cursor.fetchall())
    return makeUniqueList(castAggregate, reverse = False)

def getYears(cursor):
    """@description: Helper function that loads list of unique years from database
        @params: Cursor pointing to database
        @returns: list of all release years
    """

    yearQuery = "SELECT releaseyear FROM movies"
    cursor.execute(yearQuery)
    years = datasource.formatToList(cursor.fetchall(),returnTitles=False,isPopular=False)
    return makeUniqueList(years, reverse = True)

def getCountries(cursor):
    """@description: Helper function that loads list of unique countries from database
        @params:Cursor pointing to database
        @returns: list of all countries
    """

    countryQuery = "SELECT country FROM movies"
    cursor.execute(countryQuery)
    countries = datasource.formatToList(cursor.fetchall(),returnTitles=False,isPopular=False)
    return makeUniqueList(countries, reverse = False)

def makeUniqueList(messyList, reverse = False):
    """@description: Helper function for the "get" functions above that processes tuples and lists within lists
        to put all items in a single list 
        @params:Aggregate of each movie's genre label
        @returns: List of unique genre labels
    """
    uniquelist = []
    messyList = [list(filter(None, i)) for i in messyList]
    for item in messyList:
        if item==[]:
            continue
        item = ', '.join(item)
        if ',' in item:
            itemGrouping = item.split(',')
            for item in itemGrouping:
                item = item.strip() 
                if item not in uniquelist:
                    uniquelist.append(item)  
        else:
            item = item.strip()
            if item not in uniquelist:
                uniquelist.append(item)
    return sorted(uniquelist,reverse=reverse)



allCategories = getCategories()
homepage_message = str(getHomepage())
@app.route('/')
def homepage():
    """@description: Loads genre and rating lists, along with the three top films, then opens the html file
    for the homepage with those inputs
        @params:None
        @return: Formatted home page with search form and popular movies"""
    genreList, ratingList, releaseyears, movies, countries, cast = allCategories
    topFilms = main.getPopularMovies()[0:3]
    return render_template("home.html", genreList = genreList, ratingList = ratingList, yearList = releaseyears, movieList = movies, countryList = countries[1:], castList = cast, topFilms = topFilms)

@app.route('/moviepage')
def moviePage():
    """@description: Connects links on the movie results page to pages for individual movies
        @params:None
        @returns: Formatted movie template based on the movie selected"""
    title = request.args['title']
    parsedArgs = main.Parser(["-ti", title ])
    result = main.getMovie(parsedArgs)
    print(result)
    return render_template('movieInfo.html', type = result[0], title = result[1], director = result[2], cast = result[3], locations = result[4], dateAdded = result[5], releaseYear = result[6], rating = result[7], runtime = result[8], genres = result[9], description = result[10], streamingService = result[11],logos = logosImg,links=logosLinks)


@app.route('/search', methods =['GET', 'POST']) 
def functionSwitchboard():  
        """@description: Connects inputs from homepage form to either findMatchingMovies or getRandomMovie, sends the result to 
        matchingMovie.html
        @params:None
        @returns: Formatted movie search page based on the search categories selected in the form""" 
        title = request.args['titleChoice']
        genre = request.args['genreChoice']        
        director = request.args['directorChoice']
        entertainment = request.args['entertainmentType']
        cast = request.args['castChoice']
        country = request.args['countryChoice']
        year = request.args['yearChoice']
        rating = request.args['rating']
        streaming = request.args['Streaming']
        parsedArgs = main.Parser(["-ti", title, "-g", genre, "-di", director, "-ty", entertainment, 
        "-ca", cast, "-co", country, "-y", year, "-r", rating, "-ser", streaming])
        if request.args['randomnessChoice'] == "Random":
            movieInfo = main.getRandomMovie(parsedArgs)
            if movieInfo != []:
                movies = [movieInfo[1]]
                message = ""  
            else: 
                movies = []
                message = "No results!"
            keyword = "random matching movie"
        else:
            movies = main.findMatchingMovies(parsedArgs)
            if len(movies) == 0:
                message = "No results!"
            else:
                message = ""  
            keyword = "matching movies"  
        return render_template('matchingMovie.html', movies = movies, keyword=keyword, message = message)


@app.route('/popularmovies', strict_slashes=False)
def get_popular_movies():
    """
        @description: Returns a list of the most viewed movies as determined by popularMovies.txt 
        by running getPopularMovies() from main.py. 
        @return: getPopularMovies() - returns the list of popular movies in the matching movies html. 
    """
    return render_template('matchingMovie.html', movies = main.getPopularMovies(), keyword="popular movies")


@app.route('/FAQs', strict_slashes=False) 
def FAQpage():
    """
        @description: displays FAQ page
        @params: None
        @returns: help.html
    """
    return render_template('help.html')

@app.route('/AboutUs', strict_slashes=False)
def aboutUs():
    """
        @description: displays About Us page
        @params: None
        @returns: aboutus.html
    """
    return render_template('/aboutus.html')


@app.errorhandler(404)
def page_not_found(e):
     return render_template("404.html")


@app.errorhandler(500)
def python_bug(e):
    return "Something went wrong with the program-- hopefully this bug will be fixed shortly."


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5129, debug=False)