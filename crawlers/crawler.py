from typing import TypedDict
from selenium import webdriver
from filters.sanity import sanity_check


class FlatResult(TypedDict):
    title: str
    description: str
    price: float
    adress: str
    url: str
    images: list[str]


class Driver:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)

    def __enter__(self):
        return self.driver

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.driver.close()


class Crawler:
    def __init__(self):
        pass

    def crawl(self) -> list[FlatResult]:
        """Run the crawler and return the sanity checked results"""
        results = self._get_results()
        results = self._sanity_check_results(results)
        return results

    def _get_results(self) -> list[FlatResult]:
        """Get the flat results from the crawler"""
        raise NotImplementedError

    def _sanity_check_results(self, results: list[FlatResult]):
        """Filter the flat results"""
        return [
            *filter(
                lambda result: sanity_check(
                    result["title"],
                    result["description"],
                ),
                results,
            )
        ]
