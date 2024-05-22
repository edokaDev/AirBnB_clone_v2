#!/usr/bin/python3
"""Cities by states."""
from flask import Flask
from flask import render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown(e):
    """Close the database."""
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def states_list():
    """Cities by states route."""
    states = storage.all(State)
    return render_template('8-cities_by_states.html', states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
