"""
Download all posts and metadata using the Tumblr API.

The blog domain and API key is read from config.json. See config-dist.json.
"""

import json
import math
import os
import urllib2

def get_api_json(blog_url, api_key, limit = 20, offset = 0, page = 1):
    """Return JSON of a paginated set of posts."""
    api_url = 'http://api.tumblr.com/v2/blog/{0}/posts?api_key={1}&limit={2}&offset={3}'
    api_url = api_url.format(blog_url, api_key, limit, offset)

    json_obj = json.loads(urllib2.urlopen(api_url).read())
    total = json_obj['response']['total_posts']

    if 0 == total:
        return False

    total_left = max(0, total - (page * limit))
    response = {}
    response['posts'] = json_obj['response']['posts']
    response['pages_left'] = math.ceil(float(total_left) / float(limit))
    return response

def get_config():
    """Return JSON of a paginated set of blog's posts."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return json.loads(open(script_dir + '/config.json').read())

def strip_metadata(posts, blacklist):
    """Return the post list stripped of specific metadata keys."""
    formatted = []
    for post in posts:
        core_post = {}
        for field in post.keys():
            if field in blacklist:
                continue
            core_post[field] = post[field]
        formatted.append(core_post)
    return formatted

def backup():
    """Download paginated posts and output them as JSON."""
    config = get_config()

    per_page = 20
    offset = 0
    cur_page = 0
    posts = []

    while True:
        api_json = get_api_json(config['url'], config['api_key'], per_page, offset, cur_page)

        if False == api_json:
            break

        posts.extend(api_json['posts'])

        if api_json['pages_left']:
            offset = int(api_json['pages_left'] * per_page)
            cur_page += 1
        else:
            break

    posts = strip_metadata(posts, config['strip_metadata'])
    print json.dumps(posts, separators = (',', ':'))

if __name__ == '__main__':
    backup()
