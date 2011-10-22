import json
import math
import os
import urllib2

def get_api_json(blog_url, api_key, limit = 20, offset = 0, page = 1):
    api_url = 'http://api.tumblr.com/v2/blog/{0}/posts?api_key={1}&limit={2}&offset={3}'
    api_url = api_url.format(blog_url, api_key, limit, offset)

    response = {}

    json_obj = json.loads(urllib2.urlopen(api_url).read())
    total = json_obj['response']['total_posts']

    if 0 == total:
        return False

    response['posts'] = json_obj['response']['posts']

    total_left = max(0, total - (page * limit))
    response['pages_left'] = math.ceil(float(total_left) / float(limit))

    return response

def get_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return json.loads(open(script_dir + '/config.json').read())

def reformat_list(posts):
    blacklist = ['format', 'note_count', 'post_url', 'reblog_key', 'date', 'blog_name']

    formatted = []
    for post in posts:
        core_post = {}
        for field in post.keys():
            if field in blacklist:
                continue
            core_post[field] = post[field]
        formatted.append(core_post)
    return formatted

if __name__ == '__main__':
    config = get_config()

    limit = 20
    offset = 0
    page = 0
    posts = []

    while True:
        api_json = get_api_json(config['url'], config['api_key'], limit, offset, page)

        if False == api_json:
            break

        posts.extend(api_json['posts'])

        if api_json['pages_left']:
            offset = int(api_json['pages_left'] * limit)
            page += 1
        else:
            break

    posts = reformat_list(posts)
    print json.dumps(posts, separators = (',', ':'))

