import aiohttp
import json
import Weverse.objects as obj
from Weverse.community import Community
from Weverse.weverse import Weverse
from asyncio import get_event_loop


class WeverseAsync(Weverse):
    def __init__(self, loop=get_event_loop(), **kwargs):
        self.loop = loop
        super().__init__(**kwargs)

    async def start(self):
        """Creates internal cache.

        This is the main process that should be run.
        """
        try:
            if not self.web_session:
                self.web_session = aiohttp.ClientSession()
            await self.create_communities()
            await self.create_community_artists_and_tabs()
            await self.get_user_notifications()
            for community in self.all_communities.values():
                await self.create_posts(community)
            self.cache_loaded = True
        except Exception as err:
            raise err

    async def create_communities(self):
        """Get and Create the communities the logged in user has access to."""
        async with self.web_session.get(self.api_communities_url, headers=self.headers) as resp:
            if self.check_status(resp.status, self.api_communities_url):
                response_text = await resp.text()
                response_text_as_dict = json.loads(response_text)
                user_communities = response_text_as_dict.get("communities")
                self.all_communities = obj.create_community_objects(user_communities)

    async def create_community_artists_and_tabs(self):
        """Create the community artists and tabs and add them to their respective communities."""
        for community in self.all_communities.values():
            url = self.api_communities_url + str(community.id)
            async with self.web_session.get(url, headers=self.headers) as resp:
                if self.check_status(resp.status, url):
                    response_text = await resp.text()
                    response_text_as_dict = json.loads(response_text)
                    self.process_community_artists_and_tabs(community, response_text_as_dict)
                    for artist in community.artists:
                        self.all_artists[artist.id] = artist
                    for tab in community.tabs:
                        self.all_tabs[tab.id] = tab

    async def create_posts(self, community: Community, next_page_id: int = None):
        """Paginate through a community's posts and add it to object cache."""
        artist_tab_url = self.api_communities_url + str(community.id) + '/' + self.api_all_artist_posts_url
        if next_page_id:
            artist_tab_url = artist_tab_url + "?from=" + str(next_page_id)
        async with self.web_session.get(artist_tab_url, headers=self.headers) as resp:
            if self.check_status(resp.status, artist_tab_url):
                response_text = await resp.text()
                response_text_as_dict = json.loads(response_text)
                posts = obj.create_post_objects(response_text_as_dict.get('posts'), community)
                for post in posts:
                    self.all_posts[post.id] = post
                if not response_text_as_dict.get('isEnded'):
                    await self.create_posts(community, response_text_as_dict.get('lastId'))

    async def create_post(self, community: Community, post_id):
        """Create a post and update the cache with it. This is meant for an individual post."""
        post_url = self.api_communities_url + str(community.id) + '/posts/' + str(post_id)
        async with self.web_session.get(post_url, headers=self.headers) as resp:
            if self.check_status(resp.status, post_url):
                response_text = await resp.text()
                response_text_as_dict = json.loads(response_text)
                return (obj.create_post_objects([response_text_as_dict], community, new=True))[0]

    async def get_user_notifications(self):
        """Get a list of updated user notification objects"""
        async with self.web_session.get(self.api_notifications_url, headers=self.headers) as resp:
            if self.check_status(resp.status, self.api_notifications_url):
                response_text = await resp.text()
                response_text_as_dict = json.loads(response_text)
                self.user_notifications = obj.create_notification_objects(response_text_as_dict.get('notifications'))
                for user_notification in self.user_notifications:
                    self.all_notifications[user_notification.id] = user_notification
                return self.user_notifications

    async def check_new_user_notifications(self):
        """Returns if there is a new user notification. Also updates cache."""
        async with self.web_session.get(self.api_new_notifications_url, headers=self.headers) as resp:
            if self.check_status(resp.status, self.api_new_notifications_url):
                response_text = await resp.text()
                response_text_as_dict = json.loads(response_text)
                has_new = response_text_as_dict.get('has_new')
                if has_new:
                    # update cache
                    # Not that cache_loaded necessarily matters here,
                    # but just in case other checks are happening concurrently.
                    self.cache_loaded = False
                    await self.update_cache_from_notification()
                    self.cache_loaded = True
                return has_new

    async def translate(self, post_or_comment_id, is_post=False, is_comment=False, p_obj=None, community_id=None):
        """Translates a post or comment, must set post or comment to True."""
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
        async with self.web_session.get(url, headers=self.headers) as resp:
            if self.check_status(resp.status, url):
                response_text = await resp.text()
                response_text_as_dict = json.loads(response_text)
                return response_text_as_dict.get('translation')

    async def fetch_artist_comments(self, community_id, post_id):
        """Fetches the artist comments on a post."""
        post_comments_url = self.api_communities_url + str(community_id) + '/posts/' + str(post_id) + "/comments/"
        async with self.web_session.get(post_comments_url, headers=self.headers) as resp:
            if self.check_status(resp.status, post_comments_url):
                response_text = await resp.text()
                response_text_as_dict = json.loads(response_text)
                return obj.create_comment_objects(response_text_as_dict.get('artistComments'))

    async def fetch_comment_body(self, community_id, comment_id):
        """Fetches a comment from it's ID."""
        comment_url = f"{self.api_communities_url}{str(community_id)}/comments/{comment_id}/"
        async with self.web_session.get(comment_url, headers=self.headers) as resp:
            if self.check_status(resp.status, comment_url):
                response_text = await resp.text()
                response_text_as_dict = json.loads(response_text)
                return response_text_as_dict.get('body')

    async def fetch_media(self, community_id, media_id):
        """Receive media object based on media id."""
        media_url = self.api_communities_url + str(community_id) + "/medias/" + str(media_id)
        async with self.web_session.get(media_url, headers=self.headers) as resp:
            if self.check_status(resp.status, media_url):
                response_text = await resp.text()
                response_text_as_dict = json.loads(response_text)
                return obj.create_media_object(response_text_as_dict.get('media'))

    async def update_cache_from_notification(self):
        """Grab a new post based from a notification and add it to cache."""
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

        :return: returns True if the token works.
        """
        async with self.web_session.get(url=self.user_endpoint, headers=self.headers) as resp:
            return resp.status == 200
