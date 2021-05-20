.. _weverse_main:

Weverse
=======

.. autoclass:: Weverse.Weverse
    :members:

.. _clients_main:

Clients
========

===========
WeverseSync
===========
.. autoclass:: Weverse.WeverseSync
    :members:

============
WeverseAsync
============
.. autoclass:: Weverse.WeverseAsync
    :members:

.. _obj_types:

Models
======

=========
Community
=========
.. autoclass:: Weverse.Community
    :members:

============
Notification
============
.. autoclass:: Weverse.Notification
    :members:

=========
Photo
=========
.. autoclass:: Weverse.Photo
    :members:

=========
Artist
=========
.. autoclass:: Weverse.Artist
    :members:

=========
Comment
=========
.. autoclass:: Weverse.Comment
    :members:

=========
Post
=========
.. autoclass:: Weverse.Post
    :members:

=========
Tab
=========
.. autoclass:: Weverse.Tab
    :members:

=========
Media
=========
.. autoclass:: Weverse.Media
    :members:

.. _obj_creation:

Model Creation
===============
.. automodule:: Weverse.objects
    :members:

.. _obj_exception:

Exceptions
==========

.. _invalid_token_exc:

=============
Invalid Token
=============
.. autoexception:: Weverse.InvalidToken
    :members:

==============
Page Not Found
==============
.. autoexception:: Weverse.PageNotFound
    :members:

==================
Being Rate Limited
==================
.. autoexception:: Weverse.BeingRateLimited
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