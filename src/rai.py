import requests
from datetime import datetime as dt
from urllib.parse import urljoin
from feedendum import Feed, FeedItem, to_rss_string
from itertools import chain


NSITUNES = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"


class RaiParser:
    baseurl = "https://www.raiplaysound.it/programmi/"

    def __init__(self, slug: str) -> None:
        self.url = self.baseurl + slug

    def __call__(self) -> str:
        response = requests.get(self.url + ".json")
        response.raise_for_status()
        rdata = response.json()

        feed = Feed()
        feed.title = rdata["title"]
        feed.description = rdata["podcast_info"].get("description", rdata["title"])
        feed.url = self.url
        feed._data["image"] = {"url": urljoin(self.url, rdata["podcast_info"]["image"])}
        feed._data[f"{NSITUNES}author"] = "RaiPlaySound"
        feed._data["language"] = "it-it"
        feed._data[f"{NSITUNES}owner"] = {
            f"{NSITUNES}email": "giuliomagnifico@gmail.com"
        }

        categories = {
            c["name"]
            for c in chain(
                rdata["podcast_info"]["genres"],
                rdata["podcast_info"]["subgenres"],
                rdata["podcast_info"]["dfp"].get("escaped_genres", []),
                rdata["podcast_info"]["dfp"].get("escaped_typology", []),
            )
        }

        feed._data[f"{NSITUNES}category"] = [{"@text": c} for c in sorted(categories)]
        feed.items = []

        cards = rdata["block"].get("cards", [])
        for item in cards:
            if not item.get("audio"):
                continue
            fitem = self._generate_feed_item(item)
            feed.items.append(fitem)

        feed.items.sort(key=lambda x: x.update, reverse=True)

        return to_rss_string(feed)

    def _generate_feed_item(self, item: dict) -> FeedItem:
        fitem = FeedItem()
        fitem.title = item["toptitle"]
        fitem.id = "giuliomagnifico-raiplay-feed-" + item["uniquename"]
        fitem.update = self._datetime_parser(
            item["track_info"].get("date", dt.now().isoformat())
        )
        fitem.url = urljoin(self.url, item["track_info"]["page_url"])
        fitem.content = item.get("description", item["title"])

        enclosure_url = item["audio"].get("url")
        if item.get("downloadable_audio", {}).get("url"):
            enclosure_url = item["downloadable_audio"]["url"].replace("http:", "https:")

        fitem._data = {
            "enclosure": {
                "@type": "audio/mpeg",
                "@url": urljoin(self.url, enclosure_url),
            },
            f"{NSITUNES}title": fitem.title,
            f"{NSITUNES}summary": fitem.content,
            f"{NSITUNES}duration": item["audio"]["duration"],
            "image": {"url": urljoin(self.url, item["image"])},
        }
        return fitem

    def _datetime_parser(self, s: str) -> dt:
        formats = [
            "%a, %d %b %Y %H:%M:%S %z",
            "%d/%m/%Y",
            "%d %b %Y",
            "%d-%m-%Y %H:%M:%S",
            "%Y-%m-%d",
        ]
        for fmt in formats:
            try:
                return dt.strptime(s, fmt)
            except ValueError:
                continue
        return dt.now()
