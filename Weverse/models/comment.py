class Comment:
    r"""A Comment object that represents a Weverse Comment that belongs to an Artist.

    It is not suggested to create a Comment manually, but rather through the
    following method: :class:`Weverse.objects.create_comment_objects`

    The information retrieved on a Comment is directly from the Weverse API and altered to fit this class.

    Parameters
    ----------
    id: :class:`int`
        The ID of the comment.
    body: :class:`str`
        The comment content AKA the body of the message.
    comment_count: :class:`int`
        Amount of comments inside of this comment (replies).
    like_count: :class:`int`
        Amount of likes on the comment.
    has_my_like: :class:`bool`
        Whether the client has liked the comment.
    is_blind: :class:`bool`
        NOT SURE WHAT THIS IS
    post_id: :class:`int`
        The Post ID that the comment was created under.
    created_at:
        The time the comment was created.
    updated_at:
        The time the comment was updated.

    Attributes
    -----------
    id: int
        The ID of the comment.
    body: str
        The comment content AKA the body of the message.
    comment_count: int
        Amount of comments inside of this comment (replies).
    like_count: int
        Amount of likes on the comment.
    has_my_like: bool
        Whether the client has liked the comment.
    is_blind: bool
        NOT SURE WHAT THIS IS
    post_id: int
        The Post ID that the comment was created under.
    created_at:
        The time the comment was created.
    updated_at:
        The time the comment was updated.
    post: Post
        The Post Object the comment belongs to.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('comment_id')
        self.body = kwargs.get('body')
        self.comment_count = kwargs.get('comment_count')
        self.like_count = kwargs.get('like_count')
        self.has_my_like = kwargs.get('has_my_like')
        self.is_blind = kwargs.get('is_blind')
        self.post_id = kwargs.get('post_id')
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')
        self.post = None
