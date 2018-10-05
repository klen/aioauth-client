AIOHTTP OAuth Client
####################

.. _description:

AIOHTTP OAuth Client -- OAuth support for Aiohttp/Asyncio.

.. _badges:

.. image:: http://img.shields.io/travis/klen/aioauth-client.svg?style=flat-square
    :target: http://travis-ci.org/klen/aioauth-client
    :alt: Build Status

.. image:: http://img.shields.io/pypi/v/aioauth-client.svg?style=flat-square
    :target: https://pypi.python.org/pypi/aioauth-client

.. image:: http://img.shields.io/pypi/dm/aioauth-client.svg?style=flat-square
    :target: https://pypi.python.org/pypi/aioauth-client

.. _contents:

.. contents::

.. _requirements:

Requirements
=============

- python >= 3.5

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
    from aioauth_client import TwitterClient

    twitter = TwitterClient(
        consumer_key='J8MoJG4bQ9gcmGh8H7XhMg',
        consumer_secret='7WAscbSy65GmiVOvMU5EBYn5z80fhQkcFWSLMJJu4',
    )

    request_token, request_token_secret, _ = yield from twitter.get_request_token()

    authorize_url = twitter.get_authorize_url(request_token)
    print("Open",authorize_url,"in a browser")
    # ...
    # Reload client to authorize_url and get oauth_verifier
    # ...
    print("PIN code:")
    oauth_verifier = input()
    oauth_token, oauth_token_secret, _ = yield from twitter.get_access_token(oauth_verifier)

    # Save the tokens for later use

    # ...

    twitter = TwitterClient(
        consumer_key='J8MoJG4bQ9gcmGh8H7XhMg',
        consumer_secret='7WAscbSy65GmiVOvMU5EBYn5z80fhQkcFWSLMJJu4',
        oauth_token=oauth_token,
        oauth_token_secret=oauth_token_secret,
    )

    # Or you can use this if you have initilized client already
    # twitter.access_token = oauth_token
    # twitter.access_token_secret = oauth_token_secret

    timeline = yield from twitter.request('GET', 'statuses/home_timeline.json')
    content = yield from timeline.read()
    print(content)

.. code:: python

    # OAuth2
    from aioauth_client import GithubClient

    github = GithubClient(
        client_id='b6281b6fe88fa4c313e6',
        client_secret='21ff23d9f1cad775daee6a38d230e1ee05b04f7c',
    )

    authorize_url = github.get_authorize_url(scope="user:email")

    # ...
    # Reload client to authorize_url and get code
    # ...

    otoken, _ = yield from github.get_access_token(code)

    # Save the token for later use

    # ...

    github = GithubClient(
        client_id='b6281b6fe88fa4c313e6',
        client_secret='21ff23d9f1cad775daee6a38d230e1ee05b04f7c',
        access_token=otoken,
    )

    # Or you can use this if you have initilized client already
    # github.access_token = otoken

    response = yield from github.request('GET', 'user')
    user_info = yield from response.json()


Example
-------

Run example with command: ::

    make run

Open http://localhost:5000 in your browser.

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

.. _license:

License
========

Licensed under a `MIT license`_.

If you wish to express your appreciation for the role, you are welcome to send
a postcard to: ::

    Kirill Klenov
    pos. Severny d. 8 kv. 3
    MO, Istra, 143500
    Russia


.. _links:


.. _klen: https://github.com/klen

.. _MIT license: http://opensource.org/licenses/MIT
