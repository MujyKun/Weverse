from asyncio import iscoroutinefunction
from functools import wraps
from . import models

from .error import InvalidToken, PageNotFound, BeingRateLimited, LoginFailed, InvalidCredentials, NoHookFound
from .objects import create_tab_objects, create_community_objects, create_comment_objects, create_notification_objects,\
    create_media_object, create_post_objects, create_artist_objects, create_photo_objects, \
    iterate_community_media_categories, create_announcement_object

__title__ = 'Weverse'
__author__ = 'MujyKun'
__license__ = 'MIT'
__version__ = '1.0.8'


def check_expired_token(func):
    """Decorator to reinstate a token if it is expired."""

    @wraps(func)
    async def wrap_async_function(self=None, *args, **kwargs):
        if self._expired_token:
            if self._refresh_token_exists:
                await self._refresh_token()
            else:
                if self._login_info_exists:
                    await self._try_login()
                    await self._wait_for_login()  # wait for login or an exception to occur.

        return await func(self, *args, **kwargs)

    @wraps(func)
    def wrap_sync_function(self=None, *args, **kwargs):
        if self._expired_token:
            if self._refresh_token_exists:
                self._refresh_token()
            else:
                if self._login_info_exists:
                    self._try_login()
        return func(self, *args, **kwargs)
    return wrap_sync_function if not iscoroutinefunction(func) else wrap_async_function


from .weverseclient import WeverseClient
from .weversesync import WeverseClientSync
from .weverseasync import WeverseClientAsync
