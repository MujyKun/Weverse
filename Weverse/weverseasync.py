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
            for community in self.communities:
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
                self.communities = obj.create_community_objects(user_communities)

    async def create_community_artists_and_tabs(self):
        """Create the community artists and tabs and add them to their respective communities."""
        for community in self.communities:
            url = self.api_communities_url + str(community.id)
            async with self.web_session.get(url, headers=self.headers) as resp:
                if self.check_status(resp.status, url):
                    response_text = await resp.text()
                    response_text_as_dict = json.loads(response_text)
                    self.process_community_artists_and_tabs(community, response_text_as_dict)

    async def create_posts(self, community: Community, next_page_id: int = None):
        """Paginate through a community's posts and add it to object cache."""
        artist_tab_url = self.api_communities_url + str(community.id) + '/' + self.api_all_artist_posts_url
        if next_page_id:
            artist_tab_url = artist_tab_url + "?from=" + str(next_page_id)
        async with self.web_session.get(artist_tab_url, headers=self.headers) as resp:
            if self.check_status(resp.status, artist_tab_url):
                response_text = await resp.text()
                response_text_as_dict = json.loads(response_text)
                obj.create_post_objects(response_text_as_dict.get('posts'), community)
                if not response_text_as_dict.get('isEnded'):
                    await self.create_posts(community, response_text_as_dict.get('lastId'))

    async def get_user_notifications(self):
        """Get a list of updated user notification objects"""
        async with self.web_session.get(self.api_notifications_url, headers=self.headers) as resp:
            if self.check_status(resp.status, self.api_notifications_url):
                response_text = await resp.text()
                response_text_as_dict = json.loads(response_text)
                self.user_notifications = obj.create_notification_objects(response_text_as_dict.get('notifications'))
                return self.user_notifications

    async def check_new_user_notifications(self):
        """Returns true if there is a new user notification."""
        async with self.web_session.get(self.api_new_notifications_url, headers=self.headers) as resp:
            if self.check_status(resp.status, self.api_new_notifications_url):
                response_text = await resp.text()
                response_text_as_dict = json.loads(response_text)
                return response_text_as_dict.get('has_new')

    async def translate(self, post_or_comment_id, post=False, comment=False):
        """Translates a post or comment, must set post or comment to True."""
        p_obj = None
        post_check = False
        comment_check = False
        community_id = None
        method_url = None
        if post:
            method_url = "comments/"
            p_obj = self.get_post_by_id(post_or_comment_id)
            post_check = True
        elif comment:
            method_url = "posts/"
            p_obj = self.get_comment_by_id(post_or_comment_id)
            comment_check = False
        if p_obj:
            if comment_check:
                community_id = p_obj.post.artist.community_id
            if post_check:
                community_id = p_obj.artist.community_id
        else:
            return None
        url = self.api_communities_url + str(community_id) + "/" + method_url + str(post_or_comment_id) + "/translate?languageCode=en"
        async with self.web_session.get(url, headers=self.headers) as resp:
            if self.check_status(resp.status, url):
                response_text = await resp.text()
                response_text_as_dict = json.loads(response_text)
                return response_text_as_dict.get('translation')

    async def create_to_fan_post(self, community_id, to_fan_id):
        """Connects to a ToFan post (Basically a story) and returns a ToFan object. """
        artist_tab_url = self.api_communities_url + str(community_id) + '/' + self.api_artist_to_fans + to_fan_id + '?pageSize=1'
        async with self.web_session.get(artist_tab_url, headers=self.headers) as resp:
            if self.check_status(resp.status, artist_tab_url):
                response_text = await resp.text()
                response_text_as_dict = json.loads(response_text)
                return obj.create_to_fan_post(response_text_as_dict.get('post'))

    async def fetch_artist_comments(self, community_id, post_id):
        """Fetches the artist comments on a post."""
        post_comments_url = self.api_communities_url + str(community_id) + '/posts/' + str(post_id) + "/comments/"
        async with self.web_session.get(post_comments_url, headers=self.headers) as resp:
            if self.check_status(resp.status, post_comments_url):
                response_text = await resp.text()
                response_text_as_dict = json.loads(response_text)
                return obj.create_comment_objects(response_text_as_dict.get('artistComments'))

    async def fetch_media(self, community_id, media_id):
        """Receive media object based on media id."""
        media_url = self.api_communities_url + str(community_id) + "/medias/" + str(media_id)
        async with self.web_session.get(media_url, headers=self.headers) as resp:
            if self.check_status(resp.status, media_url):
                response_text = await resp.text()
                response_text_as_dict = json.loads(response_text)
                return obj.create_media_object(response_text_as_dict.get('media'))



