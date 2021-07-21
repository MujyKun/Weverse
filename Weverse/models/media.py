from typing import List

from . import Photo


class Media:
    r"""A Media object that represents a Weverse Media Post.

    It is not suggested to create a Media object manually, but rather through the
    following method: :class:`Weverse.objects.create_media_object`

    The information retrieved on Media is directly from the Weverse API and altered to fit this class.

    .. container:: operations

        .. describe:: x == y

            Checks if two Media objects have the same ID.

        .. describe:: x != y

            Checks if two Media objects do not have the same ID.

        .. describe:: str(x)

            Returns the Media body message.

        .. describe:: len(x)

            Returns the amount of images (not videos) in the Media object.

    Parameters
    ----------
    id: int
        ID of the Media post.
    community_id: int
        ID of the Community the media post was made in.
    body: str
        The media content AKA the body of the message.
    type: str
        The type of media post it is.
    thumbnail_path: str
        The (url??) of the thumbnail.
    title: str
        The title of the media post.
    level:
        The level of access the media post is categorized under.
    video_link: str
        The video link supplied under the media post.
    youtube_id: str
        The youtube video ID.


    Attributes
    -----------
    id: int
        ID of the Media post.
    community_id: int
        ID of the Community the media post was made in.
    body: str
        The media content AKA the body of the message.
    type: str
        The type of media post it is.
    thumbnail_path: str
        The (url??) of the thumbnail.
    title: str
        The title of the media post.
    level:
        The level of access the media post is categorized under.
    video_link: str
        The video link supplied under the media post.
    youtube_id: str
        The youtube video ID.
    photos: List[:ref:`Photo`]
        A list of photos under the media post.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.community_id = kwargs.get('communityId')
        self.body = kwargs.get('body')
        self.type = kwargs.get('type')
        self.thumbnail_path = kwargs.get('thumbnailPath')
        self.title = kwargs.get('title')
        self.level = kwargs.get('level')
        self.video_link = kwargs.get('extVideoPath')
        self.youtube_id = kwargs.get('youtubeId')
        self.photos: List[Photo] = kwargs.get('photo_objects') or []

    def __eq__(self, other):
        """Check if the IDs of the Media objects are equal."""
        if not isinstance(other, Media):
            return NotImplemented

        return self.id == other.id

    def __ne__(self, other):
        """Check if the IDs of the Media objects are not equal."""
        return not self == other

    def __str__(self):
        """Returns the Media body message."""
        return f"{self.body}"

    def __len__(self):
        """Returns the amount of images (not videos) available."""
        return len(self.photos)
