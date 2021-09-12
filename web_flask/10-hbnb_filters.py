#!/usr/bin/python3
'''module'''

from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.city import City

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
	states = storage.all(State)
	amenities = storage.all(Amenity)
	cities = storage.all(City)
	return render_template(
		'10-hbnb_filters.html', states=states, amenities=amenities,
		cities=cities)


if __name__ == '__main__':
    app.run(debug=True, port=5000)