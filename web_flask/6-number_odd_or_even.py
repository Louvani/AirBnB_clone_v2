#!/usr/bin/python3
'''module'''

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    text = text.replace('_', ' ')
    return 'C ' + text


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text='is cool'):
    text = text.replace('_', ' ')
    return 'Python %s' % text


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    if not isinstance(n, int):
        return "None"
    else:
        return '{} is a number'. format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    if not isinstance(n, int):
        return "None"
    else:
        return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    if not isinstance(n, int):
        return "None"
    else:
        return render_template('6-number_odd_or_even.html', n=n)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
