from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Weverse.models import Post


class Photo:
    r"""A Photo object that represents a Weverse Photo that belongs to media or a post.

    It is not suggested to create a Photo manually, but rather through the
    following method: :class:`Weverse.objects.create_photo_objects`

    The information retrieved on a Photo is directly from the Weverse API and altered to fit this class.

    .. container:: operations

        .. describe:: x == y

            Checks if two Photo objects have the same ID.

        .. describe:: x != y

            Checks if two Photo objects do not have the same ID.

        .. describe:: str(x)

            Returns the file name.

    Parameters
    ----------
    id: int
        The ID of the photo.
    content_index: int
        Index the photo is in from a bundle of photos.
    thumbnail_img_url: str
        The thumbnail image link.
    thumbnail_img_width: str
        The original image width.
    thumbnail_img_height: str
        The thumbnail image height.
    original_img_url: str
        The original image link.
    original_img_width: str
        The original image width.
    original_img_height: str
        The original image height.
    file_name: str
        File name of the photo.

    Attributes
    -----------
    id: int
        The ID of the photo.
    media_id: Optional[int]
        The media ID of the photo (if there is one).
    content_index: int
        Index the photo is in from a bundle of photos.
    thumbnail_img_url: str
        The thumbnail image link.
    thumbnail_img_width: str
        The original image width.
    thumbnail_img_height: str
        The thumbnail image height.
    original_img_url: str
        The original image link.
    original_img_width: str
        The original image width.
    original_img_height: str
        The original image height.
    file_name: str
        File name of the photo.
    post: Post
        The Post Object the photo belongs to.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('photo_id')
        self.media_id = kwargs.get('media_id')
        self.content_index = kwargs.get('content_index')
        self.thumbnail_img_url = kwargs.get('thumbnail_img_url')
        self.thumbnail_img_width = kwargs.get('thumbnail_img_width')
        self.thumbnail_img_height = kwargs.get('thumbnail_img_height')
        self.original_img_url = kwargs.get('original_img_url')
        self.original_img_width = kwargs.get('original_img_width')
        self.original_img_height = kwargs.get('original_img_height')
        self.file_name = kwargs.get('file_name')
        self.post: Optional[Post] = None

    def __eq__(self, other):
        """Check if the IDs of the Photo objects are equal."""
        if not isinstance(other, Photo):
            return NotImplemented

        return self.id == other.id

    def __ne__(self, other):
        """Check if the IDs of the Photo objects are not equal."""
        return not self == other

    def __str__(self):
        """Returns the file name."""
        return f"{self.file_name}"
