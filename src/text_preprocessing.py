
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from spacy.lang.en.stop_words import STOP_WORDS
from textblob import TextBlob
import re
import string

class TP:
    def __init__(self, tokenizer=nltk.word_tokenize, stop_words=()):
        self.tokenizer = tokenizer
        self.STOP_WORDS = STOP_WORDS | set(stopwords.words('english')) | set(stop_words)

        #HappyEmoticons
        self.emoticons_happy = set(
            [
                ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
                ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
                '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
                'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
                '<3'
            ]
        )

        # Sad Emoticons
        self.emoticons_sad = set(
            [
                ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
                ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
                ':c', ':{', '>:\\', ';('
            ]
        )

        self.emoticons = self.emoticons_happy.union(self.emoticons_sad)

        #Emoji patterns
        self.emoji_pattern = re.compile(
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

        #string.punctuation
        punctuation = list(string.punctuation)
        punctuation.remove('$')
        self.punctuation_pattern = re.compile(
            r'['+''.join(punctuation)+']'
        )

    def clean_tweet(self, tweet, urls=[], user_mentions=[]):
        for entities in urls:
            if not entities: continue
            tweet = tweet.replace(entities, '')
        
        for entities in user_mentions:
            if not entities: continue
            tweet = tweet.replace(*entities)
        
        tweet = re.sub(r':', '', tweet)
        tweet = re.sub(r'‚Ä¶', '', tweet)
        #replace consecutive non-ASCII characters with a space
        tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)

        #remove emojis from tweet
        tweet = self.emoji_pattern.sub(r'', tweet)

        #remove punctuation from tweet
        tweet = self.punctuation_pattern.sub(r'', tweet)

        return ' '.join(
            [
                w 
                for w in self.tokenizer(tweet) 
                if not w in self.STOP_WORDS and w not in self.emoticons
            ]
        )

    def text_sentiment(self, text):
        text_sentiment = TextBlob(text).sentiment
        return text_sentiment.polarity, text_sentiment.subjectivity
    