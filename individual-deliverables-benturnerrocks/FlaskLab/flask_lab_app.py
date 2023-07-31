from plistlib import load
import csv
from flask import Flask, render_template, request



app = Flask(__name__)

data = []

def load_data():
    #slightly weird syntax for reading from a file, but apparently the proper Pythonic way:
    with open('dataset.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)

def getRowTitles():
    row_titles = []
    for row in data:
        row_titles.append(row[0])

    return row_titles

def getRowByTitle(title):
    for row in data:
        if row[0] == title:
            return row
    return []

@app.route('/<row>/<column>', strict_slashes=False)
def get_cell(row, column):
    return str(data[int(row)][int(column)])

@app.route('/greeting/<name>', strict_slashes=False)
def greeting(name):
    return render_template('greeting.html',name=name)

@app.route('/')
def homepage():
    return render_template('index.html', title="Silly Dataset", headings = data[0],headings2 = data[1], rows=getRowTitles())

@app.route('/displayrow', methods=['GET', 'POST'])
def display_row():
    if request.method == 'POST':
        row = int(request.form['rowchoice'])
    elif request.method == 'GET':
        row = int(request.args['rowchoice'])
    else:
        return 'Not a valid request protocol'

    return str(data[row]) 

@app.route('/rowbytitle')
def display_row_by_title():
    return str(getRowByTitle(request.args['rowchoice']))

@app.errorhandler(404)
def page_not_found(e):
    return "sorry, wrong format, do this instead...."

@app.errorhandler(500)
def python_bug(e):
    return "Eek, a bug!"

if __name__ == '__main__':
    load_data()
    app.run()