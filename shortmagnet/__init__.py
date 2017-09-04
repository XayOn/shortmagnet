"""shortmag.net.

Magnet-oriented URL Shortener.
"""

import uuid
import configparser
from functools import partial
from docopt import docopt
from flask import Flask, request, redirect
from flask_redis import FlaskRedis


def create_app():
    """Create flask APP."""
    redis_store = FlaskRedis()
    app = Flask(__name__)
    redis_store.init_app(app)
    return app, redis_store


def index(param, redis_store):
    """Handle main route."""
    if request.method == "GET":
        return redirect(redis_store.get(param))
    assert param.startswith('magnet:')
    name = str(uuid.uuid4())[:5]
    redis_store.set(name, param)
    return name


def main():
    """shortmagnet.

    Magnet-oriented URL Shortener.

    Usage: shortmagnet [options]

    Options:
        --config=CONFIG  Config file
        --host=HOST      Host to listen on [default: 0.0.0.0]
        --port=PORT      Port to listen on [default: 8080]
    """
    options = docopt(main.__doc__)

    # Read config
    config = configparser.ConfigParser()
    config.add_section('main')
    config['main']['redis'] = "redis://localhost:6379/0"
    if options['--config']:
        config.read(options['--config'])

    # Create app and configure it
    app, redis_store = create_app()
    app.config['REDIS_URL'] = config['main']['redis']

    # Set up views
    app.add_url_rule(
        '/<param>', 'index', partial(index, redis_store=redis_store),
        methods=["GET", "POST"])

    # Run
    app.run(host=options['--host'], port=int(options['--port']))
