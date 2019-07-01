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

path = "rumoureval-2019-training-data/reddit-training-data"
main_dir = os.listdir(path)

lst_a = ["support", "query", "deny", "comment"]
lst_b = ["true", "false", "unverified"]

with open('reddit_training_dataset.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    # header = ['type', 'id', 'text', 'ups', 'downs', 'label_a', 'label_b']
    # writer.writerow(header)

    for source_id in sorted(main_dir):
        print(10 * "- - ", source_id, 10 * "- - ")
        source_tweet = os.path.join(path, source_id, "source-tweet", source_id + ".json")
        with open(source_tweet) as json_file:
            d = json.load(json_file)
            data = d['data']['children'][0]['data']

        task_a = ""
        task_b = ""

        for i in train_key['subtaskaenglish']:
            if i == str(source_id):
                task_a = lst_a.index(train_key['subtaskaenglish'][i])

        for i in train_key['subtaskbenglish']:
            if i == str(source_id):
                task_b = lst_b.index(train_key['subtaskbenglish'][i])

        if task_a == "":
            for i in dev_key['subtaskaenglish']:
                if i == str(source_id):
                    task_a = lst_a.index(dev_key['subtaskaenglish'][i])

            for i in dev_key['subtaskbenglish']:
                if i == str(source_id):
                    task_b = lst_b.index(dev_key['subtaskbenglish'][i])

        row = ["source", data['id'], p.clean(str(data['title'])), data['ups'], data['downs'],
               task_a, task_b]
        writer.writerow(row)

        replies = os.path.join(path, source_id, "replies")
        replies_dir = sorted(os.listdir(replies))

        for reply in replies_dir[:]:
            tweet = os.path.join(replies, reply)
            reply_id = str(reply)[:-5]

            task_a = ""
            task_b = ""

            for i in train_key['subtaskaenglish']:
                if i == str(reply_id):
                    task_a = lst_a.index(train_key['subtaskaenglish'][i])

            if task_a == "":
                for i in dev_key['subtaskaenglish']:
                    if i == str(reply_id):
                        task_a = lst_a.index(dev_key['subtaskaenglish'][i])
            with open(tweet) as json_file:
                d = json.load(json_file)
                data = d['data']

            if 'body' in data:
                row = ["reply", str(data['id']), p.clean(data['body'].encode("utf-8").replace("\\", " ").replace("("," ").replace(")", " ")), data['ups'],data['downs'], task_a, task_b]
                writer.writerow(row)
            while 'replies' in data and str(data['replies']) !="":
                if 'replies' in data:
                    data = data['replies']['data']['children'][0]['data']
                    print data['id']
                    if 'body' in data:
                        row = ["reply", str(data['id']), p.clean(data['body'].encode("utf-8").replace("\\", " ").replace("("," ").replace(")", " ")), data['ups'],data['downs'], task_a, task_b]
                        writer.writerow(row)
                else:
                    break

path = "rumoureval-2019-training-data/reddit-dev-data"
main_dir = os.listdir(path)

with open('reddit_training_dataset.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)

    for source_id in sorted(main_dir):
        print(10 * "- - ", source_id, 10 * "- - ")
        source_tweet = os.path.join(path, source_id, "source-tweet", source_id + ".json")
        with open(source_tweet) as json_file:
            d = json.load(json_file)
            data = d['data']['children'][0]['data']

        task_a = ""
        task_b = ""

        for i in train_key['subtaskaenglish']:
            if i == str(source_id):
                task_a = lst_a.index(train_key['subtaskaenglish'][i])

        for i in train_key['subtaskbenglish']:
            if i == str(source_id):
                task_b = lst_b.index(train_key['subtaskbenglish'][i])

        if task_a == "":
            for i in dev_key['subtaskaenglish']:
                if i == str(source_id):
                    task_a = lst_a.index(dev_key['subtaskaenglish'][i])

            for i in dev_key['subtaskbenglish']:
                if i == str(source_id):
                    task_b = lst_b.index(dev_key['subtaskbenglish'][i])

        row = ["source", data['id'], p.clean(str(data['title'])), data['ups'], data['downs'],
               task_a, task_b]
        writer.writerow(row)

        replies = os.path.join(path, source_id, "replies")
        replies_dir = sorted(os.listdir(replies))

        for reply in replies_dir[:]:
            tweet = os.path.join(replies, reply)
            reply_id = str(reply)[:-5]

            task_a = ""
            task_b = ""

            for i in train_key['subtaskaenglish']:
                if i == str(reply_id):
                    task_a = lst_a.index(train_key['subtaskaenglish'][i])

            if task_a == "":
                for i in dev_key['subtaskaenglish']:
                    if i == str(reply_id):
                        task_a = lst_a.index(dev_key['subtaskaenglish'][i])
            with open(tweet) as json_file:
                d = json.load(json_file)
                data = d['data']

            if 'body' in data:
                row = ["reply", str(data['id']), p.clean(data['body'].encode("utf-8").replace("\\", " ").replace("("," ").replace(")", " ")), data['ups'],data['downs'], task_a, task_b]
                writer.writerow(row)
            while 'replies' in data and str(data['replies']) !="":
                if 'replies' in data:
                    data = data['replies']['data']['children'][0]['data']
                    print data['id']
                    if 'body' in data:
                        row = ["reply", str(data['id']), p.clean(data['body'].encode("utf-8").replace("\\", " ").replace("("," ").replace(")", " ")), data['ups'],data['downs'], task_a, task_b]
                        writer.writerow(row)
                else:
                    break
