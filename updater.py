#!/usr/bin/env python

import contextlib
import json
import os
import sys
import urllib.request

URL = "https://www.archlinux.org/mirrors/status/json/"


def main():
    DATA = load_data(URL)

    synced_urls = set()
    for encapsulated_data in DATA["urls"]:
        if is_valid(encapsulated_data):
            synced_urls.add(f"Server = {encapsulated_data['url']}$repo/os/$arch\n")

    with open("/etc/pacman.d/mirrorlist", "w") as mirror_file:
        for mirror_url in synced_urls:
            mirror_file.write(mirror_url)


def is_platform_linux() -> bool:
    """
    Check if the running platform is linux.

    Returns
    -------
    bool
        True if the running platform is linux.
    """
    return "linux" in sys.platform


def is_valid(url_info: dict) -> bool:
    """
    Check if the tested dict is up to standarts.

    Which means that the values for the specific keys are:

    protocol: 'https'
    completion_pct: 1
    active: True

    Parameters
    ----------
    url_info : dict
        Dict mapping:
        - url : str
        - protocol : {'http', 'https', 'rsync'}
        - last_sync : datetime
        - completion_pct : float
        - delay : int
        - duration_avg : float
        - duration_stddev : float
        - score : float
        - active : bool
        - country : str
        - country_code : str
        - isos : bool
        - ipv4 : bool
        - ipv6 : bool
        - details : str

    Returns
    -------
    bool
        True if all the checks are passed.
    """
    if url_info["protocol"] != "https":
        return False
    if url_info["completion_pct"] != 1:
        return False
    if not url_info["active"]:
        return False
    return True


def load_data(url: str) -> dict:
    """
    Load json data from a given URL.

    Parameters
    ----------
    url : str
        URL to fetch data from.

    Returns
    -------
    dict
    """
    with contextlib.closing(urllib.request.urlopen(url)) as url_data:
        data = json.loads(url_data.read().decode())
    return data


if __name__ == "__main__":
    if is_platform_linux():
        assert os.geteuid() == 0, "Must run as root"
    sys.exit(main())
