## Weverse

### What is it?
Weverse creates internal cache for the communities a user follows on [weverse.io](https://www.weverse.io/).

### Functionalities

* Asynchronous and Synchronous Support
* Receive all the posts the artists in your communities have made. This includes all images/videos/comments made by them.
* Cache is split under a hierarchy directly under a community. The most recent is always the first element (0th index).
* Keep track of notifications on your user account, you can easily create a loop to update your notification cache on updates. [**Example of real usage**](https://github.com/MujyKun/IreneBot/blob/9193fcd3b6c73f61c57fb2fad557921141b1c07a/module/Weverse.py#L65)

### Installation

In a terminal, type `pip install weverse`.  

To install from source:  
`pip install git+https://github.com/MujyKun/Weverse.git`


### How to Use

First off, your account token is needed (Will need to be updated about every 6 months iirc).  

In order to get your account token, go to [Weverse](https://www.weverse.io/) and Inspect Element (F12).  
Then go to the `Network` tab and filter by `XHR`. Then refresh your page (F5) and look for `info` or `me` under `XHR`.  
Under Headers, scroll to the bottom and view the request headers. You want to copy everything past `authorization: Bearer`.

For example, you may see (This is just an example):  
``authorization: Bearer ABCDEFGHIJKLMNOPQRSTUVWXYZ``  
Then ``ABCDEFGHIJKLMNOPQRSTUVWXYZ`` would be your auth token for Weverse. 
It is suggested to have the auth token as an environment variable.


#### CODE EXAMPLES

```python


# Asynchronous
import asyncio
import aiohttp
from Weverse.error import InvalidToken
from Weverse.weverseasync import WeverseClientAsync

token = "fake_token"  # REQUIRED
# It is advised to pass in your own web session as it is not closed in Weverse 
web_session = aiohttp.ClientSession()  # A session is created by default 
weverse_client = WeverseClientAsync(authorization=token, verbose=True, loop=asyncio.get_event_loop(),
                                    web_session=web_session)
try:
    await weverse_client.start()  # creates all the cache needed for your account.
except InvalidToken:
    print("Invalid Token")

# Synchronous
import requests
from Weverse.weversesync import WeverseClientSync
from Weverse.error import InvalidToken

token = "fake_token"  # REQUIRED
# It is advised to pass in your own web session as it is not closed in Weverse
web_session = requests.Session()  # A session is created by default 
weverse_client = WeverseClientSync(authorization=token, verbose=True)
try:
    weverse_client.start()  # creates all the cache needed for your account.
except InvalidToken:
    print("Invalid Token")

# After calling the start method, you now have all the objects you would want to modify.

```

## **[API Documentation](https://weverse.readthedocs.io/en/latest/)**