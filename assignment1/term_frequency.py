import json
import re
import sys

from itertools import chain

def extract_tweet_words(tweet):
    text = json.loads(tweet).get('text', '')
    words = re.finditer('\w+', text)
    return (w.group().lower() for w in words)

def main():
    with open(sys.argv[1]) as f:
        tweets_words = [extract_tweet_words(l) for l in f]

    count = {}
    for word in chain(*tweets_words):
        count[word] = count.get(word, 0) + 1
    total_count = sum(count.itervalues()) + 0.
    print '\n'.join("%s %g"%(w,c/total_count) for (w,c) in count.iteritems())

if __name__ == '__main__':
    main()
