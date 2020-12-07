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

    def create_post(self, community: Community, post_id):
        """Create a post and update the cache with it. This is meant for an individual post."""
        post_url = self.api_communities_url + str(community.id) + '/posts/' + post_id
        with self.web_session.get(post_url, headers=self.headers) as resp:
            if self.check_status(resp.status_code, post_url):
                response_text = resp.text
                response_text_as_dict = json.loads(response_text)
                return (obj.create_post_objects([response_text_as_dict], community, new=True))[0]

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
                has_new = response_text_as_dict.get('has_new')
                if has_new:
                    # update cache
                    # Not that cache_loaded necessarily matters here,
                    # but just in case other checks are happening concurrently.
                    self.cache_loaded = False
                    self.update_cache_from_notification()
                    self.cache_loaded = True
                return has_new

    def translate(self, post_or_comment_id, is_post=False, is_comment=False, p_obj=None):
        """Translates a post or comment, must set post or comment to True."""
        post_check = False
        comment_check = False
        community_id = None
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

    def fetch_artist_comments(self, community_id, post_id):
        """Fetches the artist comments on a post."""
        post_comments_url = self.api_communities_url + str(community_id) + '/posts/' + str(post_id) + "/comments/"
        with self.web_session.get(post_comments_url, headers=self.headers) as resp:
            if self.check_status(resp.status_code, post_comments_url):
                response_text = resp.text
                response_text_as_dict = json.loads(response_text)
                return obj.create_comment_objects(response_text_as_dict.get('artistComments'))

    def fetch_media(self, community_id, media_id):
        """Receive media object based on media id."""
        media_url = self.api_communities_url + str(community_id) + "/medias/" + str(media_id)
        with self.web_session.get(media_url, headers=self.headers) as resp:
            if self.check_status(resp.status_code, media_url):
                response_text = resp.text
                response_text_as_dict = json.loads(response_text)
                return obj.create_media_object(response_text_as_dict.get('media'))

    def update_cache_from_notification(self):
        try:
            notification = (self.get_user_notifications())[0]
            noti_type = self.determine_notification_type(notification.message)
            community = self.get_community_by_id(notification.community_id)
            if noti_type == 'comment':
                artist_comments = self.fetch_artist_comments(notification.community_id, notification.contents_id)
                comment = artist_comments[0]
                comment.post = self.get_post_by_id(comment.post_id)
                if comment.post.artist_comments:
                    comment.post.artist_comments.insert(0, comment)
                else:
                    comment.post.artist_comments = [comment]
            elif noti_type == "post":
                self.create_post(community, notification.contents_id)
            elif noti_type == 'media':
                self.new_media.insert(0, self.fetch_media(community.id, notification.contents_id))
            elif noti_type == 'announcement':
                return  # not keeping track of announcements in cache ATM
        except Exception as e:
            if self.verbose:
                print(f"Failed to update Weverse Cache - {e}")
