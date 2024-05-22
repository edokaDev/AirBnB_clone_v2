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


@app.route('/states', strict_slashes=False)
def states_list():
    """Cities by states route."""
    states = storage.all(State)
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_by_id(id: str):
    """Cities by states route."""
    states = storage.all(State)
    state_id = 'State.{}'.format(id)
    state = states.get(state_id)
    return render_template('9-states.html', state=state)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
