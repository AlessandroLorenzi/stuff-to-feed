from src.telegram import TelegramParser

def test_telegram_parser():
    # Create an instance of TelegramParser with a mock channel ID
    channel_id = "podcastconsiglidiascolto"
    parser = TelegramParser(channel_id)

    # Call the parser
    rss_feed = parser()

    # Check if the feed title is set correctly
    assert "Podcast 🎧 Consigli di Ascolto" == parser.feed.title
    assert "Che podcast ascolto oggi?" in parser.feed.description
    # Check if the RSS feed is not empty
    assert rss_feed is not None