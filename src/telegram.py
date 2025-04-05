from telethon.sync import TelegramClient
import asyncio
from feedendum import Feed, FeedItem, to_rss_string
import os
from telethon.tl.functions.channels import GetFullChannelRequest

api_id = os.environ.get("TELEGRAM_API_ID")
api_hash = os.environ.get("TELEGRAM_API_HASH")


class TelegramParser:
    def __init__(self, channel_id: str) -> None:
        self.channel_id = channel_id
        self.feed = Feed()

    def __call__(self):
        self.feed.title =  self.channel_id

        try:
            print(f"Fetching messages from channel: {self.channel_id}")
            asyncio.run(self.fetch_messages())
        except Exception as e:
            print(f"An error occurred: {e}")

        return to_rss_string(self.feed)

    async def fetch_messages(self):
        async with TelegramClient("session_name", api_id, api_hash) as client:
            channel = await client.get_entity(self.channel_id)
            channel_full = await client(GetFullChannelRequest(channel=channel))
            self.feed.title = channel.title
            self.feed.description = channel_full.full_chat.about

            async for message in client.iter_messages(self.channel_id, limit=10):
                item = FeedItem()
                item.title = message.message.split("\n")[0]
                item.content = message.message

                self.feed.items.append(item)
