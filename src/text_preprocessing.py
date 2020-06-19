
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from spacy.lang.en.stop_words import STOP_WORDS
from textblob import TextBlob
import re
import string

STOP_WORDS = STOP_WORDS | set(stopwords.words('english'))

#HappyEmoticons
emoticons_happy = set(
    [
        ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
        ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
        '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
        'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
        '<3'
    ]
)

# Sad Emoticons
emoticons_sad = set(
    [
        ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
        ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
        ':c', ':{', '>:\\', ';('
    ]
)

emoticons = emoticons_happy.union(emoticons_sad)

#Emoji patterns
emoji_pattern = re.compile(
    "["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    u"\U00002702-\U000027B0"
    u"\U000024C2-\U0001F251"
    "]+", 
    flags=re.UNICODE
)

def clean_tweet(tweet, urls):
    for url in urls:
        tweet = tweet.replace(url, '')
    
    tweet = re.sub(r':', '', tweet)
    tweet = re.sub(r'‚Ä¶', '', tweet)
    #replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)

    #remove emojis from tweet
    tweet = emoji_pattern.sub(r'', tweet)

    return ' '.join(
        [
            w 
            for w in nltk.word_tokenize(tweet) 
            if not w in STOP_WORDS and w not in emoticons and w not in string.punctuation
        ]
    )

def text_sentiment(text):
    text_sentiment = TextBlob(text).sentiment
    return text_sentiment.polarity, text_sentiment.subjectivity