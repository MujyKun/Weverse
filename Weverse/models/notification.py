class Notification:
    r"""A Media object that represents a Weverse Media Post.

    It is not suggested to create a Notification object manually, but rather through the
    following method: :class:`Weverse.objects.create_notification_objects`

    The information retrieved on a Notification is directly from the Weverse API and altered to fit this class.

    Parameters
    ----------
    id: int
        The id of the notification.
    message: str
        The message of the notification.
    bold_element: str
        The bolded element in the notification.
    community_id: int
        The community id associated with the notification.
    community_name: str
        The community name associated with the notification.
    contents_type: str
        The type of post it is.
    contents_id: int
        The id of the content post.
    notified_at:
        The time the notification was triggered.
    icon_image_url: str
        Icon image url of the notification.
    thumbnail_image_url: str
        Thumbnail url of the notification.
    artist_id: int
        The ID of the Artist that released the content.
    is_membership_content: bool
        If the content is exclusive to members.
    is_web_only: bool
        Whether the notification is only available directly on the website.
    platform: str
        The platform of the notification.


    Attributes
    -----------
    id: int
        The id of the notification.
    message: str
        The message of the notification.
    bold_element: str
        The bolded element in the notification.
    community_id: int
        The community id associated with the notification.
    community_name: str
        The community name associated with the notification.
    contents_type: str
        The type of post it is.
    contents_id: int
        The id of the content post.
    notified_at:
        The time the notification was triggered.
    icon_image_url: str
        Icon image url of the notification.
    thumbnail_image_url: str
        Thumbnail url of the notification.
    artist_id: int
        The ID of the Artist that released the content.
    is_membership_content: bool
        If the content is exclusive to members.
    is_web_only: bool
        Whether the notification is only available directly on the website.
    platform: str
        The platform of the notification.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('notification_id')
        self.message = kwargs.get('message')
        self.bold_element = kwargs.get('bold_element')
        self.community_id = kwargs.get('community_id')
        self.community_name = kwargs.get('community_name')
        self.contents_type = kwargs.get('contents_type')
        self.contents_id = kwargs.get('contents_id')
        self.notified_at = kwargs.get('notified_at')
        self.icon_image_url = kwargs.get('icon_image_url')
        self.thumbnail_image_url = kwargs.get('thumbnail_image_url')
        self.artist_id = kwargs.get('artist_id')
        self.is_membership_content = kwargs.get('is_membership_content')
        self.is_web_only = kwargs.get('is_web_only')
        self.platform = kwargs.get('platform')
