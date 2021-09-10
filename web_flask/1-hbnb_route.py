#!/usr/bin/python3
'''module'''

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return 'HBNB!'


if __name__ == '__main__':
    app.run(debug=True, port=5000)
