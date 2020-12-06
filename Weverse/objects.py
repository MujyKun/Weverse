from Weverse.community import Community
from Weverse.artist import Artist
from Weverse.tab import Tab
from Weverse.notification import Notification
from Weverse.post import Post
from Weverse.photo import Photo
from Weverse.comment import Comment
from Weverse.media import Media


def create_community_objects(current_communities: list):
    """Creates community objects based on a list of information sent in and returns the objects."""
    community_objects = []
    if current_communities:
        for community in current_communities:
            kwargs = {
                'community_id': community.get('id'),
                'name': community.get('name'),
                'description': community.get('description'),
                'member_count': community.get('memberCount'),
                'home_banner': community.get('homeBannerImgPath'),
                'icon': community.get('iconImgPath'),
                'banner': community.get('bannerImgPath'),
                'full_name': community.get('fullname'),
                'fc_member': community.get('fcMember'),
                'show_member_count': community.get('showMemberCount')
            }
            community_object = Community(**kwargs)
            community_objects.append(community_object)
    return community_objects


def create_artist_objects(current_artists: list):
    """Creates artist objects based on a list of information sent in and returns the objects."""
    community_artists = []
    if current_artists:
        for artist in current_artists:
            kwargs = {
                'artist_id': artist.get('id'),
                'community_user_id': artist.get('communityUserId'),
                'name': artist.get('name'),
                'list_name': artist.get('listName'),
                'is_online': artist.get('isOnline'),
                'profile_nick_name': artist.get('profileNickName'),
                'profile_img_path': artist.get('profileImgPath'),
                'is_birthday': artist.get('isBirthday'),
                'group_name': artist.get('groupName'),
                'max_comment_count': artist.get('maxCommentCount'),
                'community_id': artist.get('communityId'),
                'is_enabled': artist.get('isEnabled'),
                'has_new_to_fans': artist.get('hasNewToFans'),
                'has_new_private_to_fans': artist.get('hasNewPrivateToFans'),
                'to_fan_last_id': artist.get('toFanLastId'),
                'to_fan_last_created_at': artist.get('toFanLastCreatedAt'),
                'to_fan_last_expire_in': artist.get('toFanLastExpireIn'),
                'birthday_img_url': artist.get('birthdayImgUrl')
            }
            community_artist = Artist(**kwargs)
            community_artists.append(community_artist)
    return community_artists


def create_tab_objects(current_tabs: list):
    """Creates tab objects based on a list of information sent in and returns the objects."""
    community_tabs = []
    if current_tabs:
        for tab in current_tabs:
            kwargs = {
                'tab_id': tab.get('id'),
                'name': tab.get('name')
            }
            community_tab = Tab(**kwargs)
            community_tabs.append(community_tab)
    return community_tabs


def create_notification_objects(current_notifications: list):
    """Creates notification objects based on a list of information sent in and returns the objects."""
    user_notifications = []
    if current_notifications:
        for notification in current_notifications:
            kwargs = {
                'notification_id': notification.get('id'),
                'message': notification.get('message'),
                'bold_element': notification.get('boldElement'),
                'community_id': notification.get('communityId'),
                'community_name': notification.get('CommunityName'),
                'contents_type': notification.get('contentsType'),
                'contents_id': notification.get('contentsId'),
                'notified_at': notification.get('notifiedAt'),
                'icon_image_url': notification.get('iconImageUrl'),
                'thumbnail_image_url': notification.get('thumbnailImageUrl'),
                'artist_id': notification.get('artistId'),
                'is_membership_content': notification.get('isMembershipContent'),
                'is_web_only': notification.get('isWebOnly'),
                'platform': notification.get('platform')
            }
            user_notification = Notification(**kwargs)
            user_notifications.append(user_notification)
    return user_notifications


def create_post_objects(current_posts: list, community: Community, new=False):
    """Creates post objects based on a list of posts sent in and the community and returns the objects."""
    posts = []
    if current_posts:
        for post in current_posts:
            artist_comments = create_comment_objects(post.get('artistComments'))
            artist_photos = create_photo_objects(post.get('photos'))
            artist_info = post.get('communityUser')
            community_artist_id = artist_info.get('id')
            kwargs = {
                'artist_id': artist_info.get('artistId'),
                'community_artist_id': community_artist_id,
                'post_id': post.get('id'),
                'community_tab_id': post.get('communityTabId'),
                'post_type': post.get('type'),
                'body': post.get('body'),
                'comment_count': post.get('commentCount'),
                'like_count': post.get('likeCount'),
                'max_comment_count': post.get('maxCommentCount'),
                'has_my_like': post.get('hasMyLike'),
                'has_my_bookmark': post.get('hasMyBookmark'),
                'created_at': post.get('createdAt'),
                'updated_at': post.get('updatedAt'),
                'is_locked': post.get('isLocked'),
                'is_blind': post.get('isBlind'),
                'is_active': post.get('isActive'),
                'is_private': post.get('isPrivate'),
                'photos': artist_photos,
                'is_hot_trending_post': post.get('isHotTrendingPost'),
                'is_limit_comment': post.get('isLimitComment'),
                'artist_comments': artist_comments
            }
            post_obj = Post(**kwargs)
            if new:
                posts.insert(0, post_obj)
            else:
                posts.append(post_obj)
            for comment in artist_comments:
                comment.post = post_obj
            for photo in artist_photos:
                photo.post = post_obj
            for artist in community.artists:
                if artist.community_user_id == community_artist_id:
                    artist.posts.append(post_obj)
                    post_obj.artist = artist
    return posts


def create_photo_objects(current_photos: list):
    """Creates & Returns photo objects based on a list of photos"""
    photos = []
    if current_photos:
        for photo in current_photos:
            kwargs = {
                'photo_id': photo.get('id'),
                'content_index': photo.get('contentIndex'),
                'thumbnail_img_url': photo.get('thumbnailImgUrl'),
                'thumbnail_img_width': photo.get('thumbnailImgWidth'),
                'thumbnail_img_height': photo.get('thumbnailImgHeight'),
                'original_img_url': photo.get('orgImgUrl'),
                'original_img_width': photo.get('orgImgWidth'),
                'original_img_height': photo.get('orgImgHeight'),
                'file_name': photo.get('downloadImgFilename')
            }
            photo_obj = Photo(**kwargs)
            photos.append(photo_obj)
    return photos


def create_comment_objects(current_comments: list):
    """Creates & Returns comment objects based on a list of comments"""
    comments = []
    if current_comments:
        for comment in current_comments:
            kwargs = {
                'comment_id': comment.get('id'),
                'body': comment.get('body'),
                'comment_count': comment.get('commentCount'),
                'like_count': comment.get('likeCount'),
                'has_my_like': comment.get('hasMyLike'),
                'is_blind': comment.get('isBlind'),
                'post_id': comment.get('postId'),
                'created_at': comment.get('createdAt'),
                'updated_at': comment.get('updatedAt')
            }
            comment_obj = Comment(**kwargs)
            comments.append(comment_obj)

    return comments


def create_media_object(media_info: dict):
    """Creates and returns a media object"""
    return Media(**media_info)
