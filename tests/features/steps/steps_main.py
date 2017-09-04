"""Main steps."""

from multiprocessing import Process
from behave import given, when, then  # noqa
import requests


@given(u'I have a shortener server up')
def setup_server(context):
    """Start server up."""
    from contextlib import closing
    from functools import partial
    from shortmagnet import main
    import socket

    def find_free_port():
        """Find a free port."""
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sck:
            sck.bind(('', 0))
            return sck.getsockname()[1]

    port = find_free_port()

    context.base_url = "http://localhost:{}/".format(port)
    import sys

    sys.argv = [sys.argv[0], '--port', str(port)]

    context.server = Process(target=main)
    context.server.start()
    import time
    time.sleep(2)


@when(u'I make a {request} request to {url}')
def make_request(context, request, url):
    """Make a request of type request to given url."""
    base_url = context.base_url
    if url == "that string":
        url = base_url + context.result.text
    else:
        url = url.replace('{base_url}', base_url)
    try:
        context.result = getattr(requests, request.lower())(url)
    except requests.exceptions.InvalidSchema as msg:
        context.exception = str(msg)


@then(u'I receive a body with a string')
def string_in_body(context):
    """Check body."""
    assert len(context.result.text) < 7


@then(u'I get a redirect to {place}')
def redirect_found(context, place):
    """Assert we found a redirect."""
    assert place in context.exception


@then(u'I stop the server')
def stop_server(context):
    """Stop server."""
    context.server.terminate()
