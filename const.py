import os

from playwright._impl._api_structures import ProxySettings

PROXY_SETTINGS: ProxySettings = {
    "server": os.getenv("SERVER"),
    "username": os.getenv("USERNAME"),
    "password": os.getenv("PASSWORD")
}
