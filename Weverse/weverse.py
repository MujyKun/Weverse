import Weverse.error as error
import Weverse.objects as obj
from . import artist as w_artist, \
    comment as w_comment, \
    community as w_community, \
    media as w_media, \
    notification as w_notification,  \
    photo as w_photo, \
    post as w_post, \
    tab as w_tab


class Weverse:
    """
    Client for connecting to Weverse and creating the internal cache.

    Do not create an object directly from this class.
    Instead, create a WeverseSync or WeverseAsync object since those are concrete.
    """
    def __init__(self, **kwargs):
        self.verbose = kwargs.get('verbose')
        self.web_session = kwargs.get('web_session')
        self.token = kwargs.get('authorization')
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
        self.user_endpoint = "https://weversewebapi.weverse.io/wapi/v1/users/me"

        self.all_posts = {}
        self.all_artists = {}
        self.all_comments = {}
        self.all_notifications = {}
        self.all_photos = {}
        self.all_communities = {}
        self.all_media = {}
        self.all_tabs = {}

    def check_status(self, status, url) -> bool:
        """
        Confirm the status of a URL

        :param status: Status code of url connection
        :param url: Link that we connected to.
        :return: True if the connection was a success.
        :raises: error.InvalidToken if there was an invalid token.
        """
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
        """
        Process the community artists and tabs and add them to their respective communities.

        :param community: Community object
        :param response_text_as_dict: Response text of connection to endpoint but as a dict.
        """
        # split up response dict by artists and tabs
        community_artists = response_text_as_dict.get('artists')
        community_tabs = response_text_as_dict.get('tabs')

        # create artist and tab objects under the community
        community.artists = obj.create_artist_objects(community_artists)
        community.tabs = obj.create_tab_objects(community_tabs)

        # set the community for each artist
        for artist in community.artists:
            artist.community = community

    def get_artist_by_id(self, artist_id) -> w_artist.Artist:
        """
        Get artist by their ID.

        :param artist_id: The artist's ID
        """
        artist = self.all_artists.get(artist_id)
        if not artist:
            for t_artist in self.all_artists.values():
                if t_artist.community_user_id == artist_id:
                    artist = t_artist
        return artist

    def get_tab_by_id(self, tab_id) -> w_tab.Tab:
        """
        Get tab by their ID.

        :param tab_id: The tab ID
        """
        return self.all_tabs.get(tab_id)

    def get_post_by_id(self, post_id) -> w_post.Post:
        """
        Get a post by the ID

        :param post_id: Post ID
        """
        return self.all_posts.get(post_id)

    def get_comment_by_id(self, comment_id) -> w_comment.Comment:
        """
        Get a comment by the ID
        :param comment_id: Comment ID
        """
        return self.all_comments.get(comment_id)

    def get_notification_by_id(self, notification_id) -> w_notification.Notification:
        """
        Get a notification by the ID

        :param notification_id: Notification ID
        """
        return self.all_notifications.get(notification_id)

    def get_photo_by_id(self, photo_id) -> w_photo.Photo:
        """
        Get a photo by the ID

        :param photo_id: Photo ID
        """
        return self.all_photos.get(photo_id)

    def get_community_by_id(self, community_id) -> w_community.Community:
        """
        Get a community by the ID.

        :param community_id: Community ID
        """
        return self.all_communities.get(community_id)

    def get_media_by_id(self, media_id) -> w_media.Media:
        """
        Get Media by the ID

        :param media_id: Media ID
        """
        return self.all_media.get(media_id)

    @staticmethod
    def determine_notification_type(notification_body) -> str:
        """
        Determine the post type based on the notification body.
        NOTE: notifications don't usually say if they are comments. This is to differentiate Posts and Comments.

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



