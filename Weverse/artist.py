class Artist:
    r"""An Artist object that represents a Weverse Artist that belongs in a community.

    It is not suggested to create an Artist manually, but rather through the
    following method: :class:`Weverse.objects.create_artist_objects`

    The information retrieved on an Artist is directly from the Weverse API and altered to fit this class.

    Parameters
    ----------
    id: :class:`int`
        The Artist ID.
    community_user_id: :class:`int`
        Artist's ID in the community.
    name: :class:`str`
        The Primary Artist Name.
    list_name: :class:`list`
        A list of names for the Artist.
    is_online: :class:`bool`
        Whether the Artist is currently online
    profile_nick_name: :class:`str`
        Artist nickname.
    profile_img_path: :class:`str`
        Image URL for the Artist's profile.
    is_birthday: :class:`bool`
        Whether it is the Artist's birthday.
    group_name: :class:`str`
        The group name the Artist is associated with.
    max_comment_count: :class:`int`
        The maximum amount of comments this Artist can post.
    community_id: :class:`int`
        The ID of the community this Artist object was selected from.
    is_enabled: :class:`bool`
        If the Artist account is enabled.
    has_new_to_fans: :class:`bool`
        If the Artist has a new post for fans.
    has_new_private_to_fans: :class:`bool`
        If the Artist has a new private post for fans.
    to_fan_last_id: :class:`int`
        The latest tofan post ID.
    to_fan_last_created_at:
        When the artist's last tofan post was created.
    to_fan_last_expire_in:
        When the artist's last tofan post expires.
    birthday_img_url: :class:`str`
        A direct image url to the artist's birthday image.
    community: Community
        The community the Artist is in.
    posts: :class:`list`
        A list of posts the Artist has.

    Attributes
    -----------
    id: int
        The Artist ID.
    community_user_id: int
        Artist's ID in the community.
    name: str
        The Primary Artist Name.
    list_name: list
        A list of names for the Artist.
    is_online: bool
        Whether the Artist is currently online
    profile_nick_name: str
        Artist nickname.
    profile_img_path: str
        Image URL for the Artist's profile.
    is_birthday: bool
        Whether it is the Artist's birthday.
    group_name: str
        The group name the Artist is associated with.
    max_comment_count: int
        The maximum amount of comments this Artist can post.
    community_id: int
        The ID of the community this Artist object was selected from.
    is_enabled: bool
        If the Artist account is enabled.
    has_new_to_fans: bool
        If the Artist has a new post for fans.
    has_new_private_to_fans: bool
        If the Artist has a new private post for fans.
    to_fan_last_id: int
        The latest tofan post ID.
    to_fan_last_created_at:
        When the artist's last tofan post was created.
    to_fan_last_expire_in:
        When the artist's last tofan post expires.
    birthday_img_url: str
        A direct image url to the artist's birthday image.
    community: Community
        The community the Artist is in.
    posts: list
        A list of posts the Artist has.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('artist_id')
        self.community_user_id = kwargs.get('community_user_id')
        self.name = kwargs.get('name')
        self.list_name = kwargs.get('list_name')
        self.is_online = kwargs.get('is_online')
        self.profile_nick_name = kwargs.get('profile_nick_name')
        self.profile_img_path = kwargs.get('profile_img_path')
        self.is_birthday = kwargs.get('is_birthday')
        self.group_name = kwargs.get('group_name')
        self.max_comment_count = kwargs.get('max_comment_count')
        self.community_id = kwargs.get('community_id')
        self.is_enabled = kwargs.get('is_enabled')
        self.has_new_to_fans = kwargs.get('has_new_to_fans')
        self.has_new_private_to_fans = kwargs.get('has_new_private_to_fans')
        self.to_fan_last_id = kwargs.get('to_fan_last_id')
        self.to_fan_last_created_at = kwargs.get('to_fan_last_created_at')
        self.to_fan_last_expire_in = kwargs.get('to_fan_last_expire_in')
        self.birthday_img_url = kwargs.get('birthday_img_url')
        self.community = None
        self.posts = []
