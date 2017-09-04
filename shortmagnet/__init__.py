"""shortmag.net.

Magnet-oriented URL Shortener.
"""

from docopt import docopt


def main():
    """shortmagnet.

    Magnet-oriented URL Shortener.

    Usage: shortmagnet [options]
    """
    options = docopt(main.__doc__)
    print(options)
