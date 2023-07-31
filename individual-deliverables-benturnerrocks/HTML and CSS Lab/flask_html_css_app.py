from plistlib import load
from flask import Flask
import csv
from flask import render_template


app = Flask(__name__)

data = []

def load_data():
    #slightly weird syntax for reading from a file, but apparently the proper Pythonic way:
    with open('dataset.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)

@app.route('/<row>/<column>', strict_slashes=False)
def get_cell(row, column):
    return str(data[int(row)][int(column)])

@app.route('/greeting/<name>', strict_slashes=False)
def greeting(name):
    return render_template('greeting.html',name=name)

@app.route('/')
def homepage():
    return render_template('index.html', title="Silly Dataset", headings = data[0],headings2 = data[1])

@app.errorhandler(404)
def page_not_found(e):
    return "sorry, wrong format, do this instead...."

@app.errorhandler(500)
def python_bug(e):
    return "Eek, a bug!"

if __name__ == '__main__':
    load_data()
    app.run()