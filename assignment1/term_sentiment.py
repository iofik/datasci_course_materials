import json
import re
import sys

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
        tweets_words = [extract_tweet_words(l) for l in f]

    score_count = {}
    for words in tweets_words:
        words = list(words)
        tweet_score = evaluate_words(sent_dict, words)
        known_words = len(filter(sent_dict.has_key, words))
        ave_score = tweet_score / (known_words + 1e-8)
        for word in words:
            if word not in sent_dict:
                score, count = score_count.get(word, (0, 0))
                score_count[word] = (score+ave_score, count+1)

    print '\n'.join("%s %g"%(w,sc[0]/sc[1]) for (w,sc) in score_count.iteritems())

if __name__ == '__main__':
    main()
