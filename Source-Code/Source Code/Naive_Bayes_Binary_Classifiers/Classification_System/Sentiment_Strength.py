import os
import json
from subprocess import Popen, PIPE, STDOUT

REVIEW_DIR = '/home/gijs/Documents/ReplicationSA/PaperReplication/app-stores-scraper/reviews/'


def get_text_sentiment(text):
    p = Popen(['java', '-jar', 'SentiStrength.jar', 'sentidata',
               'SentStrength_Data/', 'text', text], stdout=PIPE,
              stderr=STDOUT)

    for line in p.stdout:  # Should be just one line though
        if len(line) > 0:
            sentilist = str.split(line)
            pos = int(sentilist[0])
            neg = int(sentilist[1])

            sentiscore = neg if abs(neg) >= pos else pos
            return sentiscore, pos, neg


"""Output Sentiment score to CSV file in format:
    SOURCEFILE_NAME|REVIEW_ID, SENTISCORE, POSITIVE SENTIMENT SCORE, NEGATIVE SENTIMENT SCORE
"""
def write_to_file(filename, ID, sentiscore, pos, neg):
    with open("Sentiscores_CSV", "a") as f:
        f.write("{0}|{1},{2},{3},{4}\r\n".format(filename, ID, sentiscore, pos,
                                                 neg))

for filename in os.listdir(REVIEW_DIR):
    with open(os.path.join(REVIEW_DIR, filename), "r") as f:
        data = json.load(f)
        for reviewdict in data:
            text = "{0} {1}".format(reviewdict['title'].encode('utf-8'),
                                    reviewdict['comment'].encode('utf-8'))
            sentiscore, pos, neg = get_text_sentiment(text)
            write_to_file(filename, reviewdict['id'], sentiscore, pos, neg)
