import asyncio
from typing import List, Optional, Union, Dict

from . import create_artist_objects, create_tab_objects, InvalidToken, LoginFailed
from .models import Artist as w_Artist, \
    Comment as w_Comment, Media as w_Media, Notification as w_Notification, Photo as w_Photo, Post as w_Post, \
    Tab as w_Tab, Community as w_Community, Video as w_Video, Announcement as w_Announcement

from base64 import b64decode, b64encode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class WeverseClient:
    """
    Abstract & Parent Client for connecting to Weverse and creating the internal cache.

    Do not create an object directly from this class.
    Instead, create a :class:`Weverse.WeverseClientSync` or :class:`Weverse.WeverseClientAsync`
    object since those are concrete.

    Parameters
    ----------
    verbose: bool
        Whether to print out verbose messages.
    web_session:
        An aiohttp or requests client session.
    authorization: :class:`str`
        The account token to connect to the Weverse API. In order to find your token,
        please refer to :ref:`account_token`
    username: :class:`str`
        The email or username associated with the account.
    password: :class:`str`
        The password associated with the account.
    hook:
        A passed in method that will be called every time there is a new notification.
        This method must take in a list of :class:`models.Notification` objects.

    Attributes
    -----------
    verbose: bool
        Whether to print out verbose messages.
    web_session:
        An aiohttp or requests client session.
    user_notifications: list
        Most recent notifications of the account connected.
    cache_loaded: bool
        Whether the Internal Weverse Cache is fully loaded.
        This will change for a split moment when grabbing a new post.
    user_endpoint: str
        User info endpoint.
    all_posts: dict(Post)
        All posts in cache where the Post ID is the key and the value is the Post Object
    all_artists: dict(Artist)
        All artists in cache where the Artist ID is the key and the value is the Artist Object
    all_comments: dict(Comment)
        All comments in cache where the Comment ID is the key and the value is the Comment Object
    all_notifications: dict(Notification)
        All notifications in cache where the Notification ID is the key and the value is the Notification Object
    all_photos: dict(Photo)
        All photos in cache where the Photo ID is the key and the value is the Photo Object
    all_communities: dict(Community)
        All communities in cache where the Community ID is the key and the value is the Community Object
    all_media: dict(Media)
        All media in cache where the Media ID is the key and the value is the Media Object
    all_tabs: dict(Tab)
         All tabs in cache where the Tab ID is the key and the value is the Tab Object
    all_videos: dict(Video)
        All videos in cache where the Video URL is the key and the value is the Video Object
    all_announcements: dict(Announcement)
        All announcements/notices in cache where the Announcement ID is the key and the value is the Announcement Object
   """
    def __init__(self, **kwargs):
        self.verbose = kwargs.get('verbose')
        self.web_session = kwargs.get('web_session')
        self.__token = kwargs.get('authorization')
        self.user_notifications = []

        self._old_notifications = []
        self._headers = self.__get_headers()

        self.__login_payload = {
            "grant_type": "password",
            "client_id": "weverse-test",
            "username": kwargs.get("username"),
            "password": self.__get_encrypted_password(kwargs.get("password"))
        }

        self._refresh_payload = {
            "grant_type": "refresh_token",
            "client_id": "weverse-test",
            "refresh_token": None
        }

        self._login_url = "https://accountapi.weverse.io/api/v1/oauth/token"
        self._api_url = "https://weversewebapi.weverse.io/wapi/v1/"
        self._api_communities_url = self._api_url + "communities/"  # endpoint for communities
        self._api_notifications_url = self._api_url + "stream/notifications/"  # endpoint for user notifications
        # endpoint for checking new user notifications
        self._api_new_notifications_url = self._api_notifications_url + "has-new/"
        self._api_all_artist_posts_url = "posts/artistTab/"  # Artist Feed from a community
        self._api_stream_url = self._api_url + "/stream/community/"  # followed by community id and mediaTab.
        self._api_media_tab = "mediaTab/categorical?countByCategory=100000"
        self._api_artist_to_fans = "posts/tofans/"
        # endpoint for information about ALL communities and ALL idols.
        self._api_all_communities_info_url = self._api_communities_url + "info/"
        self.cache_loaded = False
        self._user_endpoint = "https://weversewebapi.weverse.io/wapi/v1/users/me"

        self.all_posts: Dict[int, w_Post] = {}
        self.all_artists: Dict[int, w_Artist] = {}
        self.all_comments: Dict[int, w_Comment] = {}
        self.all_notifications: Dict[int, w_Notification] = {}
        self.all_photos: Dict[int, w_Photo] = {}
        self.all_communities: Dict[int, w_Community] = {}
        self.all_media: Dict[int, w_Media] = {}
        self.all_tabs: Dict[int, w_Tab] = {}
        # Videos have the url as the key due to no unique ID.
        self.all_videos: Dict[str, w_Video] = {}
        self.all_announcements: Dict[int, w_Announcement] = {}

        self._hook = kwargs.get("hook")
        self._hook_loop = False
        self._expired_token = False
        self.__exception_to_raise = None

    @property
    def _login_info_exists(self) -> bool:
        """Whether login info is present."""
        return self.__login_payload["username"] and self.__login_payload["password"]

    @property
    def _token_exists(self) -> bool:
        """Whether a token is present."""
        return bool(self.__token)

    @property
    def _refresh_token_exists(self) -> bool:
        """Whether a refresh token is present."""
        return bool(self._refresh_payload["refresh_token"])

    @property
    def public_weverse_key(self) -> str:
        """Hard-coded weverse key"""
        return "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu/OhimOynajYomJmBsNvQxSDwekunsp986l7s/zMN/8jHXFlTqT79ZOsOwzVdZcKnkWYXwJg4nhIFpaIsPzklQCImp2kfKUJQV3jzw7/Qtq6NrOOh9YBADr+b99SHYcc7E7cDHjGXgWlC5jEI9h80R822wBU0HcbODkAQ3uosvFhSq3gLpxwdimesZofkJ5ZbAmGIMj1GEWAfMGA49mxkv/cDFWry+6FM4mUW6A0301QUg4wK/8n6RrzRj1NUkevZj1smizHeqmBE+0BU5H/fR9HclErx3LMHlVlxSgEEEjNUx3B0bLO0OHppmEb4B3Tk1O3ZsquYyqZyb2lBTbrQwIDAQAB"

    def stop(self):
        """Stop the hook loop."""
        self._hook_loop = False

    def _login(self, method):
        """
        Requests a login.
        Will not return response.
        The method should handle the response itself.
        Parameters
        ----------
        method:
            The async/sync method to call. Should be able to take in the login payload.
        """
        if not asyncio.iscoroutinefunction(method):
            method(self.__login_payload)
        else:
            asyncio.create_task(method(self.__login_payload))

    def _set_exception(self, exception: Exception):
        """
        Set an exception from a task that occurred.
        Parameters
        ----------
        exception: The Exception that was raised.
        """
        self.__exception_to_raise = exception

    async def _wait_for_login(self, timeout=15):
        """
        Will wait until the client is logged in or the timeout timer is exceed.
        Parameters
        ----------
        timeout: int
            Amount of seconds before an exception is raised.
        :raises: :class:`Weverse.error.LoginFailed` Login process had failed.
        :raises: :class:`asyncio.exceptions.TimeoutError` Waited too long for a login.
        """
        seconds_passed = 0
        while not self._refresh_token_exists or self._expired_token:
            if self.__exception_to_raise:
                if isinstance(self.__exception_to_raise, (LoginFailed, asyncio.exceptions.TimeoutError)):
                    exception = self.__exception_to_raise
                    self.__exception_to_raise = None
                    # if an exception was raised from here, the actual exception occurred in a task.
                    raise exception
            await asyncio.sleep(1)
            seconds_passed += 1

            if seconds_passed > timeout:
                self._set_exception(asyncio.exceptions.TimeoutError())

    def get_new_notifications(self) -> List[w_Notification]:
        """Will get the new notifications from the last notification check.

        Should only be used after :ref:`check_new_user_notifications` OR :ref:`update_cache_from_notification`.

        :returns: List[:ref:`Notification`]
        """
        return [noti for noti in self.user_notifications if noti not in self._old_notifications]

    def check_status(self, status, url) -> bool:
        """
        Confirm the status of a URL

        :param status: Status code of url connection
        :param url: Link that we connected to.
        :return: True if the connection was a success.
        :raises: :ref:`invalid_token_exc` if there was an invalid token.
        """
        if status == 200:
            return True
        elif status == 401:
            self._expired_token = True
            # raise InvalidToken
        elif status == 404:
            if self.verbose:
                # raise error.PageNotFound
                print("WARNING (NOT CRITICAL): " + url + " was not found.")
        else:
            if self.verbose:
                print("WARNING (NOT CRITICAL): " + url + " Failed to load. [Status: " + str(status) + "]")

    @staticmethod
    def process_community_artists_and_tabs(community, response_text_as_dict):
        """
        Process the community artists and tabs and add them to their respective communities.

        :param community: Community object
        :param response_text_as_dict: Response text of connection to endpoint but as a dict.
        """
        # split up response dict by artists and tabs
        community_artists = response_text_as_dict.get('artists')
        community_tabs = response_text_as_dict.get('tabs')

        # create artist and tab objects under the community
        community.artists = create_artist_objects(community_artists)
        community.tabs = create_tab_objects(community_tabs)

        # set the community for each artist
        for artist in community.artists:
            artist.community = community

    def get_artist_by_id(self, artist_id) -> Optional[w_Artist]:
        """
        Get artist by their ID.

        :param artist_id: The artist's ID
        :returns: Optional[:ref:`Artist`]
        """
        artist = self.all_artists.get(artist_id)
        if not artist:
            for t_artist in self.all_artists.values():
                if t_artist.community_user_id == artist_id:
                    artist = t_artist
        return artist

    def get_tab_by_id(self, tab_id) -> Optional[w_Tab]:
        """
        Get tab by their ID.

        :param tab_id: The tab ID
        :returns: Optional[:ref:`Tab`]
        """
        return self.all_tabs.get(tab_id)

    def get_post_by_id(self, post_id) -> Optional[w_Post]:
        """
        Get a post by the ID

        :param post_id: Post ID
        :returns: Optional[:ref:`Post`]
        """
        return self.all_posts.get(post_id)

    def get_comment_by_id(self, comment_id) -> Optional[w_Comment]:
        """
        Get a comment by the ID
        :param comment_id: Comment ID
        :returns: Optional[:ref:`Comment`]
        """
        return self.all_comments.get(comment_id)

    def get_notification_by_id(self, notification_id) -> Optional[w_Notification]:
        """
        Get a notification by the ID

        :param notification_id: Notification ID
        :returns: Optional[:ref:`Notification`]
        """
        return self.all_notifications.get(notification_id)

    def get_photo_by_id(self, photo_id) -> Optional[w_Photo]:
        """
        Get a photo by the ID

        :param photo_id: Photo ID
        :returns: Optional[:ref:`Photo`]
        """
        return self.all_photos.get(photo_id)

    def get_video_by_url(self, video_url) -> Optional[w_Video]:
        """
        Get a video by the direct URL.

        :param video_url: URL of the video
        :return: Optional[:ref:`Video`]
        """
        return self.all_videos.get(video_url)

    def get_community_by_id(self, community_id) -> Optional[w_Community]:
        """
        Get a community by the ID.

        :param community_id: Community ID
        :returns: Optional[:ref:`Community`]
        """
        return self.all_communities.get(community_id)

    def get_media_by_id(self, media_id) -> Optional[w_Media]:
        """
        Get Media by the ID

        :param media_id: Media ID
        :returns: Optional[:ref:`Media`]
        """
        return self.all_media.get(media_id)

    def get_announcement_by_id(self, announcement_id) -> Optional[w_Announcement]:
        """
        Get Announcement by the ID

        :param announcement_id: Media ID
        :returns: Optional[:ref:`Announcement`]
        """
        return self.all_announcements.get(announcement_id)

    def _add_media_to_cache(self, media_objects: List[w_Media]):
        """
        Will add media objects and it's photos to cache.

        :param media_objects:
        """
        for media in media_objects:
            self.all_media[media.id] = media
            if media.photos:
                for photo in media.photos:
                    self.all_photos[photo.id] = photo

    def __get_encrypted_password(self, password):
        """
        Get the encrypted password from Weverse's public key.

        :param password: The password to encrypt with Weverse's public key.
        :return: Encrypted password.
        """
        if not password:
            return

        key_der = b64decode(self.public_weverse_key)
        pub_key = RSA.importKey(key_der)
        cipher = PKCS1_OAEP.new(pub_key)
        cipher_text = cipher.encrypt(password.encode())
        encrypted_pass = b64encode(cipher_text)
        password = encrypted_pass.decode("utf-8")
        return password

    def _set_token(self, token):
        """
        Set the token used for endpoints.
        Parameters
        ----------
        token: str
            New token used for endpoints
        """
        self.__token = token
        self._headers = self.__get_headers()  # update headers

    def __get_headers(self):
        return {'Authorization': f"Bearer {self.__token}"}

    def _set_refresh_token(self, refresh_token: str):
        """
        Set the refresh token.
        Parameters
        ----------
        refresh_token: str
            The refresh token to pass when logging in.
        """
        self._refresh_payload["refresh_token"] = refresh_token

    @staticmethod
    def determine_notification_type(notification: Union[w_Notification, str]) -> str:
        """
        Determine the post type based on the notification body or the Notification object itself.

        Since notifications do not differentiate between Posts and Comments, this is for that purpose.

        :param notification: The message body of the notification or the notification itself.
        :returns: A string with either
            "comment", "media", "post", or "announcement".
        """
        if isinstance(notification, w_Notification):
            notification_body = notification.message
        else:
            notification_body = notification

        comment_body_triggers = ["commented on", "replied to", "포스트에 댓글을 작성했습니다", "답글을 작성했습니다."]
        post_body_triggers = ["님이 포스트를 작성했습니다", "created a new post!", "shared a moment with you",
                              "모먼트가 도착했습니다"]
        media_triggers = ["Check out the new media", "새로운 미디어"]

        announcement_body_triggers = ["New announcement", "NOTICE:", "(광고)", "(AD)"]

        for trigger in comment_body_triggers:
            if trigger in notification_body:
                return "comment"

        for trigger in post_body_triggers:
            if trigger in notification_body:
                return "post"

        for trigger in media_triggers:
            if trigger in notification_body:
                return "media"

        for trigger in announcement_body_triggers:
            if trigger in notification_body:
                return "announcement"
