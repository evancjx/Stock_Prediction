
from .helper import datetime_convert_timezone, datetime_string_to_datetime 
from .text_preprocessing import TP

class DM(TP):
    tweet_created_at_format = '%a %b %d %H:%M:%S %z %Y'
    to_tz = 'Asia/Singapore'

    def __init__(self, tokenizer=None, stop_words=()):
        super().__init__(stop_words=stop_words)

    def organize_tweet(self, tweet_json):
        text = tweet_json.get('retweeted_status').get('text') if 'retweeted_status' in tweet_json else tweet_json.get('text')
        
        tweet_entities = tweet_json.get('entities')
        urls = [
            url.get('url')
            for url in tweet_entities.get('urls', [])+
            tweet_entities.get('media', [])+
            tweet_json.get('extended_entities', {}).get('media', []) 
        ] + [
            url.get('url')
            for url in 
            (
                tweet_json.get('retweeted_status')
                .get('entities', {})
                .get('urls', []) 
                if tweet_json.get('retweeted_status') 
                else []
            )
        ]
        user_mentions = [
            (user_mention.get('screen_name'), user_mention.get('name'))
            for user_mention in tweet_entities.get('user_mentions')
        ]
        text_cleaned = self.clean_tweet(text, urls, user_mentions)
        polarity, subjectivity = self.text_sentiment(text_cleaned)

        return {
            'id': tweet_json.get('id_str'),
            'created_at': datetime_convert_timezone(
                datetime_string_to_datetime(
                    tweet_json.get('created_at'), self.tweet_created_at_format
                ), self.to_tz
            ),
            'source': tweet_json.get('source'),
            'original_text': text,
            'clean_text': text_cleaned,
            'polarity': polarity,
            'subjectivity': subjectivity,
            'lang': tweet_json.get('lang'),
            'favorite_count': tweet_json.get('favorite_count'),
            'retweet_count': tweet_json.get('retweet_count'),
            'original_author': tweet_json.get('user', {}).get('screen_name', ''),
            'possibly_sensitive': tweet_json.get('possibly_sensitive'),
            'hashtags': ', '.join([
                hashtags.get('text')
                for hashtags in tweet_entities.get('hashtags', [])
            ]),
            'mentions': ', '.join([
                mention[0]
                for mention in user_mentions
            ]),
            'location': tweet_json.get('location', '')
        }