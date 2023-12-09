from selenium.webdriver.common.by import By
from crawlers.crawler import Crawler, Driver, FlatResult
from filters.sanity import check_title


# TODO do this better
KLEINANZEIGEN_AREAS = {
    "friedrichshain-kreuzberg": "c203l26918",
    "koepenick": "c203l3360",
}


class KleinanzeigenCrawler(Crawler):
    def __init__(
        self,
        price_min: int,
        price_max: int,
        areas: list[str],
        rooms_min: int,
        area_min: int,
    ):
        self.price_min = price_min
        self.price_max = price_max
        self.areas = areas
        self.rooms_min = rooms_min
        self.area_min = area_min

    def _url(self, area: str, page: int) -> str:
        global KLEINANZEIGEN_AREAS
        return (
            f"https://www.kleinanzeigen.de/s-wohnung-mieten/"
            + area
            + f"/preis:{self.price_min}:{self.price_max}"
            + f"/seite:{page}/{KLEINANZEIGEN_AREAS[area]}"
            + "+wohnung_mieten."
            + f"qm_d:{self.area_min}"
            + "%2C+wohnung_mieten.swap_s:nein+wohnung_mieten."
            + f"zimmer_d:{self.rooms_min}%2C"
        )

    def _get_results(self) -> list[FlatResult]:
        with Driver() as driver:
            for area in self.areas:
                page = 0
                hasNextPage = True
                urls: list[str] = []
                while hasNextPage:
                    page += 1
                    driver.get(self._url(area, page))
                    hasNextPage = (
                        driver.find_elements(By.CLASS_NAME, "pagination-next") != []
                    )

                    # get article elements
                    articles = driver.find_elements(By.TAG_NAME, "article")

                    # get articles urls
                    for article in articles:
                        headerElem = article.find_element(By.TAG_NAME, "h2")
                        linkElem = headerElem.find_element(By.TAG_NAME, "a")
                        title = linkElem.text.strip()
                        if check_title(title):
                            urls.append(linkElem.get_attribute("href"))

            print(f"Found {len(urls)} results. Crawling details...")

            # get details
            results: list[FlatResult] = []
            for i, url in enumerate(urls):
                print(
                    f"Crawling {i+1}/{len(urls)}, {(i+1)/len(urls)*100:.2f}% complete"
                )
                driver.get(url)

                title = driver.find_element(By.ID, "viewad-title").text.strip()
                priceText = (
                    driver.find_element(By.ID, "viewad-price")
                    .text.split(" ")[0]
                    .replace(".", "")
                )
                addressText = driver.find_element(By.ID, "viewad-title").text.strip()
                descriptionText = driver.find_element(
                    By.ID, "viewad-description-text"
                ).text.strip()

                imageUrls: list[str] = []
                imgContainers = driver.find_elements(By.CLASS_NAME, "ad-thumbs")
                if imgContainers:
                    images = imgContainers[0].find_elements(By.TAG_NAME, "img")
                    imageUrls = [*map(lambda img: img.get_attribute("src"), images)]

                results.append(
                    {
                        "url": url,
                        "title": title,
                        "adress": addressText,
                        "price": int(priceText),
                        "description": descriptionText,
                        "images": imageUrls,
                    }
                )

        return results
