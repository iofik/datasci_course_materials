import json
import re
import sys

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

state_codes = dict((v,k) for (k,v) in states.iteritems())

def load_sent(fname):
    with open(fname) as f:
        entries = (l.split('\t') for l in f)
        return dict((w,int(s)) for (w,s) in entries)

def evaluate_words(sent_dict, words):
    return sum(sent_dict.get(w, 0) for w in words)

def extract_words(text):
    words = re.finditer('\w+', text)
    return (w.group().lower() for w in words)

def main():
    sent_dict = load_sent(sys.argv[1])
    score_count = {}
    with open(sys.argv[2]) as f:
        for tweet in f:
            js = json.loads(tweet)

            place = js.get('place', None)
            if not place:
                continue

            country, country_code = place.get('country', None), place.get('country_code', None)
            if country != "United States" and country_code != "US":
                continue

            full_name = place.get('full_name', '')
            match = re.search('^([\w ]+), *USA$', full_name)
            if match:
                state_code = state_codes.get(match.group(1), None)
                if not state_code:
                    continue
            else:
                match = re.search(', *([A-Z]{2})$', full_name)
                state_code = match.group(1)
                if state_code not in states:
                    continue

            tweets_words = extract_words(js.get('text', ''))
            score, count = score_count.get(state_code, (0, 0))
            score_count[state_code] = (score + evaluate_words(sent_dict, tweets_words), count + 1)

    best_score = -1e9;
    best_state = ''

    for (state,sc) in score_count.iteritems():
        score = float(sc[0]) / sc[1]
        if score > best_score:
            best_score = score
            best_state = state

    print best_state

if __name__ == '__main__':
    main()
