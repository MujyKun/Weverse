from typing import Optional, List

from . import Video, Photo, Artist, Comment


class Announcement:
    r"""An Announcement object that represents a Weverse Notice for a Community.

    It is not suggested to create an Announcement manually, but rather through the
    following method: :class:`Weverse.objects.create_announcement_objects`

    The information retrieved on a Post is directly from the Weverse API and altered to fit this class.

    .. container:: operations

        .. describe:: x == y

            Checks if two Announcement objects have the same ID.

        .. describe:: x != y

            Checks if two Announcement objects do not have the same ID.

        .. describe:: str(x)

            Returns the Announcement content.

    Parameters
    ----------
    id: int
        The ID of the post.
    communityId: int
        The Community ID.
    title: str
        The title of the announcement notice.
    content: str
        The HTML body of the page notice.
    createdAt:
        Timestamp with the date of when the announcement was created.
    exposedAt:
        Timestamp with the date of when the announcement was released.
    categoryId: int
        Category that the announcement belongs to (used for paginating or quick endpoint access)
    fcOnly: bool
        If only premium members have access to the announcement.

    Attributes
    -----------
    id: int
        The ID of the post.
    community_id: int
        The Community ID.
    title: str
        The title of the announcement notice.
    html_content: str
        The HTML body of the page notice.
    created_at:
        Timestamp with the date of when the announcement was created.
    exposed_at:
        Timestamp with the date of when the announcement was released.
    category_id: int
        Category that the announcement belongs to (used for paginating or quick endpoint access)
    fc_only: bool
        If only premium members have access to the announcement.
    image_url: Optional[str]
        An image url if one is present.

    """
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.community_id = kwargs.get("communityId")
        self.title = kwargs.get("title")
        self.html_content: str = kwargs.get("content")
        self.created_at = kwargs.get("createdAt")
        self.exposed_at = kwargs.get("exposedAt")
        self.category_id = kwargs.get("categoryId")
        self.fc_only: bool = kwargs.get("fcOnly")
        self.image_url: Optional[str] = self.__get_image()

    def __eq__(self, other):
        """Check if the IDs of the Announcement objects are equal."""
        if not isinstance(other, Announcement):
            return NotImplemented

        return self.id == other.id

    def __ne__(self, other):
        """Check if the IDs of the Announcement objects are not equal."""
        return not self == other

    def __str__(self):
        """Returns the Announcement content."""
        return f"{self.html_content}"

    def __get_image(self):
        """Retrieve the image url from the html content if any exists."""
        src_loc = self.html_content.find("src=")
        if src_loc == -1:
            return ""
        skipped_start = self.html_content[src_loc:len(self.html_content)]
        end_of_src = skipped_start.find(" ")  # a space will indicate the end of the src
        if skipped_start == -1:
            return ""

        image_src = self.html_content[src_loc:end_of_src]
        image_src = image_src.replace("src=", "")
        image_src = image_src.replace('\\', "")
        image_src = image_src.replace('"', "")
        return image_src
