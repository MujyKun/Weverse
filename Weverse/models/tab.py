class Tab:
    r"""A Post object that represents a Weverse Post.

    It is not suggested to create a Post manually, but rather through the
    following method: :class:`Weverse.objects.create_post_objects`

    The information retrieved on a Post is directly from the Weverse API and altered to fit this class.

    Parameters
    ----------
    tab_id: [Optional] int
        The ID of the Tab.
    name: [Optional] str
        The Tab name.

    Attributes
    -----------
    id: int
        The ID of the Tab.
    name: str
        The Tab name.

    """
    def __init__(self, tab_id=None, name=None):
        self.id = tab_id
        self.name = name
