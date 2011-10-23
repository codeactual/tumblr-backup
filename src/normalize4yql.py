"""
Normalize backup JSON from https://github.com/codeactual/tumblr-backup
for use as a YQL input source. Matches Tumblr RSS tag names.
"""

import argparse
import json

def normalize(file):
    json_str = open(file).read()
    json_obj = json.loads(json_str)

    posts = []
    for raw_post in json_obj:
        normal_post = {}
        normal_post['pubDate'] = raw_post['timestamp']
        normal_post['tags'] =  raw_post['tags']

        if 'body' in raw_post:
            normal_post['description'] = raw_post['body']
        elif 'caption' in raw_post:
            normal_post['description'] = raw_post['caption']
        elif 'text' in raw_post:
            normal_post['description'] = raw_post['text']
        elif 'link' == raw_post['type']:
            normal_post['description'] = raw_post['title']

        if 'title' in raw_post:
            normal_post['title'] = raw_post['title']
        elif 'photo' == raw_post['type']:
            normal_post['title'] = raw_post['caption']

        posts.append(normal_post)
    return json.dumps(posts)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()
    print normalize(args.file)
