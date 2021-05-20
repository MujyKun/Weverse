class Community:
    r"""A Comment object that represents a Weverse Comment that belongs to an Artist.

    It is not suggested to create a Comment manually, but rather through the
    following method: :class:`Weverse.objects.create_comment_objects`

    The information retrieved on a Comment is directly from the Weverse API and altered to fit this class.

    Parameters
    ----------
    id: :class:`int`
        The Community ID.
    name: :class:`str`
        The Community Name.
    description: :class:`str`
        Description of the Community.
    member_count: :class:`int`
        Amount of members in the community.
    home_banner: :class:`str`
        Direct Image URL to the home banner.
    icon: :class:`str`
        Direct Image URL to the Icon.
    Banner: :class:`str`
        Direct Image URL to the Banner.
    full_name: :class:`str`
        Full Name of the Community.
    fc_member: bool
        If a special membership is required to join.
    show_member_count: bool
        If the member count is visible.

    Attributes
    -----------
    id: :class:`int`
        The Community ID.
    name: :class:`str`
        The Community Name.
    description: :class:`str`
        Description of the Community.
    member_count: :class:`int`
        Amount of members in the community.
    home_banner: :class:`str`
        Direct Image URL to the home banner.
    icon: :class:`str`
        Direct Image URL to the Icon.
    Banner: :class:`str`
        Direct Image URL to the Banner.
    full_name: :class:`str`
        Full Name of the Community.
    fc_member: bool
        If a special membership is required to join.
    show_member_count: bool
        If the member count is visible.
    artists: List[Artist]
        List of artists the community has.
    tabs: List[Tab]
        The Tabs the community has.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('community_id')
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.member_count = kwargs.get('member_count')
        self.home_banner = kwargs.get('home_banner')
        self.icon = kwargs.get('icon')
        self.banner = kwargs.get('banner')
        self.full_name = kwargs.get('full_name')
        self.fc_member = kwargs.get('fc_member')
        self.show_member_count = kwargs.get('show_member_count')
        self.artists = []
        self.tabs = []

