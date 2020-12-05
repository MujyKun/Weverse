import json
import requests
import Weverse.objects as obj
from Weverse.weverse import Weverse
from Weverse.community import Community


class WeverseSync(Weverse):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start(self):
        """Creates internal cache."""
        try:
            if not self.web_session:
                self.web_session = requests.Session()
            self.create_communities()
            self.create_community_artists_and_tabs()
            self.get_user_notifications()
            for community in self.communities:
                self.create_posts(community)
            self.cache_loaded = True
        except Exception as err:
            raise err

    def create_communities(self):
        """Get and Create the communities the logged in user has access to."""
        with self.web_session.get(self.api_communities_url, headers=self.headers) as resp:
            if self.check_status(resp.status_code, self.api_communities_url):
                response_text = resp.text
                response_text_as_dict = json.loads(response_text)
                user_communities = response_text_as_dict.get("communities")
                self.communities = obj.create_community_objects(user_communities)

    def create_community_artists_and_tabs(self):
        """Create the community artists and tabs and add them to their respective communities."""
        for community in self.communities:
            url = self.api_communities_url + str(community.id)
            with self.web_session.get(url, headers=self.headers) as resp:
                if self.check_status(resp.status_code, url):
                    response_text = resp.text
                    response_text_as_dict = json.loads(response_text)
                    self.process_community_artists_and_tabs(community, response_text_as_dict)

    def create_posts(self, community: Community, next_page_id: int = None):
        """Paginate through a community's posts and add it to object cache."""
        artist_tab_url = self.api_communities_url + str(community.id) + '/' + self.api_all_artist_posts_url
        if next_page_id:
            artist_tab_url = artist_tab_url + "?from=" + str(next_page_id)
        with self.web_session.get(artist_tab_url, headers=self.headers) as resp:
            if self.check_status(resp.status_code, artist_tab_url):
                response_text = resp.text
                response_text_as_dict = json.loads(response_text)
                obj.create_post_objects(response_text_as_dict.get('posts'), community)
                if not response_text_as_dict.get('isEnded'):
                    self.create_posts(community, response_text_as_dict.get('lastId'))

    def get_user_notifications(self):
        """Get a list of updated user notification objects"""
        with self.web_session.get(self.api_notifications_url, headers=self.headers) as resp:
            if self.check_status(resp.status_code, self.api_notifications_url):
                response_text = resp.text
                response_text_as_dict = json.loads(response_text)
                self.user_notifications = obj.create_notification_objects(response_text_as_dict.get('notifications'))
                return self.user_notifications

    def check_new_user_notifications(self):
        """Returns true if there is a new user notification."""
        with self.web_session.get(self.api_new_notifications_url, headers=self.headers) as resp:
            if self.check_status(resp.status_code, self.api_new_notifications_url):
                response_text = resp.text
                response_text_as_dict = json.loads(response_text)
                return response_text_as_dict.get('has_new')

    def translate(self, post_or_comment_id, post=False, comment=False):
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
        with self.web_session.get(url, headers=self.headers) as resp:
            if self.check_status(resp.status_code, url):
                response_text = resp.text
                response_text_as_dict = json.loads(response_text)
                return response_text_as_dict.get('translation')

