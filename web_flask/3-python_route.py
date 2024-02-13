#!/usr/bin/python3
"""Hello Flask!."""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """Hello Flask."""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb_route():
    """HBNB Route."""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_route(text: str):
    """C Route."""
    text = text.replace('_', ' ')
    return "C {}".format(text)


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_route(text: str = "is cool"):
    """Python Route.

    This route uses multiple decorators to handle optional parameter cases.
    """
    text = text.replace('_', ' ')
    return "Python {}".format(text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
