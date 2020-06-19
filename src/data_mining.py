
from .helper import datetime_convert_timezone, datetime_string_to_datetime 
from .text_preprocessing import clean_tweet, text_sentiment

tweet_created_at_format = '%a %b %d %H:%M:%S %z %Y'
to_tz = 'Asia/Singapore'

def organize_tweet(tweet_json):
    text = tweet_json.get('text')
    urls = [
        url.get('url')
        for url in tweet_json.get('entities', {'urls': []}).get('urls', [])+
        tweet_json.get('entities', {'media': []}).get('media', [])+
        tweet_json.get('extended_entities', {'media': []}).get('media', [])
    ]
    text_cleaned = clean_tweet(text, urls)
    polarity, subjectivity = text_sentiment(text_cleaned)

    return {
        'id': tweet_json.get('id_str'),
        'created_at': datetime_convert_timezone(
            datetime_string_to_datetime(
                tweet_json.get('created_at'), tweet_created_at_format
            ), to_tz
        ),
        'source': tweet_json.get('source'),
        'original_text': text,
        'clean_text': text_cleaned,
        'polarity': polarity,
        'subjectivity': subjectivity,
        'lang': tweet_json.get('lang'),
        'favorite_count': tweet_json.get('favorite_count'),
        'retweet_count': tweet_json.get('retweet_count'),
        'original_author': tweet_json.get('user', {'screen_name': None}).get('screen_name'),
        'possibly_sensitive': tweet_json.get('possibly_sensitive'),
        'hashtags': ', '.join([
            hashtags.get('text')
            for hashtags in tweet_json.get('entities', {'hashtags': []}).get('hashtags', [])
        ]),
        'mentions': ', '.join(tweet_json.get('entities', {'user_mentions': []}).get('user_metions', [])),
        'location': tweet_json.get('location', '')
    }