import logging
import re

from playwright._impl._api_structures import ProxySettings
from patchright.sync_api import sync_playwright
import urllib.request

from const import PROXY_SETTINGS

DEBUG = True
logger = logging.getLogger(__name__)


class FbAd:

    @staticmethod
    def get_ad_stats(ad_link: str):
        with sync_playwright() as p:
            browser = p.chromium.launch(proxy=PROXY_SETTINGS, headless=False)
            page = browser.new_page()
            page.goto(ad_link, wait_until='networkidle')
            if DEBUG:
                logger.info(page.content())
            # page.get_by_text("See all ads").click()
            ads_count = page.get_by_text(re.compile('~.*result'))
            # advertiser_name = page.locator('.advertiser-name').first.inner_text()
            # number_of_creatives = page.locator('priority-creative-grid creative-preview').count()

            result = {
                # 'advertiserName': advertiser_name,
                'runningAds': ads_count.inner_text().replace('~', '').replace('result','').replace(),
                # 'returnedCreatives': number_of_creatives,
            }
            print(result)
            return result

    @staticmethod
    def get_all_creatives(google_ad: str):
        pass

    @staticmethod
    def download_creatives(google_ad: str):
        pass
