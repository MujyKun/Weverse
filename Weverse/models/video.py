from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Weverse.models import Post


class Video:
    r"""A Video object that represents a Weverse Video that belongs to media or a post.

    It is not suggested to create a Video manually, but rather through the
    following method: :class:`Weverse.objects.create_video_objects`

    The information retrieved on a Video is directly from the Weverse API and altered to fit this class.

    Videos do not have unique IDs.

    .. container:: operations

        .. describe:: x == y

            Check if the Video URL and Post are the same.

        .. describe:: x != y

            Check if the Video objects are not equal.

        .. describe:: str(x)

            Returns the Video URL.

        .. describe:: len(x)

            Returns the length of the video in seconds.

    Parameters
    ----------
    video_url: int
        Direct URL to the video.
    thumbnail_url: str
        URL of the thumbnail.
    thumbnail_width: int
        Width of the thumbnail
    thumbnail_height: int
        Height of the thumbnail.
    length: int
        Duration of the video in seconds.

    Attributes
    -----------
    video_url: int
        Direct URL to the video.
    thumbnail_url: str
        URL of the thumbnail.
    thumbnail_width: int
        Width of the thumbnail
    thumbnail_height: int
        Height of the thumbnail.
    length: int
        Duration of the video in seconds.
    post: Optional[Post]
        The Post Object the video belongs to.
    """
    def __init__(self, **kwargs):
        self.video_url = kwargs.get('video_url')
        self.thumbnail_url = kwargs.get('thumbnail_url')
        self.thumbnail_width = kwargs.get('thumbnail_width')
        self.thumbnail_height = kwargs.get('thumbnail_height')
        self.length = kwargs.get('length')
        self.post: Optional[Post] = None

    def __eq__(self, other):
        """Check if the Video URL and Post are the same."""
        if not isinstance(other, Video):
            return NotImplemented

        video_url_check = self.video_url == other.video_url
        if other.post and self.post:
            return video_url_check and (self.post == other.post)
        return video_url_check

    def __ne__(self, other):
        """Check if the Video objects are not equal."""
        return not self == other

    def __str__(self):
        """Returns the Video URL."""
        return f"{self.video_url}"

    def __len__(self):
        """Returns the length of the video in seconds."""
        return self.length
