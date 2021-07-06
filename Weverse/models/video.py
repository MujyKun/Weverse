class Video:
    r"""A Video object that represents a Weverse Video that belongs to media or a post.

    It is not suggested to create a Video manually, but rather through the
    following method: :class:`Weverse.objects.create_video_objects`

    The information retrieved on a Video is directly from the Weverse API and altered to fit this class.

    Videos do not have unique IDs.

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
    post: Post
        The Post Object the video belongs to.
    """
    def __init__(self, **kwargs):
        self.video_url = kwargs.get('video_url')
        self.thumbnail_url = kwargs.get('thumbnail_url')
        self.thumbnail_width = kwargs.get('thumbnail_width')
        self.thumbnail_height = kwargs.get('thumbnail_height')
        self.length = kwargs.get('length')
        self.post = None

