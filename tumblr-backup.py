import json
import os
import urllib2

def get_api_json(url, api_key):
    url = 'http://api.tumblr.com/v2/blog/' + url + '/posts?api_key=' + api_key
    return urllib2.urlopen(url).read()

def get_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return json.loads(open(script_dir + '/config.json').read())

if __name__ == '__main__':
    config = get_config()
    api_json = get_api_json(config['url'], config['api_key'])
    json_obj = json.loads(api_json)
    total = json_obj['response']['total_posts']
    print total
