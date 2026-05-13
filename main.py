from enum import Enum
import sys

from dotenv import load_dotenv

from fb import FbAd
from google import GoogleAd

load_dotenv()

import logging

logging.basicConfig(level=logging.DEBUG)


class AllowedAction(Enum):
    GET_STATS = '1'
    GET_CREATIVES = '2'
    DOWNLOAD_CREATIVES = '3'


class AllowedAdCenter(Enum):
    GOOGLE = 'google'
    FB = 'fb'


input_ad_center = AllowedAdCenter(sys.argv[1]) if len(sys.argv) > 1 else AllowedAdCenter.GOOGLE
input_search = sys.argv[2] if len(sys.argv) > 2 else "hoski.ca"
input_action = AllowedAction(sys.argv[3]) if len(sys.argv) > 3 else AllowedAction.GET_STATS

print(input_ad_center, input_search, input_action)


def scrape(ad_center: AllowedAdCenter, domain_name: str, action: AllowedAction):
    if ad_center == AllowedAdCenter.GOOGLE:
        ad_link = f"https://adstransparency.google.com?domain={domain_name}&hl=en&region=anywhere"
        ad_provider = GoogleAd

    if ad_center == AllowedAdCenter.FB:
        ad_link = f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&q={input_search}&search_type=keyword_unordered&sort_data[direction]=desc&sort_data[mode]=total_impressions&source=fb-logo"
        ad_provider = FbAd(slug=domain_name)

    if action == AllowedAction.GET_STATS:
        ad_provider.get_ad_stats(ad_link)

    elif action == AllowedAction.GET_CREATIVES:
        ad_provider.get_all_creatives(ad_link)

    elif action == AllowedAction.DOWNLOAD_CREATIVES:
        ad_provider.download_creatives(ad_link)


scrape(input_ad_center, input_search, input_action)
