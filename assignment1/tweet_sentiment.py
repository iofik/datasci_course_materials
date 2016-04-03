import json
import re
import sys

def warning(text):
    print >>sys.stderr, "WARNING:", text

def load_sent(fname):
    with open(fname) as f:
        entries = (l.split('\t') for l in f)
        return dict((w,int(s)) for (w,s) in entries)

def evaluate_words(sent_dict, words):
    return sum(sent_dict.get(w, 0) for w in words)

def extract_tweet_words(tweet):
    text = json.loads(tweet).get('text', '')
    words = re.finditer('\w+', text)
    return (w.group().lower() for w in words)

def main():
    sent_dict = load_sent(sys.argv[1])
    with open(sys.argv[2]) as f:
        tweets_words = (extract_tweet_words(l) for l in f)
        sent_scores = (evaluate_words(sent_dict, w) for w in tweets_words)
        print '\n'.join(map(str, sent_scores))

if __name__ == '__main__':
    main()
