# Tumblr image downloader

This is a python script to download images from tumblr blogs.

## Configuration file

Configuration is provided using a JSON file named `tumblr.json` located in the current directory,
or using a file specified as an argument.

## Configuration format

```json
{
    "dir": "./images",
    "max_age": 10,
    "auth": {
        "consumer_key": "....",
        "consumer_secret": "....",
        "oauth_token": "....",
        "oauth_secret": "...."
    },
    "blogs": [
        "blog_name_1",
        "blog_name_2"
    ]
}
```

| key     | meaning                                                                    |
| ------- | -------------------------------------------------------------------------- |
| dir     | Directory to store the images. This directory must already exist.          |
| max_age | Only scan for posts younger than max_age (in days). Use 0 to download all. |
| auth    | Application keys for tumblr. See below.                                    |
| blogs   | Names of the blogs to download.                                            |

## Application keys

Register an application with tumblr to obtain the `consumer_key` and `consumer_secret`.

Use [https://api.tumblr.com/console/calls/user/info](https://api.tumblr.com/console/calls/user/info) to obtain `oauth_token` and `oauth_secret`.

## Requirements

You need to have `pytumblr` and `requests` installed. You can use `. activate` to create and activate a virtual environment with those requirements.
