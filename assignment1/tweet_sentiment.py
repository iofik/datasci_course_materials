import json
import re
import sys

def warning(text):
    print >>sys.stderr, "WARNING:", text

def load_sent(fname):
    with open(fname) as f:
        entries = (l.split('\t') for l in f)
        return dict((w,int(s)) for (w,s) in entries)

def evaluate_tweet(sent_dict, tweet):
    text = json.loads(tweet).get('text', '')
    words = re.finditer('\w+', text)
    return sum(sent_dict.get(w.group().lower(), 0) for w in words)

def main():
    sent_dict = load_sent(sys.argv[1])
    with open(sys.argv[2]) as f:
        sent_scores = (evaluate_tweet(sent_dict, l) for l in f)
        print '\n'.join(map(str, sent_scores))

if __name__ == '__main__':
    main()
