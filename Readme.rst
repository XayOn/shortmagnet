shortmag.net
-------------

.. image:: https://travis-ci.org/XayOn/shortmagnet.svg?branch=master
    :target: https://travis-ci.org/XayOn/shortmagnet

.. image:: https://coveralls.io/repos/github/XayOn/shortmagnet/badge.svg?branch=master
 :target: https://coveralls.io/github/XayOn/shortmagnet?branch=master

.. image:: https://badge.fury.io/py/shortmagnet.svg
    :target: https://badge.fury.io/py/shortmagnet


Simple magnet-oriented URL Shortener.

Using ``redis`` to store more than 700000 magnet links.


Launching the server
--------------------

::

    shortmagnet.

    Magnet-oriented URL Shortener.

    Usage: shortmagnet [options]

    Options:
    --config=CONFIG  Config file
    --host=HOST      Host to listen on [default: 0.0.0.0]
    --port=PORT      Port to listen on [default: 8080]


Usage
-----

Shortmag.net does not have an actual user interface.

You can issue a ``POST`` request against main url (``/``) with form data magnet=magnet:?xt=foobar&baz...
to request a short link, to wich the server will directly answer with a text response containing
the short name to be used

Or you can issue a ``GET`` request against /<short_name> to get the actual redirect, direclty and **without
any intermediate pages or ads**.


Creating Short links
++++++++++++++++++++


* **URL**

  /

* **Method:**

  `POST`

*  **Form Params**

   **Required:**

   `magnet=[complete_magnet_url]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `short_name`

* **Error Response:**
  * **Code:** 503


Getting magnet links
++++++++++++++++++++

* **URL**

  /<short_name>

* **Method:**

  `GET`

 * **Success Response:**

  * **Code:** 302 <br />


Examples
++++++++


Sample usage with python-requests::

    import requests
    short = requests.post('http://shortmag.net/', data={'magnet': 'magnet:foo'}).text
    requests.get(short)

