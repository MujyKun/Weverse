from . import create_artist_objects, create_tab_objects, InvalidToken
from .models import Artist as w_Artist, \
    Comment as w_Comment, Media as w_Media, Notification as w_Notification, Photo as w_Photo, Post as w_Post, \
    Tab as w_Tab, Community as w_Community, Video as w_Video


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
    token:
        The account token to connect to the Weverse API. In order to find your token, please refer to :ref:`account_token`

    Attributes
    -----------
    verbose: bool
        Whether to print out verbose messages.
    web_session:
        An aiohttp or requests client session.
    user_notifications: list
        Most recent notifications of the account connected.
    api_url: str
        URL to connect to the API
    api_communities_url: str
        Endpoint for communities
    api_notifications_url: str
        Endpoint for user notifications
    api_new_notifications_url: str
        Endpoint for checking new user notifications
    api_all_artist_posts_url: str
        Endpoint for getting the Artist Feed from a community
    api_artist_to_fans: str
        part of the endpoint (NOT FULL) for viewing the tofans posts.
    api_all_communities_info_url: str
        Endpoint for information about ALL communities and ALL idols.
    cache_loaded: bool
        Whether the Internal Weverse Cache is fully loaded.
        This will change for a split moment when grabbing a new post.
    new_media: list(Media)
        We do not store ALL old media objects as cache, so only when there are new media, we store it
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
   """
    def __init__(self, **kwargs):
        self.verbose = kwargs.get('verbose')
        self.web_session = kwargs.get('web_session')
        self._token = kwargs.get('authorization')
        self.user_notifications = []
        self._headers = {'Authorization': f"Bearer {self._token}"}
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
        # Videos have the url as the key due to no unique ID.
        self.all_videos = {}

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
            raise InvalidToken
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

    def get_artist_by_id(self, artist_id) -> w_Artist:
        """
        Get artist by their ID.

        :param artist_id: The artist's ID
        :returns: :ref:`Artist` or NoneType
        """
        artist = self.all_artists.get(artist_id)
        if not artist:
            for t_artist in self.all_artists.values():
                if t_artist.community_user_id == artist_id:
                    artist = t_artist
        return artist

    def get_tab_by_id(self, tab_id) -> w_Tab:
        """
        Get tab by their ID.

        :param tab_id: The tab ID
        :returns: :ref:`Tab` or NoneType
        """
        return self.all_tabs.get(tab_id)

    def get_post_by_id(self, post_id) -> w_Post:
        """
        Get a post by the ID

        :param post_id: Post ID
        :returns: :ref:`Post` or NoneType
        """
        return self.all_posts.get(post_id)

    def get_comment_by_id(self, comment_id) -> w_Comment:
        """
        Get a comment by the ID
        :param comment_id: Comment ID
        :returns: :ref:`Comment` or NoneType
        """
        return self.all_comments.get(comment_id)

    def get_notification_by_id(self, notification_id) -> w_Notification:
        """
        Get a notification by the ID

        :param notification_id: Notification ID
        :returns: :ref:`Notification` or NoneType
        """
        return self.all_notifications.get(notification_id)

    def get_photo_by_id(self, photo_id) -> w_Photo:
        """
        Get a photo by the ID

        :param photo_id: Photo ID
        :returns: :ref:`Photo` or NoneType
        """
        return self.all_photos.get(photo_id)

    def get_video_by_url(self, video_url) -> w_Video:
        """
        Get a video by the direct URL.

        :param video_url: URL of the video
        :return: :ref:`Video` or NoneType
        """
        return self.all_videos.get(video_url)

    def get_community_by_id(self, community_id) -> w_Community:
        """
        Get a community by the ID.

        :param community_id: Community ID
        :returns: :ref:`Community` or NoneType
        """
        return self.all_communities.get(community_id)

    def get_media_by_id(self, media_id) -> w_Media:
        """
        Get Media by the ID

        :param media_id: Media ID
        :returns: :ref:`Media` or NoneType
        """
        return self.all_media.get(media_id)

    @staticmethod
    def determine_notification_type(notification_body) -> str:
        """
        Determine the post type based on the notification body.

        Since notifications do not differentiate between Posts and Comments, this is for that purpose.

        :param notification_body: The body of the notification.
        :returns: A string with either
            "comment", "media", or "post"
        """

        if "commented on" in notification_body or "replied to" in notification_body:
            return "comment"
        # if "shared a moment with you" in notification_body:
            # return "tofans"
        if "created a new post!" in notification_body or "shared a moment with you" in notification_body:
            return "post"
        if "Check out the new media" in notification_body:
            return "media"
        if "New announcement" in notification_body:
            return "announcement"



