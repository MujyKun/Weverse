class Comment:
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
