## Weverse

### What is it?
Weverse creates internal cache for the communities a user follows on [weverse.io](https://www.weverse.io/).

### Functionalities

* Asynchronous and Synchronous Support
* Receive all the posts the artists in your communities have made. This includes all images/videos/comments made by them.
* Cache is split under a hierarchy directly under a community. The most recent is always the first index.
* Keep track of notifications on your user account, you can easily create a loop to update your notification cache on updates.

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
from Weverse.weverseasync import WeverseAsync

token = "fake_token"  # REQUIRED
# It is advised to pass in your own web session as it is not closed in Weverse 
web_session = aiohttp.ClientSession()  # A session is created by default 
weverse_client = WeverseAsync(authorization=token, verbose=True, loop=asyncio.get_event_loop(), web_session=web_session)
try:
    await weverse_client.start()  # creates all the cache needed for your account.
except InvalidToken:
    print("Invalid Token")

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

"""
After using the start method, you now have all the objects you would want to modify.
I'm too lazy to make an official docs page, so I will just list the IMPORTANT Classes, Objects, and their properties/methods below.
"""

```


# Classes/Objects

### Weverse  [Weverse.weverse.Weverse | Weverse.weverseasync.WeverseAsync | Weverse.weversesync.WeverseSync]

```
Parent Class of WeverseAsync and WeverseSync
Weverse is the client that contains all information and can be branched down to find more specific information.

Properties:
-----------------------------------------
communities: list -> list of communities (object) the user is in
-----------------------------------------
user_notifications: list -> list of notifications (object) the user has.
-----------------------------------------
cache_loaded: boolean ->  A check to see if the Weverse cache is loaded.
-----------------------------------------
new_media: list -> list of medias (object) that were created from new notifications. 
Note that not ALL media is stored as cache, so this is useful on new notifications.
-----------------------------------------


Sub-Class Methods:

The methods in WeverseAsync and WeverseSync are the same, but the methods in WeverseAsync MUST BE AWAITED. 
Writing it only once on Parent Class.

-----------------------------------------
start() -> Creates Internal Cache [Main Process that should be run]. Can also be used to update cache if a lot has changed. 
-----------------------------------------
create_communities() -> Creates the general cache for the user's communities.
-----------------------------------------
create_community_artists_and_tabs() -> Creates the artist and tab objects of a community.
-----------------------------------------
create_posts(community: Community, next_page_id: int = None) -> Pass in a Community object, no need to pass in a page id.
The purpose of the page id is to paginate all posts when scrolling down the page. By default, recursion is used to create the posts.
-----------------------------------------
create_post(community: Community, post_id) -> Create an individual post and update the cache with it.
-----------------------------------------
get_user_notifications() -> Creates/Updates the cache for the user's notifications. 
-----------------------------------------
check_new_user_notifications() -> Checks if the user has a new notification. 
If it returns True, it is suggested to update the notification cache with get_user_notifications()
-----------------------------------------
translate(post_or_comment_id, post=False, comment=False) -> Translates the body of a post or comment.
Send in the post or comment id, then set if it is a post or comment to True. Returns translated text.
-----------------------------------------
fetch_artist_comments(comunity_id, post_id) -> Fetches the UPDATED artist comments on a post.
-----------------------------------------
fetch_media(community_id, media_id) -> receives a media object based on the media id
-----------------------------------------
update_cache_from_notification() -> Called by default after a new notification is found to update cache.
-----------------------------------------


Parent-Class Methods:
-----------------------------------------
get_artist_by_id(artist_id) -> get an artist object by their id (community or user id)
-----------------------------------------
get_post_by_id(post_id) -> get a post object by the id
-----------------------------------------
get_comment_by_id(comment_id) -> get a comment object by the id
-----------------------------------------
get_notification_by_id(notification_id) -> get a notification object by the id
-----------------------------------------
get_photo_by_id(photo_id) -> get a photo object by the id
-----------------------------------------
get_community_by_id(community_id) -> get a community by the id
-----------------------------------------
process_community_artists_and_tabs(community, dict response from a connection) -> Processes community artists and tabs and adds them to their communities (should not be used unless making API calls yourself).
-----------------------------------------
determine_notification_type(notification_body) -> Returns string that says one of the following:
comment, post, or media.
-----------------------------------------

```

### Community [Class Weverse.community.Community]
```
A community is at the center of all the group information provided with exception to the Weverse Client of course. [Not User Specific]

Properties:
-----------------------------------------
id: int -> Community ID  
-----------------------------------------
name: str -> Community Name  
-----------------------------------------
description: str -> Description of Community  
-----------------------------------------
member_count: int -> Members in community  
-----------------------------------------
home_banner: str -> Link to home banner  
-----------------------------------------
icon: str -> Link to community logo  
-----------------------------------------
banner: str -> Link to community banner  
-----------------------------------------
full_name: list -> List of names for the community  
-----------------------------------------
fc_member: bool -> I think this is if the user has to be a fanclub member to join, not sure.  
-----------------------------------------
show_member_count: bool -> Whether the community shows the member count   
-----------------------------------------
artists: list -> list of Artist objects  
-----------------------------------------
tabs: list -> list of available Tab objects  
-----------------------------------------
```
### Notification [Class Weverse.notification.Notification]
```
Contains information about the notification the user received.

Properties:
-----------------------------------------
id: int -> Notification ID
-----------------------------------------
artist_id: int -> Artist ID
-----------------------------------------
bold_element: str -> The highlighted topic in your notification. Ex: SUNMI
-----------------------------------------
community_id: int -> Community ID
-----------------------------------------
community_name: str -> Community Name
-----------------------------------------
contents_id: int -> The Post ID
-----------------------------------------
contents_type: str -> The type of post it is Ex: ARTIST_POST
-----------------------------------------
icon_image_url: str -> Image on the notification
-----------------------------------------
is_membership_content: bool -> Only accessible by those with a membership
-----------------------------------------
is_web_only: bool -> Only accessible on the web
-----------------------------------------
message: str -> Contains notification message Ex: SUNMI created a new post!
-----------------------------------------
notified_at: str -> When the user was notified. YYYY-MM-DDTHH:MM:SS+09:00
-----------------------------------------
platform: str -> What platform the post is available on Ex: "ALL"
-----------------------------------------
thumbnail_image_url: str -> Thumbnail on the notification.
-----------------------------------------
```

### Artist [Class Weverse.artist.Artist]
```
An Artist is an official member in the Community

Properties
-----------------------------------------
birthday_img_url: str -> Image showing Happy Birthday <Insert Artist Name Here>
-----------------------------------------
community: Community -> Community the artist is in
-----------------------------------------
community_id: int -> ID of the Community
-----------------------------------------
community_user_id: int -> ID of the artist in the community
-----------------------------------------
group_name: str -> Basically the community name
-----------------------------------------
has_new_private_to_fans: bool -> Guessing this is meant for updates (Not used though in this package, since we have notifications) 
-----------------------------------------
has_new_to_fans: bool -> Also meant for updates (Not used though in this package, since we have notifications)
-----------------------------------------
id: int -> Artist ID
-----------------------------------------
is_birthday: bool -> If it is the artist's birthday
-----------------------------------------
is_enabled: bool -> If the account is enabled
-----------------------------------------
is_online: bool -> If the account is online
-----------------------------------------
list_name: list -> List of names for the artist
-----------------------------------------
max_comment_count: int -> Maximum amount of comments their account can have (typically 2.147 billion)
-----------------------------------------
name: str -> Artist's name
-----------------------------------------
posts: list -> List of Post objects the user has made. List index is organized from Newest to Oldest
-----------------------------------------
profile_img_path: str -> Image URL of their Profile Photo
-----------------------------------------
profile_nick_name: str -> Artist nick name.
-----------------------------------------
to_fan_last_created_at: str -> Probably a timestamp of when their last fan post was
-----------------------------------------
to_fan_last_expire_in: int -> Probably when their last fan post expires
-----------------------------------------
to_fan_last_id: int -> Artist's last fan post id
-----------------------------------------
```

### Post [Class Weverse.post.Post]
```
A post created by an artist.

Properties:
-----------------------------------------
artist: Artist -> The Artist object that made the post.
-----------------------------------------
artist_comments: list -> List of Comment Objects that the artist has made on the post
-----------------------------------------
artist_id: int -> Artist ID
-----------------------------------------
body: str -> Post Message
-----------------------------------------
comment_count: int -> Amount of comments on the post
-----------------------------------------
community_artist_id: int -> Artist's Community ID
-----------------------------------------
community_tab_id: int -> The tab the post was made in.
-----------------------------------------
created_at: str -> When the post was made YYYY-MM-DDTHH:MM:SS+09:00
-----------------------------------------
has_my_bookmark: bool -> Whether the post is user bookmarked
-----------------------------------------
has_my_like: bool -> Whether the user liked the post.
-----------------------------------------
id: int -> Post ID
-----------------------------------------
is_active: bool -> If the post is active
-----------------------------------------
is_blind: bool -> I'm guessing this is like a spoiler mode??
-----------------------------------------
is_hot_trending_post: bool -> Whether the post is trending
-----------------------------------------
is_limit_comment: bool -> If the comments are limited
-----------------------------------------
is_locked: bool ->  If the post is locked
-----------------------------------------
is_private: bool -> If the post is private
-----------------------------------------
like_count: int ->  Amount of likes on the post
-----------------------------------------
max_comment-count: int -> Max amount of comments a post can have (Usually 2.147 bill)
-----------------------------------------
photos: list -> A list of Photo objects from the post.
-----------------------------------------
type: str -> The type of post ex: Normal
-----------------------------------------
updated_at: str -> When the post was updated YYYY-MM-DDTHH:MM:SS+09:00
-----------------------------------------
```

### Photo [Class Weverse.photo.Photo]
```
Contains all the information about a photo.

Properties:
-----------------------------------------
content_index: int -> The index in which the photo is placed (starts from 0)
-----------------------------------------
file_name: str -> Has the file's name
-----------------------------------------
id: int -> Photo ID
-----------------------------------------
original_img_height: int -> Original Image Height
-----------------------------------------
original_img_url: str -> Original Image URL
-----------------------------------------
original_img_width: int -> Original Image Width
-----------------------------------------
post: Post -> Contains the Post object the photo belongs to
-----------------------------------------
thumbnail_img_height: int -> Height of thumbnail
-----------------------------------------
thumbnail_img_url: str -> URL of thumbnail
-----------------------------------------
thumbnail_img_width: int -> Width of thumbnail
-----------------------------------------
```

### Comment [Class Weverse.comment.Comment]
```
Contains all the information about a comment.

Properties:
-----------------------------------------
body: str -> Comment Message
-----------------------------------------
comment_count: int -> Comments on the Comment
-----------------------------------------
created_at: str -> When the comment was created YYYY-MM-DDTHH:MM:SS+09:00
-----------------------------------------
has_my_like: bool -> Whether it was like by the user 
-----------------------------------------
id: int -> ID of the comment
-----------------------------------------
is_blind: bool -> Spoiler???
-----------------------------------------
like_count: int -> Likes on the comment
-----------------------------------------
post: Post -> Post Object of the post the comment belongs to
-----------------------------------------
post_id: int -> ID of the post
-----------------------------------------
updated_at: str -> When the comment was updated YYYY-MM-DDTHH:MM:SS+09:00
-----------------------------------------
```

### Tab [Class Weverse.tab.Tab]
```
Contains Information about the community tabs. These tabs are meant for where a post was made
ex: Feed, Media, Artist

Properties:
-----------------------------------------
id: int -> ID of the tab
-----------------------------------------
name: str -> Name of the tab
-----------------------------------------
```

### Media [Class Weverse.media.Media]
```
Contains Media Information
Please Note that media information is not added to the internal cache. The media object is only given
when using the fetch_media method. 

Properties:
-----------------------------------------
id: int -> Media ID
-----------------------------------------
community_id: int -> Community ID
-----------------------------------------
body: str -> Media Body
-----------------------------------------
type: str -> Media Type
-----------------------------------------
thumbnail_path: str -> URL Thumbnail of media
-----------------------------------------
title: str -> Title of Media
-----------------------------------------
level: str -> Community Level to access post
-----------------------------------------
video_link: str -> External Link to video
-----------------------------------------
youtube_id: str -> Youtube ID of viedo
-----------------------------------------
```



### objects (This is the file name, not in a class) [File Weverse.objects]
```
Creating Objects and sorting them properly as cache.
This means tracebacks on the branching is done as well.
For each method, a list of dicts DIRECTLY from the weverse.io API must be used. 
In return it will create the objects and the connections needed between the objects.

Methods:
-----------------------------------------
create_community_objects(current_communities)
-----------------------------------------
create_artist_objects(current_artists)
-----------------------------------------
create_tab_objects(current_tabs)
-----------------------------------------
create_notification_objects(current_notifications)
-----------------------------------------
create_post_objects(current_posts, Community)
-----------------------------------------
create_to_fan_post(post_info: dict)
-----------------------------------------
create_photo_objects(current_photos)
-----------------------------------------
create_comment_objects(current_comments)
-----------------------------------------
create_media_object(media_info: dict)
-----------------------------------------
```
