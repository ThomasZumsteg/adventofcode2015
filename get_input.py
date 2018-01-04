#!/usr/bin/env python3

import os
import requests

SESSION_KEY = "AOC_SESSION"
AOE_URL = "http://adventofcode.com"

def get_input(day, year):
    file_name = '.AoC-{:04}-{:02}.tmp'.format(year, day)
    try:
        with open(file_name, 'r') as f:
            return f.read()
    except FileNotFoundError:
        url = "{}/{}/day/{}/input".format(AOE_URL, year, day)
        r = requests.get(url, cookies=dict(session=os.environ.get(SESSION_KEY)))
        if not r.ok:
            raise RuntimeError("Could not get {}: {}: {}".format(url,
                r.status_code, r.reason))
        with open(file_name, 'w') as f:
            f.write(r.text)
        return r.text

def line_parser(text, parse=int, seperator='\n'):
    return [parse(item) for item in text.split(seperator) if item != '']
