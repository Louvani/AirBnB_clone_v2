#!/usr/bin/python3
'''module'''

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    states = storage.all(State)
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def cities_by_id(id):
    states = storage.all(State)
    key = 'State.' + id
    if key in states.keys():
        state = states[key]
        cities = storage.all(City)
        return render_template(
            '9-states.html', state=state, cities=cities)
    else:
        return render_template('9-states.html')


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
