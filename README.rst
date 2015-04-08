AIOHTTP OAuth Client
####################

.. _description:

AIOHTTP OAuth Client -- Short description.

.. _badges:

.. image:: http://img.shields.io/travis/klen/aioauth-client.svg?style=flat-square
    :target: http://travis-ci.org/klen/aioauth-client
    :alt: Build Status

.. image:: http://img.shields.io/pypi/v/aioauth-client.svg?style=flat-square
    :target: https://pypi.python.org/pypi/aioauth-client

.. image:: http://img.shields.io/pypi/dm/aioauth-client.svg?style=flat-square
    :target: https://pypi.python.org/pypi/aioauth-client

.. image:: http://img.shields.io/gratipay/klen.svg?style=flat-square
    :target: https://www.gratipay.com/klen/
    :alt: Donate

.. _contents:

.. contents::

.. _requirements:

Requirements
=============

- python >= 3.3

.. _installation:

Installation
=============

**AIOHTTP OAuth Client** should be installed using pip: ::

    pip install aioauth-client

.. _usage:

Usage
=====


.. code:: python

    # OAuth1

    twitter = Twitter(
        consumer_key='J8MoJG4bQ9gcmGh8H7XhMg',
        consumer_secret='7WAscbSy65GmiVOvMU5EBYn5z80fhQkcFWSLMJJu4',
    )

    request_token, request_token_secret = yield from twitter.get_request_token()

    authorize_url = twitter.get_authorize_url(request_token)

    # ...
    # Reload client to authorize_url and get oauth_verifier
    # ...

    oauth_token, oauth_token_secret = yield from twitter.get_access_token(oauth_verifier)

    # Save the tokens for later use

    # ...

    twitter = Twitter(
        consumer_key='J8MoJG4bQ9gcmGh8H7XhMg',
        consumer_secret='7WAscbSy65GmiVOvMU5EBYn5z80fhQkcFWSLMJJu4',
        oauth_token=oauth_token,
        oauth_token_secret=oauth_token_secret,
    )

    timeline = yield from twitter.request('GET', 'statuses/home_timeline.json')

.. code:: python

    # OAuth2

    github = GithubClient(
        client_id='b6281b6fe88fa4c313e6',
        client_secret='21ff23d9f1cad775daee6a38d230e1ee05b04f7c',
    )

    authorize_url = github.get_authorize_url()

    # ...
    # Reload client to authorize_url and get code
    # ...

    otoken = yield from github.get_access_token(code)

    # Save the token for later use

    # ...

    github = GithubClient(
        client_id='b6281b6fe88fa4c313e6',
        client_secret='21ff23d9f1cad775daee6a38d230e1ee05b04f7c',
        access_token=otoken,
    )

    user_info = github.request('GET', 'user')


Example
-------

Run example with command: ::

    make run

Open http://fuf.me:5000 in your browser.

.. _bugtracker:

Bug tracker
===========

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/klen/aioauth-client/issues

.. _contributing:

Contributing
============

Development of AIOHTTP OAuth Client happens at: https://github.com/klen/aioauth-client


Contributors
=============

* klen_ (Kirill Klenov)

.. _license:

License
=======

Licensed under a `MIT license`_.

.. _links:


.. _klen: https://github.com/klen

.. _MIT license: http://opensource.org/licenses/MIT
