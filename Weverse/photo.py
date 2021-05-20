class Photo:
    r"""A Photo object that represents a Weverse Photo that belongs to media or a post.

    It is not suggested to create a Photo manually, but rather through the
    following method: :class:`Weverse.objects.create_photo_objects`

    The information retrieved on a Photo is directly from the Weverse API and altered to fit this class.

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
        self.content_index = kwargs.get('content_index')
        self.thumbnail_img_url = kwargs.get('thumbnail_img_url')
        self.thumbnail_img_width = kwargs.get('thumbnail_img_width')
        self.thumbnail_img_height = kwargs.get('thumbnail_img_height')
        self.original_img_url = kwargs.get('original_img_url')
        self.original_img_width = kwargs.get('original_img_width')
        self.original_img_height = kwargs.get('original_img_height')
        self.file_name = kwargs.get('file_name')
        self.post = None

