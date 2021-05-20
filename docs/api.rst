.. _weverse_main:

Weverse
=======

.. autoclass:: weverse.Weverse
    :members:

.. _clients_main:

Clients
========

===========
WeverseSync
===========
.. autoclass:: weversesync.WeverseSync
    :members:

============
WeverseAsync
============
.. autoclass:: weverseasync.WeverseAsync
    :members:

.. _obj_types:

Models
======

=========
Community
=========
.. autoclass:: community.Community
    :members:

============
Notification
============
.. autoclass:: notification.Notification
    :members:

=========
Photo
=========
.. autoclass:: photo.Photo
    :members:

=========
Artist
=========
.. autoclass:: artist.Artist
    :members:

=========
Comment
=========
.. autoclass:: comment.Comment
    :members:

=========
Post
=========
.. autoclass:: post.Post
    :members:

=========
Tab
=========
.. autoclass:: tab.Tab
    :members:

=========
Media
=========
.. autoclass:: media.Media
    :members:

.. _obj_creation:

Model Creation
===============
.. automodule:: objects
    :members:

.. _obj_exception:

Exceptions
==========

.. _invalid_token_exc:

=============
Invalid Token
=============
.. autoexception:: error.InvalidToken
    :members:

==============
Page Not Found
==============
.. autoexception:: error.PageNotFound
    :members:

==================
Being Rate Limited
==================
.. autoexception:: error.BeingRateLimited
    :members:


.. _account_token:

Get Account Token
=================
Your account token is needed (Will need to be updated about every 6 months iirc).

In order to get your account token, go to https://www.weverse.io/ and Inspect Element (F12).

Then go to the `Network` tab and filter by `XHR`.

Then refresh your page (F5) and look for `info` or `me` under `XHR`.

Under Headers, scroll to the bottom and view the request headers.

You want to copy everything past `authorization: Bearer`.

For example, you may see (This is just an example):

``authorization: Bearer ABCDEFGHIJKLMNOPQRSTUVWXYZ``

Then ``ABCDEFGHIJKLMNOPQRSTUVWXYZ`` would be your auth token for Weverse.

It is suggested to have the auth token as an environment variable.


Asynchronous Usage
==================

.. code-block:: python

    # Asynchronous
    import asyncio
    import aiohttp
    from Weverse.error import InvalidToken
    from Weverse.weverseasync import WeverseAsync

    token = "fake_token"  # REQUIRED
    # It is advised to pass in your own web session as it is not closed in Weverse
    web_session = aiohttp.ClientSession()
    weverse_client = WeverseAsync(authorization=token, verbose=True, loop=asyncio.get_event_loop(), web_session=web_session)
    try:
        await weverse_client.start()  # creates all the cache needed for your account.
    except InvalidToken:
        print("Invalid Token")

Synchronous Usage
=================

.. code-block:: python

    # Synchronous
    import requests
    from Weverse.weversesync import WeverseSync
    from Weverse.error import InvalidToken

    token = "fake_token"  # REQUIRED
    # It is advised to pass in your own web session as it is not closed in Weverse
    web_session = requests.Session()  # A session is created by default
    weverse_client = WeverseSync(authorization=token, verbose=True)
    try:
        weverse_client.start()  # creates all the cache needed for your account.
    except InvalidToken:
        print("Invalid Token")