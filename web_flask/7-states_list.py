#!/usr/bin/python3
"""Lis of states."""
from flask import Flask
from flask import render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown(e):
    """Close the database."""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """States List route."""
    states = storage.all('State')
    data = { state.id : state.name for id, state in states.items() }
    sorted_dict = dict(sorted(data.items(), key=lambda item: item[1]))
    return render_template('7-states_list.html', states=sorted_dict)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
