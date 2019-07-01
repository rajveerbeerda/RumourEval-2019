import json
import os
import csv
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import preprocessor as p

path = "rumoureval-2019-test-data/reddit-test-data"
main_dir = os.listdir(path)

with open('reddit_test_dataset.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    header = ['type', 'id', 'text', 'ups', 'downs']
    writer.writerow(header)

    for source_id in sorted(main_dir):
        print(10 * "- - ", source_id, 10 * "- - ")
        source_tweet = os.path.join(path, source_id, "source-tweet", source_id + ".json")
        with open(source_tweet) as json_file:
            d = json.load(json_file)
            data = d['data']['children'][0]['data']

        row = ["source", data['id'], p.clean(str(data['title'])), data['ups'], data['downs']]
        writer.writerow(row)

        replies = os.path.join(path, source_id, "replies")
        replies_dir = sorted(os.listdir(replies))

        for reply in replies_dir[:]:
            tweet = os.path.join(replies, reply)
            reply_id = str(reply)[:-5]

            with open(tweet) as json_file:
                d = json.load(json_file)
                data = d['data']

            if 'body' in data:
                row = ["reply", str(data['id']), p.clean(data['body'].encode("utf-8").replace("\\", " ").replace("("," ").replace(")", " ")), data['ups'],data['downs']]
                writer.writerow(row)
            while 'replies' in data and str(data['replies']) !="":
                if 'replies' in data:
                    data = data['replies']['data']['children'][0]['data']
                    print data['id']
                    if 'body' in data:
                        row = ["reply", str(data['id']), p.clean(data['body'].encode("utf-8").replace("\\", " ").replace("("," ").replace(")", " ")), data['ups'],data['downs']]
                        writer.writerow(row)
                else:
                    break
