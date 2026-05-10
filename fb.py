import logging
import re

from patchright.sync_api import sync_playwright
import urllib.request
from bs4 import BeautifulSoup

import html_to_json

from const import PROXY_SETTINGS

DEBUG = True
logger = logging.getLogger(__name__)


class FbAd:

    def __init__(self, slug: str):
        self.slug = slug

    def _matches_slug(self, advertiser_name: str) -> bool:
        return True

    def get_ad_stats(self, ad_link: str):
        with sync_playwright() as p:
            browser = p.chromium.launch(proxy=PROXY_SETTINGS, headless=False)
            page = browser.new_page()
            page.goto(ad_link, timeout=60000, wait_until='networkidle')

            grid_count = page.evaluate("""
                                       () => {
                                           const grids = [...document.querySelectorAll('div')]
                                               .filter(el => getComputedStyle(el).display === 'grid');
                                           const grid = grids[0];
                                           if (grid) {
                                               grid.setAttribute('data-ad-grid', 'true');
                                           }
                                           return grids.length;
                                       }
                                       """)
            print(f"Found {grid_count} grids")

            cards = page.locator("[data-ad-grid='true'] > *").all()
            print(f"Found {len(cards)} ad cards")

            ads = []
            for i, card in enumerate(cards):
                text = card.inner_text()

                if not re.search(r'^\s*Active\b', text, re.MULTILINE):
                    continue

                advertiser_name = re.search(r'\n([^\n]+)\n\s*Sponsored\b', text)
                advertiser_name = advertiser_name.group(1).strip() if advertiser_name else None

                library_id = re.search(r'Library ID:\s*(\S+)', text)
                started_running = re.search(r'Started running on\s+([^\n]+)', text)

                img_srcs = [
                    src for src in (img.get_attribute('src') for img in card.locator('img').all())
                    if src
                ]

                ad = {
                    'libraryId': library_id.group(1) if library_id else None,
                    'active': True,
                    'startedRunning': started_running.group(1).strip() if started_running else None,
                    'advertiserName': advertiser_name,
                    'imgSrcs': img_srcs[:2],
                }
                ads.append(ad)

            ads_count = page.get_by_text(re.compile('~.*result'))

            result = {
                'runningAds': ads_count.inner_text().replace('~', '').replace('result', '').replace('s', '').strip(),
                'activeAdsOnPage': len(ads),
                'ads': ads,
            }
            print(result)
            return result

    @staticmethod
    def get_all_creatives(google_ad: str):
        print("Not implemented")

    @staticmethod
    def download_creatives(google_ad: str):
        print("Not implemented")
