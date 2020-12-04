class Photo:
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

