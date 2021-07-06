class Post:
    r"""A Post object that represents a Weverse Post.

    It is not suggested to create a Post manually, but rather through the
    following method: :class:`Weverse.objects.create_post_objects`

    The information retrieved on a Post is directly from the Weverse API and altered to fit this class.

    Parameters
    ----------
    id: int
        The ID of the post.
    community_tab_id: int
        The tab the post is under.
    type: str
        The type of Post.
    body: str
        Body Message on the Post.
    comment_count: int
        Current amount of comments on the Post
    like_count: int
        Current amount of likes on the Post
    max_comment_count: int
        Maximum amount of comments that can be on the Post
    has_my_like: bool
        If the client user has the post liked.
    has_my_bookmark: bool
        If the client user has the post bookmarked.
    created_at:
        When the post was created
    updated_at:
        When the post was last modified.
    is_locked: bool
        Whether the post is locked.
    is_blind: bool
        Whether the post is visible?? Unknown
    is_active: bool
        Whether the post is active.
    is_private: bool
        Whether the post is private.
    photos: List[:ref:`Photo`]
        A list of photos under the post.
    videos: List[:ref:`Video`]
        A list of videos under the post.
    is_hot_trending_post: bool
        If the post is trending.
    is_limit_comment: bool
        If the comments are limited.
    artist_comments: List[:ref:`Comment`]
        The Artist comments under the post.
    community_artist_id: int
        The Community Artist ID that made the post.
    artist_id: int
        The ID of the Artist that made the post.

    Attributes
    -----------
    id: int
        The ID of the post.
    community_tab_id: int
        The tab the post is under.
    type: str
        The type of Post.
    body: str
        Body Message on the Post.
    comment_count: int
        Current amount of comments on the Post
    like_count: int
        Current amount of likes on the Post
    max_comment_count: int
        Maximum amount of comments that can be on the Post
    has_my_like: bool
        If the client user has the post liked.
    has_my_bookmark: bool
        If the client user has the post bookmarked.
    created_at:
        When the post was created
    updated_at:
        When the post was last modified.
    is_locked: bool
        Whether the post is locked.
    is_blind: bool
        Whether the post is visible?? Unknown
    is_active: bool
        Whether the post is active.
    is_private: bool
        Whether the post is private.
    photos: List[:ref:`Photo`]
        A list of photos under the post.
    videos: List[:ref:`Video`]
        A list of videos under the post.
    is_hot_trending_post: bool
        If the post is trending.
    is_limit_comment: bool
        If the comments are limited.
    artist_comments: List[:ref:`Comment`]
        The Artist comments under the post.
    community_artist_id: int
        The Community Artist ID that made the post.
    artist_id: int
        The ID of the Artist that made the post.
    artist: Artist
        The Artist Object the post belongs to.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('post_id')
        self.community_tab_id = kwargs.get('community_tab_id')
        self.type = kwargs.get('post_type')
        self.body = kwargs.get('body')
        self.comment_count = kwargs.get('comment_count')
        self.like_count = kwargs.get('like_count')
        self.max_comment_count = kwargs.get('max_comment_count')
        self.has_my_like = kwargs.get('has_my_like')
        self.has_my_bookmark = kwargs.get('has_my_bookmark')
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')
        self.is_locked = kwargs.get('is_locked')
        self.is_blind = kwargs.get('is_blind')
        self.is_active = kwargs.get('is_active')
        self.is_private = kwargs.get('is_private')
        self.photos = kwargs.get('photos')
        self.videos = kwargs.get('videos')
        self.is_hot_trending_post = kwargs.get('is_hot_trending_post')
        self.is_limit_comment = kwargs.get('is_limit_comment')
        self.artist_comments = kwargs.get('artist_comments')
        self.community_artist_id = kwargs.get('community_artist_id')
        self.artist_id = kwargs.get('artist_id')
        self.artist = None

