## Weverse

### What is it?
Weverse creates internal cache for the communities a user follows on [weverse.io](https://www.weverse.io/).  
This is a **wrapper** for Weverse's private API, but will be referred to as an API on this repository.

### **[API Documentation](https://weverse.readthedocs.io/en/latest/)**

### Functionalities

* Asynchronous and Synchronous Support
* Receive all the posts the artists in your communities have made. This includes all images/videos/comments made by them.
* Cache is split under a hierarchy directly under a community. The most recent is always the first element (0th index).
* Keep track of notifications on your user account, you can easily create a loop to update your notification cache on updates. [**Example of real usage**](https://github.com/MujyKun/IreneBot/blob/5ed92595314e146d0f4a7a3f04461afd168d327f/module/Weverse.py#L80)

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

# THERE IS A MORE DETAILED EXAMPLE IN THE EXAMPLES FOLDER
# https://github.com/MujyKun/Weverse/blob/main/examples/asynchronous.py

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

# After calling the start method, you now have all the objects you would want to modify.
# The start method takes in parameters that can disable old posts from loading up 
# if only the newer posts are wanted. More info on the documentation.

```
**[More Detailed Asynchronous Example](https://github.com/MujyKun/Weverse/blob/main/examples/asynchronous.py)**  
**[More Detailed Synchronous Example](https://github.com/MujyKun/Weverse/blob/main/examples/synchronous.py)**

### **[API Documentation](https://weverse.readthedocs.io/en/latest/)**
