import Weverse.error as error
import Weverse.objects as obj


class Weverse:
    def __init__(self, **kwargs):
        self.verbose = kwargs.get('verbose')
        self.web_session = kwargs.get('web_session')
        self.token = kwargs.get('authorization')
        self.communities = []
        self.user_notifications = []
        self.headers = {'Authorization': f"Bearer {self.token}"}
        self.api_url = "https://weversewebapi.weverse.io/wapi/v1/"
        self.api_communities_url = self.api_url + "communities/"  # endpoint for communities
        self.api_notifications_url = self.api_url + "stream/notifications/"  # endpoint for user notifications
        # endpoint for checking new user notifications
        self.api_new_notifications_url = self.api_notifications_url + "has-new/"
        self.api_all_artist_posts_url = "posts/artistTab/"  # Artist Feed from a community
        self.api_artist_to_fans = "posts/tofans/"
        # endpoint for information about ALL communities and ALL idols.
        self.api_all_communities_info_url = self.api_communities_url + "info/"
        self.cache_loaded = False
        self.new_media = []  # We do not store ALL media objects as cache, so only when there are new media, we store it

    def check_status(self, status, url):
        if status == 200:
            return True
        elif status == 401:
            raise error.InvalidToken
        elif status == 404:
            if self.verbose:
                # raise error.PageNotFound
                print("WARNING: " + url + " was not found.")
        else:
            if self.verbose:
                print("WARNING: " + url + " Failed to load. [Status: " + str(status) + "]")

    @staticmethod
    def process_community_artists_and_tabs(community, response_text_as_dict):
        """Process the community artists and tabs and add them to their respective communities."""
        # split up response dict by artists and tabs
        community_artists = response_text_as_dict.get('artists')
        community_tabs = response_text_as_dict.get('tabs')

        # create artist and tab objects under the community
        community.artists = obj.create_artist_objects(community_artists)
        community.tabs = obj.create_tab_objects(community_tabs)

        # set the community for each artist
        for artist in community.artists:
            artist.community = community

    def get_artist_by_id(self, artist_id):
        for community in self.communities:
            for artist in community.artists:
                if artist_id in [artist.id, artist.community_user_id]:
                    return artist

    def get_post_by_id(self, post_id):
        for community in self.communities:
            for artist in community.artists:
                for post in artist.posts:
                    if post.id == post_id:
                        return post

    def get_comment_by_id(self, comment_id):
        for community in self.communities:
            for artist in community.artists:
                for post in artist.posts:
                    for comment in post.artist_comments:
                        if comment.id == comment_id:
                            return comment

    def get_notification_by_id(self, notification_id):
        for notification in self.user_notifications:
            if notification.id == notification_id:
                return notification

    def get_photo_by_id(self, photo_id):
        for community in self.communities:
            for artist in community.artists:
                for post in artist.posts:
                    for photo in post.photos:
                        if photo.id == photo_id:
                            return photo

    def get_community_by_id(self, community_id):
        for community in self.communities:
            if community_id == community.id:
                return community

    @staticmethod
    def determine_notification_type(notification_body):
        """Determine the post type based on the notification body.
        NOTE -> notifications don't usually say if they are comments. This is to differentiate Posts and Comments.

        Returns comment, media, or post as a string.
        """

        if "commented on" in notification_body:
            return "comment"
        # if "shared a moment with you" in notification_body:
            # return "tofans"
        if "created a new post!" in notification_body or "shared a moment with you" in notification_body:
            return "post"
        if "Check out the new media" in notification_body:
            return "media"
        if "New announcement" in notification_body:
            return "announcement"



