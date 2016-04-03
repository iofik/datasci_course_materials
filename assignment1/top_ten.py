import heapq
import json
import sys

from itertools import chain, ifilter

def extract_tweet_hashtags(tweet):
    hashtags = json.loads(tweet).get('entities', {}).get('hashtags', [])
    return ifilter(None, (h.get('text', None) for h in hashtags))

def main():
    count = {}
    with open(sys.argv[1]) as f:
        for tag in chain.from_iterable(extract_tweet_hashtags(l) for l in f):
            count[tag] = count.get(tag, 0) + 1
    top_ten = heapq.nlargest(10, count.iteritems(), lambda kv: kv[1])
    print '\n'.join('%s %d' % tc for tc in top_ten)

if __name__ == '__main__':
    main()
