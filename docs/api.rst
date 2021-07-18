.. py:currentmodule:: Weverse

.. _weverse_main:

WeverseClient
=============

.. autoclass:: Weverse.WeverseClient
    :members:

.. _clients_main:

Clients
========

===========
WeverseClientSync
===========
.. autoclass:: Weverse.WeverseClientSync
    :members:

============
WeverseClientAsync
============
.. autoclass:: Weverse.WeverseClientAsync
    :members:

.. _obj_types:

Models
======

=========
Community
=========
.. autoclass:: Weverse.models.Community
    :members:

============
Notification
============
.. autoclass:: Weverse.models.Notification
    :members:

=========
Photo
=========
.. autoclass:: Weverse.models.Photo
    :members:

=========
Video
=========
.. autoclass:: Weverse.models.Video
    :members:

=========
Artist
=========
.. autoclass:: Weverse.models.Artist
    :members:

=========
Comment
=========
.. autoclass:: Weverse.models.Comment
    :members:

=========
Post
=========
.. autoclass:: Weverse.models.Post
    :members:

=========
Tab
=========
.. autoclass:: Weverse.models.Tab
    :members:

=========
Media
=========
.. autoclass:: Weverse.models.Media
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

IMPORTANT NOTE: Not all korean key-phrases may be logged. Scroll to the bottom of the Weverse page when you are logged in
and click "English" to set the account language to English.


Asynchronous Usage
==================

.. code-block:: python

    # Asynchronous
    import asyncio
    import aiohttp
    from Weverse.error import InvalidToken
    from Weverse.weverseasync import WeverseClientAsync

    # THERE IS A MORE DETAILED EXAMPLE IN THE EXAMPLES FOLDER
    # https://github.com/MujyKun/Weverse/blob/main/examples/asynchronous.py

    token = "fake_token"  # REQUIRED
    # It is advised to pass in your own web session as it is not closed in Weverse
    web_session = aiohttp.ClientSession()
    weverse_client = WeverseClientAsync(authorization=token, verbose=True, loop=asyncio.get_event_loop(), web_session=web_session)
    try:
        await weverse_client.start()  # creates all the cache needed for your account.
    except InvalidToken:
        print("Invalid Token")

Synchronous Usage
=================

.. code-block:: python

    # Synchronous
    import requests
    from Weverse.weversesync import WeverseClientSync
    from Weverse.error import InvalidToken

    # THERE IS A MORE DETAILED EXAMPLE IN THE EXAMPLES FOLDER
    # https://github.com/MujyKun/Weverse/blob/main/examples/synchronous.py

    token = "fake_token"  # REQUIRED
    # It is advised to pass in your own web session as it is not closed in Weverse
    web_session = requests.Session()  # A session is created by default
    weverse_client = WeverseClientSync(authorization=token, verbose=True)
    try:
        weverse_client.start()  # creates all the cache needed for your account.
    except InvalidToken:
        print("Invalid Token")