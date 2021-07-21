import asyncio
import time
import aiohttp
from typing import Optional, List
from Weverse import WeverseClientAsync, InvalidToken, BeingRateLimited, models
from dotenv import load_dotenv
from os import getenv


"""
asynchronous.py


Asynchronous Examples for Weverse.

This file should be able to run if a token is supplied.
If you would like to view more specific information,
then it would be suggested to look at the API Docs at https://weverse.readthedocs.io/en/latest/ 
or run this file in a debugger.

In order to get a token: https://weverse.readthedocs.io/en/latest/api.html#get-account-token
In order to set a token, Rename .env.example to .env and set WEVERSE_AUTH to the token (recommended). 
You may also set the variable weverse_token to the token (not recommended).

If you are running in a Synchronous environment, go take a look at the Synchronous examples file.
"""


def get_formatted_time(seconds):
    """Turn seconds into days, hours, minutes, and seconds.

    Not related to Weverse.
    :param seconds: Amount of seconds to convert.
    """
    seconds = round(seconds)
    minute, sec = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)

    return f"{f'{day}d ' if day else ''}" \
           f"{f'{hour}h ' if hour else ''}" \
           f"{f'{minute}m ' if minute else ''}" \
           f"{f'{sec}s' if sec else ''}" \
           f"{f'0s' if seconds < 1 else ''}"


class Example:
    def __init__(self):
        self.weverse_client: Optional[WeverseClientAsync] = None

    async def check_new_notifications(self) -> Optional[List[models.Notification]]:
        """Check for new weverse notifications.

        This should be called in a loop to constantly check for notifications.
        """
        if not self.weverse_client.cache_loaded:
            # This is more of an issue with async, but we should always make sure the cache is loaded.
            return

        if not await self.weverse_client.check_new_user_notifications():
            # This will check if there are new notifications and will process them into objects for us.
            return

        # They should now be loaded into notification cache, but just to confirm nothing went wrong, we will check.
        if not self.weverse_client.user_notifications:
            return

        # We can now get the latest notifications
        # get_new_notifications is new in V1.0.3. Separates new notifications from older ones.
        latest_notifications = self.weverse_client.get_new_notifications()
        return latest_notifications

    async def start(self):
        """
        Managing Weverse Client and starting the notification loop.

        """
        load_dotenv()  # loads up .env in memory

        weverse_token = getenv("WEVERSE_AUTH") or "fake_token"

        web_session = aiohttp.ClientSession()  # create a web session for Weverse to use (Not needed, but recommended)

        client_kwargs = {
            "verbose": True,  # Will print warning messages for links that have failed to connect or were not found.
            "web_session": web_session,  # Existing web session
            "authorization": weverse_token,  # Auth Token to connect to Weverse
            "loop": asyncio.get_event_loop()  # current event loop
        }

        self.weverse_client = WeverseClientAsync(**client_kwargs)

        # start the client process.
        start_kwargs = {
            # Will load ALL followed community posts. If following majority communities, this will take
            # more than 10 minutes to complete. If you are not in need of OLDER posts, you can set it to False and
            # it should load within a few seconds.
            "create_old_posts": True,
            # Will load up the past 20 notifications. This is a quick process, so you may as well load them up.
            "create_notifications": True,
            # Will load ALL media posts. This will take a very long time if enabled.
            "create_media": True
        }

        # You can actually check if the token works before starting the cache process and receiving an exception.
        token_works = await self.weverse_client.check_token_works()

        try:
            print("Weverse cache is currently being created.")
            start_time = time.time()  # Start Time for Weverse Cache
            await self.weverse_client.start(**start_kwargs)  # start the client process to all needed data.
            end_time = time.time()  # The time when Weverse Cache has loaded.
            print(f"Weverse cache has loaded after {get_formatted_time(end_time - start_time)}")
        except InvalidToken:
            raise RuntimeError("An Invalid Token was passed in")
        except BeingRateLimited:
            raise RuntimeError("Weverse Client is being rate-limited.")  # Note that this issue has never occurred yet.
        except Exception as e:
            # No other specific exceptions are raised, But we shouldn't ignore any errors.
            raise RuntimeError(f"A different error has occurred. {e}")
        # We now have all of the data we would want to modify.

        # loop the notifications
        await self.loop_notifications()

    async def loop_notifications(self):
        """Check for notifications on a loop."""
        continue_loop = True
        while continue_loop:  # Just a warning that this would block if not under it's own task.
            # This is a loop running to check for notifications.

            new_notifications = await self.check_new_notifications()
            if not new_notifications:
                continue

            for new_notification in new_notifications:
                # Two ways to determine the community name.
                community_name = new_notification.community_name or new_notification.bold_element
                if not community_name:
                    # In the case a notification faults from Weverse, this is a safety measure.
                    continue

                # We do not know the type of notification it is because it is usually hidden inside the message.
                # The wrapper does not automatically check for this, so we must call the method.
                notification_type = self.weverse_client.determine_notification_type(new_notification.message)

                possible_notification_types = ["comment", "post", "media", "announcement"]

                # The content ID is the ID of the actual post we are looking for.
                content_id = new_notification.contents_id

                # In the below conditions, you should do any logic needed for knowing the types...
                if notification_type == possible_notification_types[0]:  # comment
                    comment = self.weverse_client.get_comment_by_id(content_id)
                    ...  # Do stuff with the comment here
                elif notification_type == possible_notification_types[1]:  # post
                    post = self.weverse_client.get_post_by_id(content_id)
                    ...  # Do stuff with the post here
                elif notification_type == possible_notification_types[2]:  # media
                    media = self.weverse_client.get_media_by_id(content_id)
                    ...  # Do stuff with the media here
                elif notification_type == possible_notification_types[3]:  # announcement
                    # Announcements are not currently stored in cache.
                    ...
                else:  # No Type Found (Perhaps a new type was created but wrapper is not updated)
                    print(f"{new_notification.id} has an unrecognized type.")

                ...  # do more stuff if you want to.
            continue_loop = False  # no longer want to check for notifications.


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Example().start())

    # Please note that if you are running Weverse in a huge program and you are loading the entire cache, this should
    # be run using asyncio.create_task
    # Assuming you will not be running the Weverse section from the main part (this function) of your program,
    # it would be advised to do something along the lines of the below line
    # task = asyncio.create_task(Example().start())

