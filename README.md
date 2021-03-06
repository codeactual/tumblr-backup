# tumblr-backup

Downloads post content and metadata using the Tumblr API.

# Usage

```python tumblrbackup.py > backup.json```

# Output

``` javascript
[
    {
        "body": "<p>Text body.</p>",
        "id": 11309083598,
        "tags": [],
        "timestamp": 1318313280,
        "title": "Text post",
        "type": "text"
    },
    {
        "id": 11084927889,
        "source": "Quote Author",
        "source_title": "quotesource.com",
        "source_url": "http://www.quotesource.com/",
        "tags": [
            "tag1",
            "tag2"
        ],
        "text": "Quote body.",
        "timestamp": 1317865857,
        "type": "quote"
    },
    ...
]
```

# Configuration

``` javascript
{
    "url": "my.tumblr.com",
    "api_key": "myApiKey",
    "strip_metadata": ["format", "note_count", "post_url", "reblog_key", "date", "blog_name"]
}
```


# Tests

```
cd test
python -m unittest discover
```
