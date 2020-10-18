import logging
import time
import random

import chromedriver_binary  # noqa: F401
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select


class TdsystemCrawler:
    def __init__(self, headless: bool = True):
        self.root = "https://www.tdsystem.co.jp/"
        self.driver = Chrome(options=self.__get_options(headless))
        self.driver.implicitly_wait(5)
        self.driver.set_page_load_timeout(180)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()

    def get_root(self):
        self.driver.get(self.root)

    def __get_options(self, headless: bool):
        options = Options()
        if headless:
            options.add_argument("--headless")
        return options

    def __get_wait_secs(self):
        max_wait = 5.0
        min_wait = 1.0
        mean = 3.0
        sigma = 1.0
        return min([max_wait, max([min_wait, random.normalvariate(mean, sigma)])])

    def _get_meet_result_buttons(self, year: str):
        self.get_root()
        select_years = Select(self.driver.find_element_by_id("category"))
        select_years.select_by_value(year)
        time.sleep(self.__get_wait_secs())

        select_months = Select(self.driver.find_element_by_name("M"))
        select_months.select_by_value("0")  # 1~12月
        time.sleep(self.__get_wait_secs())
        return self.driver.find_elements_by_xpath("//button[text() = '結果']")

    def crawl_years(self, years: list[str]):
        logger = logging.getLogger(__file__)
        for y in years:
            logger.info(f"crawl_years: {y}")

            buttons = self._get_meet_result_buttons(y)
            num_of_meets = len(buttons)
            logger.info(f"num_of_meets = {num_of_meets}")

            # Traverse all meet results in this year
            for i in [11, 14]:  # TODO test code
                buttons = self._get_meet_result_buttons(y)
                buttons[i].click()
                logger.info(f"Open: {self.driver.current_url}")
                time.sleep(self.__get_wait_secs())
                self.driver.back()

        return


def set_logger(name: str, level: int = logging.INFO):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)


def main():
    set_logger(__file__)
    years = ["2019"]
    with TdsystemCrawler() as crawler:
        crawler.crawl_years(years)


if __name__ == "__main__":
    main()
