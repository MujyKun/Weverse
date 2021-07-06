import aiohttp
from asyncio import get_event_loop
from .models import Community, Post as w_Post
from . import WeverseClient, create_post_objects, create_community_objects, create_notification_objects, \
    create_comment_objects, create_media_object


class WeverseClientAsync(WeverseClient):
    r"""
    Asynchronous Weverse Client that Inherits from :ref:`WeverseClient`.

    Parameters
    ----------
    loop:
        Asyncio Event Loop
    kwargs:
        Same as :ref:`Weverse`.


    Attributes
    -----------
    loop:
        Asyncio Event Loop

    Attributes are the same as :ref:`WeverseClient`.
    """

    def __init__(self, loop=get_event_loop(), **kwargs):
        self.loop = loop
        super().__init__(**kwargs)

    async def start(self, create_old_posts=True, create_notifications=True):
        """Creates internal cache.

        This is the main process that should be run.

        This is a coroutine and must be awaited.

        :parameter create_old_posts: (:class:`bool`) Whether to create cache for old posts.
        :parameter create_notifications: (:class:`bool`) Whether to create/update cache for old notifications.

        :raises: :class:`Weverse.error.InvalidToken`
        :raises: :class:`Weverse.error.BeingRateLimited`
        """
        try:
            if not self.web_session:
                self.web_session = aiohttp.ClientSession()

            # create all communities that are subscribed to
            await self.create_communities()  # communities should be created no matter what

            # create and update community artists and their tabs
            await self.create_community_artists_and_tabs()

            # create and update user notifications
            if create_notifications:
                await self.get_user_notifications()

            # load up posts
            if create_old_posts:
                for community in self.all_communities.values():
                    await self.create_posts(community)

            self.cache_loaded = True
        except Exception as err:
            raise err

    async def create_communities(self):
        """Get and Create the communities the logged in user has access to.

        This is a coroutine and must be awaited.
        """
        async with self.web_session.get(self.api_communities_url, headers=self._headers) as resp:
            if self.check_status(resp.status, self.api_communities_url):
                data = await resp.json()
                user_communities = data.get("communities")
                self.all_communities = create_community_objects(user_communities)

    async def create_community_artists_and_tabs(self):
        """Create the community artists and tabs and add them to their respective communities.

        This is a coroutine and must be awaited.
        """
        for community in self.all_communities.values():
            url = self.api_communities_url + str(community.id)
            async with self.web_session.get(url, headers=self._headers) as resp:
                if self.check_status(resp.status, url):
                    data = await resp.json()
                    self.process_community_artists_and_tabs(community, data)
                    for artist in community.artists:
                        self.all_artists[artist.id] = artist
                    for tab in community.tabs:
                        self.all_tabs[tab.id] = tab

    async def create_posts(self, community: Community, next_page_id: int = None):
        """Paginate through a community's posts and add it to object cache.

        This is a coroutine and must be awaited.

        :parameter community: :ref:`Community` the posts exist under.
        :parameter [OPTIONAL] next_page_id: Next Page ID (Weverse paginates posts).
        """
        artist_tab_url = self.api_communities_url + str(community.id) + '/' + self.api_all_artist_posts_url
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

    async def create_post(self, community: Community, post_id) -> w_Post:
        """Create a post and update the cache with it. This is meant for an individual post.

        This is a coroutine and must be awaited.

        :parameter community: :ref:`Community` the post was created under.
        :parameter post_id: The id of the post we are needing to fetch.
        """
        post_url = self.api_communities_url + str(community.id) + '/posts/' + str(post_id)
        async with self.web_session.get(post_url, headers=self._headers) as resp:
            if self.check_status(resp.status, post_url):
                data = await resp.json()
                return (create_post_objects([data], community, new=True))[0]

    async def get_user_notifications(self):
        """Get a list of updated user notification objects.

        This is a coroutine and must be awaited.

        :returns: List[:ref:`Notification`]
        """
        async with self.web_session.get(self.api_notifications_url, headers=self._headers) as resp:
            if self.check_status(resp.status, self.api_notifications_url):
                data = await resp.json()
                self.user_notifications = create_notification_objects(data.get('notifications'))
                for user_notification in self.user_notifications:
                    self.all_notifications[user_notification.id] = user_notification
                return self.user_notifications

    async def check_new_user_notifications(self) -> bool:
        """Checks if there is a new user notification, updates the cache, and returns if there was.

        This is a coroutine and must be awaited.

        :returns: (:class:`bool`) Whether there is a new notification.
        """
        async with self.web_session.get(self.api_new_notifications_url, headers=self._headers) as resp:
            if self.check_status(resp.status, self.api_new_notifications_url):
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
        url = self.api_communities_url + str(community_id) + "/" + method_url + str(
            post_or_comment_id) + "/translate?languageCode=en"
        async with self.web_session.get(url, headers=self._headers) as resp:
            if self.check_status(resp.status, url):
                data = await resp.json()
                return data.get('translation')

    async def fetch_artist_comments(self, community_id, post_id):
        """Fetches the artist comments on a post.

        This is a coroutine and must be awaited.

        :parameter community_id: Community ID the post is on.
        :parameter post_id: Post ID to fetch the artist comments of.
        :returns: List[:ref:`Comment`]
        """
        post_comments_url = self.api_communities_url + str(community_id) + '/posts/' + str(post_id) + "/comments/"
        async with self.web_session.get(post_comments_url, headers=self._headers) as resp:
            if self.check_status(resp.status, post_comments_url):
                data = await resp.json()
                return create_comment_objects(data.get('artistComments'))

    async def fetch_comment_body(self, community_id, comment_id):
        """Fetches a comment from its ID.

        This is a coroutine and must be awaited.

        :parameter community_id: The ID of the community the comment belongs to.
        :parameter comment_id: The ID of the comment to fetch.
        :returns: (:class:`str`) Body of the comment.
        """
        comment_url = f"{self.api_communities_url}{str(community_id)}/comments/{comment_id}/"
        async with self.web_session.get(comment_url, headers=self._headers) as resp:
            if self.check_status(resp.status, comment_url):
                data = await resp.json()
                return data.get('body')

    async def fetch_media(self, community_id, media_id):
        """Receive media object based on media id.

        This is a coroutine and must be awaited.

        :parameter community_id: The ID of the community the media belongs to.
        :parameter media_id: The ID of the media to fetch.
        :returns: :ref:`Media` or NoneType
        """
        media_url = self.api_communities_url + str(community_id) + "/medias/" + str(media_id)
        async with self.web_session.get(media_url, headers=self._headers) as resp:
            if self.check_status(resp.status, media_url):
                data = await resp.json()
                return create_media_object(data.get('media'))

    async def update_cache_from_notification(self):
        """Grab a new post based from a notification and add it to cache.

        This is a coroutine and must be awaited.
        """
        try:
            notifications = await self.get_user_notifications()
            if not notifications:
                return
            notification = notifications[0]
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
                    self.new_media.insert(0, media)
                    self.all_media[media.id] = media
            elif notification_type == 'announcement':
                return  # not keeping track of announcements in cache ATM
        except Exception as e:
            if self.verbose:
                print(f"Failed to update Weverse Cache - {e}")

    async def check_token_works(self) -> bool:
        """
        Check if a token is invalid.

        This is a coroutine and must be awaited.

        :returns: (:class:`bool`) True if the token works.
        """
        async with self.web_session.get(url=self.user_endpoint, headers=self._headers) as resp:
            return resp.status == 200
