import asyncio
from typing import Optional, List, Union

import aiohttp
from asyncio import get_event_loop
from .models import Community, Post as w_Post, Notification, Announcement, Media
from . import WeverseClient, create_post_objects, create_community_objects, create_notification_objects, \
    create_comment_objects, create_media_object, iterate_community_media_categories, create_announcement_object, \
    InvalidCredentials, LoginFailed, InvalidToken, NoHookFound, check_expired_token
from json import dumps as dumps_


class WeverseClientAsync(WeverseClient):
    r"""
    Asynchronous Weverse Client that Inherits from :ref:`WeverseClient`.

    Parameters
    ----------
    loop:
        Asyncio Event Loop
    kwargs:
        Same as :ref:`WeverseClient`.


    Attributes
    -----------
    loop:
        Asyncio Event Loop

    Attributes are the same as :ref:`WeverseClient`.
    """

    def __init__(self, loop=get_event_loop(), **kwargs):
        self._follow_new_communities = True
        self._time_passed: int = 0
        self._request_payload_for_follow = {
            "profileNickname": "NONE",
            "profileImgPath": "https://cdn-contents.weverse.io/static/profile/profile_defalut_img_05.png"
        }
        self.loop = loop
        super().__init__(**kwargs)

    async def start(self, create_old_posts=False, create_notifications=True, create_media=False,
                    follow_new_communities=True):
        """Creates internal cache.

        This is the main process that should be run.

        This is a coroutine and must be awaited.

        :parameter create_old_posts: (:class:`bool`) Whether to create cache for old posts.
        :parameter create_notifications: (:class:`bool`) Whether to create/update cache for old notifications.
        :parameter create_media: (:class:`bool`) Whether to create/update cache for old media.
        :param follow_new_communities: bool
            Check for new communities and automatically follow them.

        :raises: :class:`Weverse.error.InvalidToken`
            If the token was invalid.
        :raises: :class:`Weverse.error.BeingRateLimited`
            If the client is being rate-limited.
        :raises: :class:`Weverse.error.LoginFailed`
            Login process had failed.
        :raises: :class:`asyncio.exceptions.TimeoutError`
            Waited too long for a login.
        :raises: :class:`Weverse.error.InvalidCredentials`
            If the user credentials were invalid or not provided.
        """
        try:
            if not self.web_session:
                self.web_session = aiohttp.ClientSession()

            if not self._login_info_exists and not self._token_exists:
                raise InvalidCredentials

            if self._login_info_exists:
                await self._try_login()
                await self._wait_for_login()  # wait for login or an exception to occur.

            if not await self.check_token_works():
                raise InvalidToken

            # create all communities that are subscribed to
            await self.create_communities()  # communities should be created no matter what

            # create and update community artists and their tabs
            await self.create_community_artists_and_tabs()

            self._follow_new_communities = follow_new_communities
            if self._follow_new_communities:
                await self.follow_all_communities()

            # create and update user notifications
            if create_notifications:
                await self.get_user_notifications()

            for community in self.all_communities.values():
                # load up posts
                if create_old_posts:
                    await self.create_posts(community)

                # load up media
                if create_media:
                    await self.create_media(community)

            self.cache_loaded = True

            if self._hook:
                if self.verbose:
                    print("Starting Notification Loop for Weverse Client.")
                await self._start_loop_for_hook()
        except Exception as err:
            raise err

    async def _start_loop_for_hook(self):
        """
        Start checking for new notifications in a new loop and call the hook with the list of new Notifications
        This will also create the posts associated with the notification so they can be used efficiently.
        This is a coroutine and must be awaited.
        """
        if not self._hook:
            raise NoHookFound

        self._hook_loop = True
        while self._hook_loop:
            if self._follow_new_communities:
                if self._time_passed == 14400:  # 4 hours in seconds
                    self._time_passed = 0
                    await self.follow_all_communities()

                self._time_passed += 30
            await asyncio.sleep(30)
            new_notifications = await self.update_cache_from_notification()
            if not new_notifications:
                continue

            if not asyncio.iscoroutinefunction(self._hook):
                self._hook(new_notifications)
            else:
                await self._hook(new_notifications)

    async def _try_login(self):
        """
        Will attempt to login to Weverse and set refresh token and token.
        This is a coroutine and must be awaited.
        """
        self._login(self.__process_login)

    async def __process_login(self, login_payload: dict):
        """
        Will process login credentials and set refresh token and token.
        This is a coroutine and must be awaited.
        Parameters
        ----------
        login_payload: dict
            The client's login payload
        """
        async with self.web_session.post(url=self._login_url, json=login_payload) as resp:
            if self.check_status(resp.status, self._login_url):
                data = await resp.json()
                refresh_token = data.get("refresh_token")
                token = data.get("access_token")
                if refresh_token:
                    self._set_refresh_token(refresh_token)
                if token:
                    self._set_token(token)
                self.expired_token = False
                return
        self._set_exception(LoginFailed())

    async def _refresh_token(self):
        """
        Refresh a token while logged in.

        This is a coroutine and must be awaited.

        """
        async with self.web_session.post(url=self._login_url, json=self._refresh_payload) as resp:
            if self.check_status(resp.status, self._login_url):
                data = await resp.json()
                token = data.get("access_token")
                if token:
                    self._set_token(token)
                self.expired_token = False
                return
        await self._try_login()
        await self._wait_for_login()

    @check_expired_token
    async def create_media(self, community: Community):
        """Paginate through a community's media and add it to object cache.

        :parameter community: :ref:`Community` the posts exist under.
        """
        media_tab_url = f"{self._api_stream_url}{community.id}/{self._api_media_tab}"
        async with self.web_session.get(media_tab_url, headers=self._headers) as resp:
            if self.check_status(resp.status, media_tab_url):
                data = await resp.json()
                media_objects, photo_media_dicts = iterate_community_media_categories(data)

                # This endpoint does NOT give us any information about the photos, therefore we must make
                # a separate api call to retrieve proper photo information for the photo media.
                for media in photo_media_dicts:
                    media_obj = await self.fetch_media(community.id, media.get("id"))
                    if media_obj:
                        media_objects.append(media_obj)

                self._add_media_to_cache(media_objects)

    @check_expired_token
    async def create_communities(self):
        """Get and Create the communities the logged in user has access to.

        This is a coroutine and must be awaited.
        """
        async with self.web_session.get(self._api_communities_url, headers=self._headers) as resp:
            if self.check_status(resp.status, self._api_communities_url):
                data = await resp.json()
                user_communities = data.get("communities")
                self.all_communities = create_community_objects(user_communities, self.all_communities)

    @check_expired_token
    async def create_community_artists_and_tabs(self, specific_community_ids: List[int] = None):
        """Create the community artists and tabs and add them to their respective communities.

        :param specific_community_ids: List[int]
            Will only do this list of community ids from the already existing communities.

        This is a coroutine and must be awaited.
        """
        for community in self.all_communities.values():
            if specific_community_ids:
                if community.id not in specific_community_ids:
                    continue
            url = self._api_communities_url + str(community.id)
            async with self.web_session.get(url, headers=self._headers) as resp:
                if self.check_status(resp.status, url):
                    data = await resp.json()
                    self.process_community_artists_and_tabs(community, data)
                    for artist in community.artists:
                        self.all_artists[artist.id] = artist
                    for tab in community.tabs:
                        self.all_tabs[tab.id] = tab

    @check_expired_token
    async def create_posts(self, community: Community, next_page_id: int = None):
        """Paginate through a community's posts and add it to object cache.

        This is a coroutine and must be awaited.

        :parameter community: :ref:`Community` the posts exist under.
        :parameter [OPTIONAL] next_page_id: Next Page ID (Weverse paginates posts).
        """
        artist_tab_url = self._api_communities_url + str(community.id) + '/' + self._api_all_artist_posts_url
        if next_page_id:
            artist_tab_url = artist_tab_url + "?from=" + str(next_page_id)
        async with self.web_session.get(artist_tab_url, headers=self._headers) as resp:
            if self.check_status(resp.status, artist_tab_url):
                data = await resp.json()
                posts = create_post_objects(data.get('posts'), community)
                for post in posts:
                    self.all_posts[post.id] = post
                    if post.photos:
                        for photo in post.photos:
                            self.all_photos[photo.id] = photo

                    if post.videos:
                        for video in post.photos:
                            self.all_videos[video.video_url] = video

                if not data.get('isEnded'):
                    await self.create_posts(community, data.get('lastId'))

    @check_expired_token
    async def create_post(self, community: Community, post_id) -> w_Post:
        """Create a post and update the cache with it. This is meant for an individual post.

        This is a coroutine and must be awaited.

        :parameter community: :ref:`Community` the post was created under.
        :parameter post_id: The id of the post we are needing to fetch.
        """
        post_url = self._api_communities_url + str(community.id) + '/posts/' + str(post_id)
        async with self.web_session.get(post_url, headers=self._headers) as resp:
            if self.check_status(resp.status, post_url):
                data = await resp.json()
                return (create_post_objects([data], community, new=True))[0]

    @check_expired_token
    async def get_user_notifications(self):
        """Get a list of updated user notification objects.

        This is a coroutine and must be awaited.

        :returns: List[:ref:`Notification`]
        """
        self._old_notifications = self.user_notifications  # important for keeping track of what is new.

        async with self.web_session.get(self._api_notifications_url, headers=self._headers) as resp:
            if self.check_status(resp.status, self._api_notifications_url):
                data = await resp.json()
                self.user_notifications = create_notification_objects(data.get('notifications'))
                for user_notification in self.user_notifications:
                    self.all_notifications[user_notification.id] = user_notification
                return self.user_notifications

    @check_expired_token
    async def check_new_user_notifications(self) -> bool:
        """Checks if there is a new user notification, updates the cache, and returns if there was.

        This is a coroutine and must be awaited.

        :returns: (:class:`bool`) Whether there is a new notification.


        This endpoint has been acting a bit off and not producing accurate results. It would be recommended to
        instantly get new notifications with :ref:`update_cache_from_notification` instead.
        """
        async with self.web_session.get(self._api_new_notifications_url, headers=self._headers) as resp:
            if self.check_status(resp.status, self._api_new_notifications_url):
                data = await resp.json()
                has_new = data.get('has_new')
                if has_new:
                    # update cache
                    # Not that cache_loaded necessarily matters here,
                    # but just in case other checks are happening concurrently.
                    self.cache_loaded = False
                    await self.update_cache_from_notification()
                    self.cache_loaded = True
                return has_new

    @check_expired_token
    async def translate(self, post_or_comment_id, is_post=False, is_comment=False, p_obj=None, community_id=None):
        """Translates a post or comment, must set post or comment to True.

        This is a coroutine and must be awaited.

        :parameter post_or_comment_id: A post or comment ID.
        :parameter [OPTIONAL] is_post: If we passed in a post.
        :parameter [OPTIONAL] is_comment: If we passed in a comment
        :parameter [OPTIONAL] p_obj: The object we are looking to translate
        :parameter [OPTIONAL] community_id: The community id the post/comment was made under.
        :returns: (:class:`str`) Translated message or NoneType
        """
        post_check = False
        comment_check = False
        method_url = None
        if is_post:
            method_url = "posts/"
            if not p_obj:
                p_obj = self.get_post_by_id(post_or_comment_id)
            post_check = True
        elif is_comment:
            method_url = "comments/"
            if not p_obj:
                p_obj = self.get_comment_by_id(post_or_comment_id)
            comment_check = True
        if not community_id:
            if p_obj:
                if comment_check:
                    if p_obj.post:
                        community_id = p_obj.post.artist.community_id
                if post_check:
                    if p_obj.artist:
                        community_id = p_obj.artist.community_id
            else:
                return None
        url = self._api_communities_url + str(community_id) + "/" + method_url + str(
            post_or_comment_id) + "/translate?languageCode=en"
        async with self.web_session.get(url, headers=self._headers) as resp:
            if self.check_status(resp.status, url):
                data = await resp.json()
                return data.get('translation')

    @check_expired_token
    async def fetch_artist_comments(self, community_id, post_id):
        """Fetches the artist comments on a post.

        This is a coroutine and must be awaited.

        :parameter community_id: Community ID the post is on.
        :parameter post_id: Post ID to fetch the artist comments of.
        :returns: List[:ref:`Comment`]
        """
        post_comments_url = self._api_communities_url + str(community_id) + '/posts/' + str(post_id) + "/comments/"
        async with self.web_session.get(post_comments_url, headers=self._headers) as resp:
            if self.check_status(resp.status, post_comments_url):
                data = await resp.json()
                return create_comment_objects(data.get('artistComments'))

    @check_expired_token
    async def fetch_comment_body(self, community_id, comment_id) -> str:
        """Fetches a comment from its ID.

        This is a coroutine and must be awaited.

        :parameter community_id: The ID of the community the comment belongs to.
        :parameter comment_id: The ID of the comment to fetch.
        :returns: (:class:`str`) Body of the comment.
        """
        comment_url = f"{self._api_communities_url}{str(community_id)}/comments/{comment_id}/"
        async with self.web_session.get(comment_url, headers=self._headers) as resp:
            if self.check_status(resp.status, comment_url):
                data = await resp.json()
                return data.get('body')

    @check_expired_token
    async def fetch_media(self, community_id, media_id) -> Optional[Media]:
        """Receive media object based on media id.

        This is a coroutine and must be awaited.

        :parameter community_id: The ID of the community the media belongs to.
        :parameter media_id: The ID of the media to fetch.
        :returns: :ref:`Media` or NoneType
        """
        media_url = self._api_communities_url + str(community_id) + "/medias/" + str(media_id)
        async with self.web_session.get(media_url, headers=self._headers) as resp:
            if self.check_status(resp.status, media_url):
                data = await resp.json()
                return create_media_object(data.get('media'))

    @check_expired_token
    async def fetch_announcement(self, community_id: int, announcement_id: int) -> Optional[Announcement]:
        """Receive announcement object based on announcement id.

        This is a coroutine and must be awaited.

        :parameter community_id: The ID of the community the media belongs to.
        :parameter announcement_id: The ID of the announcement to fetch.
        :returns: :ref:`Announcement` or NoneType
        """
        announcement_url = self._api_communities_url + str(community_id) + "/notices/" + str(announcement_id)
        async with self.web_session.get(announcement_url, headers=self._headers) as resp:
            if self.check_status(resp.status, announcement_url):
                data = await resp.json()
                return create_announcement_object(data)

    @staticmethod
    def __generate_random_nickname():
        from random import randint
        nickname_length = randint(10, 20)
        nickname = ""
        for i in range(0, nickname_length + 1):
            nickname += chr(randint(0, 255))
        return nickname

    @check_expired_token
    async def follow_community(self, community_id: Union[int, str], attempts: int = 0):
        r"""
        Follow a community

        :param community_id: Union[int, str]
            The community ID to follow.
        :param attempts: int
            The number of attempts for choosing a nickname after error.

        """
        url = self._api_communities_url + str(community_id)
        self._request_payload_for_follow['profileNickname'] = self.__generate_random_nickname()
        _headers = self._headers
        _headers['Content-Type'] = 'application/json'
        async with self.web_session.put(url, headers=_headers, data=dumps_(self._request_payload_for_follow)) as \
                resp:
            if resp.status == 400 and attempts < 1:
                return await self.follow_all_communities(community_id, attempts + 1)
            if self.check_status(resp.status, url):
                if self.verbose:
                    print(f"Followed {community_id}.")

    @check_expired_token
    async def follow_all_communities(self):
        r"""Follow all communities on Weverse"""
        communities_to_follow = [community_id for community_id in await self.get_all_community_ids() if community_id not in
                                 self.all_communities]
        for community_id in communities_to_follow:
            await self.follow_community(community_id)

        await self.create_communities()
        await self.create_community_artists_and_tabs(specific_community_ids=communities_to_follow)

    @check_expired_token
    async def get_all_community_ids(self) -> List[int]:
        r"""
        Get all the communities on Weverse.

        :returns: List[int]
            A list of community ids
        """
        url = self._api_url + 'app-properties/key/webCommunityRedirectPath'
        async with self.web_session.get(url, headers=self._headers) as resp:
            if self.check_status(resp.status, url):
                list_of_communities_: dict = await resp.json()
                return [community_info['id'] for community_info in list_of_communities_.get('communities')]
        return []

    async def update_cache_from_notification(self) -> List[Notification]:
        """Grab a new post based from new notifications and add it to cache.

        Will also return the new notifications found.

        This is a coroutine and must be awaited.

        :returns: List[:class:`models.Notification`]
        """
        new_notifications = []
        try:
            notifications = await self.get_user_notifications()

            if not notifications:
                return new_notifications

            new_notifications = self.get_new_notifications()
            for notification in new_notifications:
                await self.__manage_notification_posts(notification)
        except Exception as e:
            if self.verbose:
                print(f"Failed to update Weverse Cache - {e}")
        return new_notifications

    async def __manage_notification_posts(self, notification: Notification):
        """Manages the creation of Notification posts and comments.

        This is a coroutine and must be awaited.

        :param notification: Notification to create comments and posts for.
        """
        notification_type = self.determine_notification_type(notification.message)
        community = self.get_community_by_id(notification.community_id)
        if notification_type == 'comment':
            artist_comments = await self.fetch_artist_comments(notification.community_id, notification.contents_id)
            if artist_comments:
                comment = artist_comments[0]
                comment.post = self.get_post_by_id(comment.post_id)
                if comment.post:
                    if comment.post.artist_comments:
                        comment.post.artist_comments.insert(0, comment)
                    else:
                        comment.post.artist_comments = [comment]
                self.all_comments[comment.id] = comment
        elif notification_type in ["tofans", "post"]:
            post = await self.create_post(community, notification.contents_id)
            if post:
                self.all_posts[post.id] = post
        elif notification_type == 'media':
            media = await self.fetch_media(community.id, notification.contents_id)
            if media:
                self.all_media[media.id] = media
        elif notification_type == 'announcement':
            announcement = await self.fetch_announcement(community.id, notification.contents_id)
            if announcement:
                self.all_announcements[announcement.id] = announcement

    async def check_token_works(self) -> bool:
        """
        Check if a token is invalid.

        This is a coroutine and must be awaited.

        :returns: (:class:`bool`) True if the token works.
        """
        async with self.web_session.get(url=self._user_endpoint, headers=self._headers) as resp:
            self._expired_token = not resp.status == 200
            return not self._expired_token
