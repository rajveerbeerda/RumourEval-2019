import json
import os
import csv
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import preprocessor as p

path = "rumoureval-2019-test-data/twitter-en-test-data"
main_dir = os.listdir(path)

# lst_a = ["support", "query", "deny", "comment"]
# lst_b = ["true", "false", "unverified"]

with open('twitter_test_dataset.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    header = ['type', 'id', 'text', 'favorite_count', 'retweet_count']
    writer.writerow(header)

    for dirs in main_dir:
        print(10 * "- - ", dirs, 10 * "- - ")
        dir = os.path.join(path, dirs)
        sub_dir = os.listdir(dir)
        for source_id in sub_dir:
            source_tweet = os.path.join(dir, source_id, "source-tweet", source_id + ".json")
            with open(source_tweet) as json_file:
                data = json.load(json_file)

            row = ["source", str(data['id']), p.clean(str(data['text'])), data['favorite_count'], data['retweet_count']]
            writer.writerow(row)

            replies = os.path.join(dir, source_id, "replies")
            replies_dir = os.listdir(replies)

            for reply in replies_dir:
                tweet = os.path.join(replies, reply)
                reply_id = str(reply)[:-5]

                with open(tweet) as json_file:
                    data = json.load(json_file)
                row = ["reply", str(data['id']), p.clean(str(data['text'])), data['favorite_count'],
                       data['retweet_count']]
                writer.writerow(row)
