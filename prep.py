#!/usr/bin/env python3

import json
import os
import pprint
import re

from urllib.request import urlopen

PP = pprint.PrettyPrinter()

REPO="open-watcom/open-watcom-v2"
URL=f"https://api.github.com/repos/{REPO}/releases"
CACHE_FILE="seen-releases.json"

# Used in when runing under github actions
OUTPUT=os.environ.get('GITHUB_OUTPUT', 'out.txt')

# File name for the full snapshot.
SNAPSHOT=re.compile('ow-snapshot.tar.xz')

def find_snapshot(asset_list):
    for asset in asset_list:
        if SNAPSHOT.match(asset['name']):
            # We need the updated at to compare to the list of releases
            # we've seen in the past.
            return asset['updated_at']

    return False

def get_all_releases():
    raw_release_list=urlopen(URL).read()
    release_list=json.loads(raw_release_list)


    return {
        release['tag_name']: find_snapshot(release['assets']) for release in release_list
    }

def get_seen_releases():
  
    try:
        with open(CACHE_FILE, 'r') as f:
            raw_seen_releases=f.read()
     
        return json.loads(raw_seen_releases)
    except Exception:
        return dict()

def write_list(file, release_list):
    with open(file, 'w') as f:
        json.dump(release_list, f)

def write_to_build(file, to_build_list):
    with open(file, 'w') as f:
        to_build=json.dumps(to_build_list)
        f.write(f"to_build={to_build}")
        
def filter_releases(all_release_list, seen_release_list):
    return [ k for k, v in all_release_list.items() if seen_release_list.get(k, False) != v and v != False ]

all_release_list = get_all_releases()
to_build_list = filter_releases(all_release_list, get_seen_releases())

print("Building list:")
PP.pprint(to_build_list)

write_list(CACHE_FILE, all_release_list)
write_to_build(OUTPUT, to_build_list)

