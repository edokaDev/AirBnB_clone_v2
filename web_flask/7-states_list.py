#!/usr/bin/python3
"""Lis of states."""
from flask import Flask
from flask import render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown(e):
    """Close the database."""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """States List route."""
    states = storage.all(State)
    states = {state.id: state.name for id, state in states.items()}
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
