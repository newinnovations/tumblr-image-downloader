#!/usr/bin/env python3

# Tumblr image downloader
#
# Copyright (c) 2024 Martin van der Werff <github (at) newinnovations.nl>

import json
import os
import shutil
import sys
import time

import pytumblr
import requests


def image(blog, media, timestamp):
    image_dir = CONFIG["dir"]
    url = media["url"]
    s = url.split("/")
    if len(s) == 7:
        ext = s[6].rsplit(".", 1)[-1]
        filename = f"{blog}/{s[3]}.{ext}"
        path = f"{image_dir}/{filename}"
        if os.path.isfile(path):
            print(f"  -- {filename}: exists")
        else:
            try:
                response = requests.get(url, stream=True)
                with open(path, "wb") as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                print(f"  -- {filename}: ok")
            except KeyboardInterrupt:
                print()
                print(f"Shutdown requested...exiting (first removing {path})")
                try:
                    os.remove(path)
                    print("-- done")
                except Exception as e:
                    print(f"-- {e}")
                sys.exit(1)
            except Exception:
                print(f"  -- {filename}: error")

        os.utime(path, (timestamp, timestamp))
    else:
        print(f"Unexpected URL: len={len(s)}, url={url}")


def main():
    global CONFIG

    config_file = "tumblr.json" if len(sys.argv) < 2 else sys.argv[1]

    with open(config_file, "r") as f:
        CONFIG = json.load(f)

    client = pytumblr.TumblrRestClient(
        CONFIG["auth"]["consumer_key"],
        CONFIG["auth"]["consumer_secret"],
        CONFIG["auth"]["oauth_token"],
        CONFIG["auth"]["oauth_secret"],
    )

    image_dir = CONFIG["dir"]
    if not os.path.isdir(image_dir):
        print(f"Directory {image_dir} does not exist")
        return

    for blogname in CONFIG["blogs"]:

        if not os.path.isdir(f"{image_dir}/{blogname}"):
            os.mkdir(f"{image_dir}/{blogname}")

        offset = 0
        while True:
            print(blogname)

            res = client.posts(blogname, offset=offset, limit=50, npf=True)

            if "errors" in res:
                print(json.dumps(res, indent=2))
                return

            print(f"-- offset  = {offset}")
            if "blog" in res:
                updated = time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(res["blog"]["updated"])
                )
                print(f"-- nsfw    = {res['blog']['is_nsfw']}")
                print(f"-- posts   = {res['blog']['total_posts']}")
                print(f"-- updated = {updated}")

            if not res["posts"]:
                break

            blog_done = False

            for post in res["posts"]:
                assert post["type"] == "blocks"
                date = post["date"]
                timestamp = post["timestamp"]
                age = (time.time() - timestamp) / 86400
                print(f"* {date} (age={age:.1f} days)")

                if CONFIG["max_age"] > 0 and age > CONFIG["max_age"]:
                    print(f"> Post older than {CONFIG['max_age']} days, blog done <")
                    blog_done = True
                    break

                for c in post["content"]:
                    if c["type"] == "image":
                        image(blogname, c["media"][0], timestamp)
                    else:
                        print(f"  -- {c['type']}")

            if blog_done:
                break

            offset += len(res["posts"])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("Shutdown requested...exiting")
        sys.exit(1)
