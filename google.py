import logging

from patchright.sync_api import sync_playwright
import urllib.request

from const import PROXY_SETTINGS

DEBUG = False
logger = logging.getLogger(__name__)


class GoogleAd:

    @staticmethod
    def get_ad_stats(google_ad: str):
        with sync_playwright() as p:
            browser = p.chromium.launch(proxy=PROXY_SETTINGS, headless=False)
            page = browser.new_page()
            page.goto(google_ad)
            if DEBUG:
                logger.info(page.content())
            page.get_by_text("See all ads").click()
            domain_title = page.locator('.domain-title').inner_text()
            ads_count = page.locator('.ads-count').inner_text().replace(' ads', '').replace('k', '000')
            advertiser_name = page.locator('.advertiser-name').first.inner_text()
            number_of_creatives = page.locator('priority-creative-grid creative-preview').count()

            result = {
                'domain': domain_title,
                'advertiserName': advertiser_name,
                'runningAds': ads_count,
                'returnedCreatives': number_of_creatives,
            }
            print(result)
            return result

    @staticmethod
    def get_all_creatives(google_ad: str):
        with sync_playwright() as p:
            browser = p.chromium.launch(proxy=PROXY_SETTINGS, headless=False)
            page = browser.new_page()
            page.goto(google_ad)
            page.get_by_text("See all ads").click()

            images = page.locator('priority-creative-grid creative-preview').locator("img").all()
            src_list = [img.get_attribute("src") for img in images]
            return src_list

    @staticmethod
    def download_creatives(google_ad: str):
        with sync_playwright() as p:
            browser = p.chromium.launch(proxy=PROXY_SETTINGS, headless=False)
            page = browser.new_page()
            page.goto(google_ad)
            page.get_by_text("See all ads").click()

            images = page.locator('priority-creative-grid creative-preview').locator("img").all()
            src_list = [img.get_attribute("src") for img in images]
            for url in src_list:
                file_name = url.split("/")[-1] + ".jpg"
                print("will download " + file_name)
                urllib.request.urlretrieve(url, file_name)
