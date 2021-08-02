## Weverse

### What is it?
Weverse creates internal cache for the communities a user follows on [weverse.io](https://www.weverse.io/).  
This is a **wrapper** for Weverse's private API, but may be referred to as an API on this repository.



### **[API Documentation](https://weverse.readthedocs.io/en/latest/)**

### **[Discord Support Server](https://discord.gg/bEXm85V)**

**[A WEVERSE DISCORD BOT CAN BE FOUND HERE](https://github.com/MujyKun/WeverseBot)**  


### Functionalities

* Asynchronous and Synchronous Support
* Receive all the posts the artists in your communities have made. This includes all images/videos/comments made by them.
* Cache is split under a hierarchy directly under a community.  
* Keep track of notifications on your user account, you can easily create a loop to update your notification cache on updates. (Usage of this can be found in the examples folder)

### Installation

In a terminal, type `pip install weverse`.  

To install from source:  
`pip install git+https://github.com/MujyKun/Weverse.git`


### How to Use

First off, your account token is needed (Will need to be updated about every 6 months iirc).  
Note that it is now possible to log-in using a username and password without a token. This will prevent manual updates.


In order to get your account token, go to [Weverse](https://www.weverse.io/) and Inspect Element (F12).  
Then go to the `Network` tab and filter by `XHR`. Then refresh your page (F5) and look for `info` or `me` under `XHR`.  
Under Headers, scroll to the bottom and view the request headers. You want to copy everything past `authorization: Bearer`.

For example, you may see (This is just an example):  
``authorization: Bearer ABCDEFGHIJKLMNOPQRSTUVWXYZ``  
Then ``ABCDEFGHIJKLMNOPQRSTUVWXYZ`` would be your auth token for Weverse. 
It is suggested to have the auth token as an environment variable.

IMPORTANT NOTE: Not all korean key-phrases may be kept track of. Scroll to the bottom of the Weverse page  
when you are logged in and click "English" to set the account language to English.  

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
# THE EXAMPLE IN THE EXAMPLES FOLDER WILL SHOW YOU HOW TO LOGIN WITH A USERNAME AND PASSWORD AND SET UP HOOKS.

# It is advised to pass in your own web session as it is not closed in Weverse 
web_session = aiohttp.ClientSession()  # A session is created by default 
weverse_client = WeverseClientAsync(authorization=token, verbose=True, loop=asyncio.get_event_loop(),
                                    web_session=web_session)
try:
    # creates all the cache that is specified. If the create parameters are set to True, they will take a very long time.  
    await weverse_client.start(create_old_posts=True, create_media=True)
except InvalidToken:
    print("Invalid Token")

# Synchronous
import requests
from Weverse.weversesync import WeverseClientSync
from Weverse.error import InvalidToken


# THERE IS A MORE DETAILED EXAMPLE IN THE EXAMPLES FOLDER
# https://github.com/MujyKun/Weverse/blob/main/examples/synchronous.py

token = "fake_token"  # REQUIRED
# THE EXAMPLE IN THE EXAMPLES FOLDER WILL SHOW YOU HOW TO LOGIN WITH A USERNAME AND PASSWORD AND SET UP HOOKS.

# It is advised to pass in your own web session as it is not closed in Weverse
web_session = requests.Session()  # A session is created by default 
weverse_client = WeverseClientSync(authorization=token, verbose=True)
try:
    # creates all the cache that is specified. If the create parameters are set to True, they will take a very long time.  
    weverse_client.start(create_old_posts=True, create_media=True) 
except InvalidToken:
    print("Invalid Token")

# After calling the start method, you now have all the objects you would want to modify.
# The start method takes in parameters that can disable old posts from loading up 
# if only the newer posts are wanted. More info on the documentation.

```
**[More Detailed Asynchronous Example](https://github.com/MujyKun/Weverse/blob/main/examples/asynchronous.py)**  
**[More Detailed Synchronous Example](https://github.com/MujyKun/Weverse/blob/main/examples/synchronous.py)**

### **[API Documentation](https://weverse.readthedocs.io/en/latest/)**
