import csv
from flask import Flask, render_template
import main
 


app = Flask(__name__)

def helperParser(title):
    """ 
        @description: Takes in the title inputted by the user, then modifies the underscores to spaces so it can be
        taken by the get movie function
        @params: The title entered in the browser
        @returns: The same title with underscores instead of spaces
    """
    parsedTitle = ""
    for i in range(0, len(title)):
        if title[i] == '_':
            parsedTitle = parsedTitle + ' '
        else:
            parsedTitle = parsedTitle + title[i]
    return parsedTitle

def getHomepage():
    """
        @description: displays the homepage text as given by the usage_message.txt file
        @params: None - the file is predetermined
        @return: the string to be displayed on the webpage for usage
    """
    with open("homepage.txt") as f: # The with keyword automatically closes the file when you are done
        return f.read()

homepage_message = str(getHomepage())
@app.route('/')
def homepage():
    """ 
        @description: Standard/default route: prints a welcome message on the homepage. 
        @params: None
        @returns: home message
    """
    return "Welcome to the homepage. " + homepage_message


@app.route('/getMovie/<title>', strict_slashes=False)
def getFilm(title):
    """ 
        @description: Starts up the getMovie function-- uses parameters in the browser to specify the title of the movie
        @params: /getMovie/<title>, with <title> replaced with user input
        @returns: Movie info for the selected title
    """
    parsedTitle = helperParser(title)
    print(parsedTitle)
    return str(main.getMovie(parsedTitle))


def formatParser(category,args):
    category = category.split("_")

    newArgs = []
    for arg in args.split("_"):
        print(arg)
        newArgs.append(arg.split("-"))

    fullArgs = []
    for i,criteria in enumerate(category):
        fullArgs.append(criteria)
        for eachArg in newArgs[i]:
            fullArgs.append(eachArg)
    return fullArgs


@app.route('/getRandomMovie/<category>/<args>/', strict_slashes=False)
def getRandomMovie(category,args) -> str:
    """
        @description: assigns the getRandomMovie function from main.py to a url.
        @params: args - a user input for what to randomized 
        @return: the string to be displayed on the webpage for random movie/show
    """
    fullArgs = formatParser(category,args)
    print(fullArgs)
    parsedArgs = main.Parser(fullArgs)
    return str(main.getRandomMovie(parsedArgs))


@app.route('/popularmovies', strict_slashes=False)
def get_popular_movies():
    """
        @description: Returns a list of the most viewed movies as determined by popularMovies.txt 
        by running getPopularMovies() from main.py. 
        @return: getPopularMovies() - the list of popular movies, which here is casted to a string type. 
    """
    return str(main.getPopularMovies())


@app.route('/findMatchingMovies/<category>/<criterion>', strict_slashes=False)
def matchingMovies(category, criterion):
    """
        @description: By going to a page /<category>/<criterion>, the category and search criterion
        are parsed into main.findMatchingMovies, and a list of movies matching the given
        search criterion is returned.
        @params: None
        @return: list of movies
    """
    args = formatParser(category,criterion)
    parsedArgs = main.Parser(args)
    movies = main.findMatchingMovies(parsedArgs)
    return render_template('matchingMovie.html', keyword = criterion, movies = movies)


def getUsage():
    """
        @description: displays the usage text as given by the usage_message.txt file
        @params: None - the file is predetermined
        @return: the string to be displayed on the webpage for usage
    """
    with open("usage_message.txt") as f: # The with keyword automatically closes the file when you are done
        return f.read()



@app.route('/usage/', strict_slashes=False)
def usage() -> str:
    return getUsage()


@app.errorhandler(404)
def page_not_found(e):
     return "Error: The URL you inputted did not map to a page. " + getHomepage()


@app.errorhandler(500)
def python_bug(e):
    return "Something went wrong with the program-- hopefully this bug will be fixed shortly."


if __name__ == '__main__':
    app.run()