class Media:
    r"""A Media object that represents a Weverse Media Post.

    It is not suggested to create a Media object manually, but rather through the
    following method: :class:`Weverse.objects.create_media_object`

    The information retrieved on Media is directly from the Weverse API and altered to fit this class.

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

