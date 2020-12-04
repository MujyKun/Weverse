class Community:
    def __init__(self, **kwargs):

        self.id = kwargs.get('community_id')
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.member_count = kwargs.get('member_count')
        self.home_banner = kwargs.get('home_banner')
        self.icon = kwargs.get('icon')
        self.banner = kwargs.get('banner')
        self.full_name = kwargs.get('full_name')
        self.fc_member = kwargs.get('fc_member')
        self.show_member_count = kwargs.get('show_member_count')
        self.artists = []
        self.tabs = []

