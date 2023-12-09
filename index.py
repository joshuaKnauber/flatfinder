from crawlers.crawler import FlatResult
from crawlers.kleinanzeigen import KleinanzeigenCrawler

from notifications.email import send_email


results: list[FlatResult] = []

# run crawlers to fetch all reasonable flats (only doing sanity checks)
kleinanzeigen = KleinanzeigenCrawler(
    500, 1000, ["friedrichshain-kreuzberg", "koepenick"], 1, 28
)
results += kleinanzeigen.crawl()

# advanced filtering

# crosscheck?

# send notification
send_email("joshua.knauber@gmail.com", results)
