from typing import Optional, TYPE_CHECKING
import aiohttp

if TYPE_CHECKING:
    from Weverse.models import Post


class Video:
    r"""A Video object that represents a Weverse Video that belongs to media or a post.

    It is not suggested to create a Video manually, but rather through the
    following method: :class:`Weverse.objects.create_video_objects`

    The information retrieved on a Video is directly from the Weverse API and altered to fit this class.

    Videos do not have unique IDs.

    .. container:: operations

        .. describe:: x == y

            Check if the Video URL and Post are the same.

        .. describe:: x != y

            Check if the Video objects are not equal.

        .. describe:: str(x)

            Returns the Video URL.

        .. describe:: len(x)

            Returns the length of the video in seconds.

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
    playtime: int
        Duration of the video in seconds.
    post: Optional[Post]
        The Post Object the video belongs to.
    """
    def __init__(self, **kwargs):
        self.video_url = kwargs.get('video_url')
        self.thumbnail_url = kwargs.get('thumbnail_url')
        self.thumbnail_width = kwargs.get('thumbnail_width')
        self.thumbnail_height = kwargs.get('thumbnail_height')
        self.length = kwargs.get('playtime')
        self.post: Optional[Post] = None
        self.community_id: Optional[int] = kwargs.get('community_id')

    def __eq__(self, other):
        """Check if the Video URL and Post are the same."""
        if not isinstance(other, Video):
            return NotImplemented

        video_url_check = self.video_url == other.video_url
        if other.post and self.post:
            return video_url_check and (self.post == other.post)
        return video_url_check

    def __ne__(self, other):
        """Check if the Video objects are not equal."""
        return not self == other

    def __str__(self):
        """Returns the Video URL."""
        return f"{self.video_url}"

    def __len__(self):
        """Returns the length of the video in seconds."""
        return self.length


class VideoStream(Video):
    """
    A video stream that inherits from :ref:`Video`

    Attributes
    ----------
    hls_path: str
        Link to the .m3u8 file.
    dash_path: str
        Link to the .mpd file.
    content_index: int
        Index of the videos.
    video_id: int
        Unique Video ID
    encoding_status: str
        Encoding Status of the Video Stream.
    type: str
        The type of video it is.
    video_width: int
        The width of the video
    video_height: int
        The height of the video
    is_vertical: bool
        If the video is vertical.
    caption_s3_paths: List[str]
        A list of caption paths.
    level: str
        The users that are able to view the video.
    base_url: str
        The base url of the video to access files.
    m3u8_urls: str
        Several urls for the resolution m3u8 files.
    """
    def __init__(self, **kwargs):
        super(VideoStream, self).__init__(**kwargs)
        self.hls_path = kwargs.get('hlsPath')
        self.dash_path = kwargs.get('dashPath')
        self.content_index = kwargs.get("content_index")
        self.video_id = kwargs.get("video_id")
        self.encoding_status = kwargs.get("encoding_status")
        self.type = kwargs.get("type")
        self.video_width = kwargs.get("video_width")
        self.video_height = kwargs.get("video_height")
        self.is_vertical = kwargs.get("is_vertical")
        self.caption_s3_paths = kwargs.get("caption_s3_paths")
        self.level = kwargs.get("level")
        self.base_url = self.hls_path.replace("HLS.m3u8", "")
        self.m3u8_urls = [f"{self.base_url}HLS_{resolution}.m3u8" for resolution in [2560, 1440, 1080, 720, 540, 360]]
