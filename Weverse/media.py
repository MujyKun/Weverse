class Media:
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

