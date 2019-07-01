import json
import os
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import preprocessor as p

with open('rumoureval-2019-training-data/train-key.json') as json_file:
    train_key = json.load(json_file)

with open('rumoureval-2019-training-data/dev-key.json') as json_file:
    dev_key = json.load(json_file)

path = "rumoureval-2019-training-data/twitter-english"
main_dir = os.listdir(path)


lst_a = ["support", "query", "deny", "comment"]
lst_b = ["true", "false", "unverified"]

with open('twitter_training_dataset.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    header = ['type', 'id', 'text', 'favorite_count', 'retweet_count', 'label_a', 'label_b']
    writer.writerow(header)

    for dirs in main_dir:
        print(10 * "- - ", dirs, 10 * "- - ")
        dir = os.path.join(path, dirs)
        sub_dir = os.listdir(dir)
        for source_id in sub_dir:
            source_tweet = os.path.join(dir, source_id, "source-tweet", source_id + ".json")
            with open(source_tweet) as json_file:
                data = json.load(json_file)

            task_a = ""
            task_b = ""

            for i in train_key['subtaskaenglish']:
                if i==str(source_id):
                    task_a = lst_a.index(train_key['subtaskaenglish'][i])

            for i in train_key['subtaskbenglish']:
                if i==str(source_id):
                    task_b = lst_b.index(train_key['subtaskbenglish'][i])

            if task_a=="":
                for i in dev_key['subtaskaenglish']:
                    if i == str(source_id):
                        task_a = lst_a.index(dev_key['subtaskaenglish'][i])

                for i in dev_key['subtaskbenglish']:
                    if i == str(source_id):
                        task_b = lst_b.index(dev_key['subtaskbenglish'][i])

            row = ["source", str(data['id']), p.clean(str(data['text'])), data['favorite_count'], data['retweet_count'], task_a, task_b]
            writer.writerow(row)

            replies = os.path.join(dir, source_id, "replies")
            replies_dir = os.listdir(replies)
            
            for reply in replies_dir:
                tweet = os.path.join(replies, reply)
                reply_id = str(reply)[:-5]

                task_a = ""
                task_b = ""

                for i in train_key['subtaskaenglish']:
                    if i==str(reply_id):
                        task_a = lst_a.index(train_key['subtaskaenglish'][i])

                if task_a=="":
                    for i in dev_key['subtaskaenglish']:
                        if i == str(reply_id):
                            task_a = lst_a.index(dev_key['subtaskaenglish'][i])

                with open(tweet) as json_file:
                    data = json.load(json_file)
                row = ["reply", str(data['id']), p.clean(str(data['text'])), data['favorite_count'], data['retweet_count'], task_a, task_b]
                writer.writerow(row)
