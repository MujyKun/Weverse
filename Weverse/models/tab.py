class Tab:
    r"""A Post object that represents a Weverse Post.

    It is not suggested to create a Post manually, but rather through the
    following method: :class:`Weverse.objects.create_post_objects`

    The information retrieved on a Post is directly from the Weverse API and altered to fit this class.

    .. container:: operations

        .. describe:: x == y

            Checks if two Tab objects have the same ID.

        .. describe:: x != y

            Check if the IDs of the Tab objects are not equal.

        .. describe:: str(x)

            Returns the Tab name.

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

    def __eq__(self, other):
        """Check if the IDs of the Tab objects are equal."""
        if not isinstance(other, Tab):
            return NotImplemented

        return self.id == other.id

    def __ne__(self, other):
        """Check if the IDs of the Tab objects are not equal."""
        return not self == other

    def __str__(self):
        """Returns the Tab name."""
        return f"{self.name}"
