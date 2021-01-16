AIOAuth Client
##############

.. _description:

AIOAuth Client -- OAuth support for Asyncio_ / Trio_ libraries.

.. _badges:

.. image:: https://github.com/klen/aioauth-client/workflows/tests/badge.svg
    :target: https://github.com/klen/aioauth-client/actions
    :alt: Tests Status

.. image:: https://img.shields.io/pypi/v/aioauth-client
    :target: https://pypi.org/project/aioauth-client/
    :alt: PYPI Version

.. _contents:

.. contents::

.. _requirements:

Requirements
=============

- python >= 3.8

.. _installation:

Installation
=============

**AIOAuth Client** should be installed using pip: ::

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

    request_token, request_token_secret, _ = await twitter.get_request_token()

    authorize_url = twitter.get_authorize_url(request_token)
    print("Open",authorize_url,"in a browser")
    # ...
    # Reload client to authorize_url and get oauth_verifier
    # ...
    print("PIN code:")
    oauth_verifier = input()
    oauth_token, oauth_token_secret, _ = await twitter.get_access_token(oauth_verifier)

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

    timeline = await twitter.request('GET', 'statuses/home_timeline.json')
    content = await timeline.read()
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

    otoken, _ = await github.get_access_token(code)

    # Save the token for later use

    # ...

    github = GithubClient(
        client_id='b6281b6fe88fa4c313e6',
        client_secret='21ff23d9f1cad775daee6a38d230e1ee05b04f7c',
        access_token=otoken,
    )

    # Or you can use this if you have initilized client already
    # github.access_token = otoken

    response = await github.request('GET', 'user')
    user_info = await response.json()


Example
-------

Run example with command: ::

    make example

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

Development of AIOAuth Client happens at: https://github.com/klen/aioauth-client

.. _license:

License
========

Licensed under a `MIT license`_.

.. _links:

.. _klen: https://github.com/klen
.. _Asyncio: https://docs.python.org/3/library/asyncio.html
.. _Trio: https://trio.readthedocs.io/en/stable/

.. _MIT license: http://opensource.org/licenses/MIT
