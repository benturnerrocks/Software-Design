from plistlib import load
import csv
from flask import Flask, render_template, request
import os


app = Flask(__name__)

data = []

#loads data from csv file
def load_data():
    #slightly weird syntax for reading from a file, but apparently the proper Pythonic way:
    with open(os.path.abspath('favoriteBookWebsite/dataset.csv'), newline='') as f:
        reader = csv.reader(f)
        for book in reader:
            data.append(book)

def getBookTitles():
    """
    @description: helper function to get all the book titles
    @params: None - uses preexisting data from load_data()
    @return: a list of the book information
    """
    book_titles = []
    for book in data:
        book_titles.append(book[0])

    return book_titles

def getBookByTitle(title):
    """
    @description: helper function to get book info given a title
    @params: title - str title of book
    @return: a list of the book information
    """
    for book in data:
        if book[0] == title:
            return book
    return []

@app.route('/')
def homepage():
    """
    @description: displays the homepage
    @params: None
    @return: the rendered template to be displayed on the homepage
    """
    return render_template('project.html', title="Books Ahoy", books=getBookTitles())

@app.route('/bookbytitle', methods=['GET', 'POST'])
def display_book_by_title():
    """
    @description: displays a book info given the requested book title
    @params: None - the input comes from the GET request
    @return: the rendered template to be displayed on the webpage for a given search result
    """
    if request.method == 'POST':
        book = request.form['bookchoice']
    elif request.method == 'GET':
        book = request.args['bookchoice']
    else:
        return 'Not a valid request protocol'

    return render_template("getBook.html", title="Books Ahoy", info = getBookByTitle(book)) 

#web error check
@app.errorhandler(404)
def page_not_found(e):
    return "Sorry, wrong format. Please use the search bar on the homepage."

@app.errorhandler(500)
def python_bug(e):
    return "Eek, a bug!"

if __name__ == '__main__':
    load_data()
    app.run()