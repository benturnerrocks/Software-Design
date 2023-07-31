from plistlib import load
from flask import Flask
import csv
import main
import sys

app = Flask(__name__)

@app.route('/usage/', strict_slashes=False)
def usage() -> str:
    """
    @description: displays the usage text as given by the usage_message.txt file
    @params: None - the file is predetermined
    @return: the string to be displayed on the webpage for usage
    """
    with open("usage_message.txt") as f: # The with keyword automatically closes the file when you are done
        return f.read()

def formatParser(category,criteria):
    """
    @description: helper function that formats the input from the url
    @params: category, criteria - 
    the category in which the criteria will pertain, the criteria to filter by
    @return: fullArgs - a list formatted in a way that our main.Parser function can take in
    """
    category = category.split("_")

    newArgs = []
    for arg in criteria.split("_"):
        print(arg)
        newArgs.append(arg.split("-"))

    fullArgs = []
    for i,criteria in enumerate(category):
        fullArgs.append(criteria)
        for eachArg in newArgs[i]:
            fullArgs.append(eachArg)
    return fullArgs

@app.route('/getRandomMovie/', strict_slashes=False)
def getRandomMovie(category = False,criteria = False) -> str:
    """
    @description: assigns the getRandomMovie function from main.py to a url. Should return a completely random movie
    @params: category,criteria - a user input for what to randomized 
    @return: the string to be displayed on the webpage for random movie/show
    """
    if not category and not criteria:
        parsedArgs = main.Parser([])
        
    return str(main.getRandomMovie(parsedArgs))

@app.route('/getRandomMovie/<category>/<criteria>/', strict_slashes=False)
def getFilteredRandomMovie(category = False,criteria = False) -> str:
    """
    @description: assigns the getRandomMovie function from main.py to a url. Should return a random movie from the filtered list of movies
    @params: category,criteria - a user input for what to randomized 
    @return: the string to be displayed on the webpage for random movie/show
    """

    fullArgs = formatParser(category,criteria)
    parsedArgs = main.Parser(fullArgs)

    return str(main.getRandomMovie(parsedArgs))

@app.route('/')
def homepage() -> str:
    """
    @description: creates a homepage that is used to tell users how to do different things
    @params: None
    @return: the string to be displayed on the webpage home screen
    """
    homeMessage = "Hello, this is the homepage. To generate a random movie, enter the url extension: /getRandomMovie/<categories>/<criteria> where categories is the categories we are filtering the data by (i.e. genre, title, director, etc) and criteria is what we specify those categories are. Multiple distinct categories or criteria should be separated by an underscore (_) and should follow the usage guidlines specified in /usage ex: /getRandomMovie/-ca/Klara Castanho or /getRandomMovie/-ca_-ti/Klara Castanho_Jaws"
    return homeMessage

#Error Checking for bad url formatting

@app.errorhandler(404)
def page_not_found(e):
    return "Sorry, wrong format, see homepage for proper url formatting"

#Error Checking for code specific issues in python

@app.errorhandler(500)
def python_bug(e):
    return "Eek, a bug! See url extension /usage for usage information."

if __name__ == '__main__':
    app.run()