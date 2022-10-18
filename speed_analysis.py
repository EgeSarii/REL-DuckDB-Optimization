import json
import time
from REL.mention_detection import MentionDetection
from REL.utils import process_results
from REL.entity_disambiguation import EntityDisambiguation
from REL.ner import Cmns, load_flair_ner

def example_preprocessing(batch_size):
    # user does some stuff, which results in the format below.
    textList = []
    print("Started Reading JSON file which contains multiple JSON document")
    with open('sample_5k') as f:
        for jsonObj in f:
            studentDict = json.loads(jsonObj)
            textList.append(studentDict)
    #print(len(textList))
    processed = {}
    processed_list = []
    limit = 0
    for i in range(1000):
        text = textList[i]['body']
        new_item = {"test_doc{}".format(i):[text, []]}
        processed_list.append(new_item)
        
        '''if (limit<batch_size):
            
            text = textList[i]['body']
            new_item = {"test_doc{}".format(i):[text, []]}
            processed.update(new_item)
            limit = limit +1
            if (i == 4999):
                processed_list.append(processed)            
        else :
            processed_list.append(processed)
            processed = {}
            limit=0
            text = textList[i]['body']
            new_item = {"test_doc{}".format(i):[text, []]}
            processed.update(new_item)
            limit = limit +1'''
    print(len(processed_list))
    return processed_list


def entity_linking(input_text):

    wiki_version = "wiki_2014"


    base_url = "/home/ege/REL"
    start_wall = time.time()
    start_cpu = time.process_time()

    mention_detection = MentionDetection(base_url, wiki_version)
    tagger_ner = load_flair_ner("ner-fast")
    tagger_ngram = Cmns(base_url, wiki_version, n=5)
    mentions_dataset, n_mentions = mention_detection.find_mentions(
    input_text, tagger_ner)


    config = {
        "mode": "eval",
        # or alias, see also tutorial 7: custom models
        "model_path": "/home/ege/REL/wiki_2014/generated/model",
    }

    model = EntityDisambiguation(base_url, wiki_version, config)
    predictions, timing = model.predict(mentions_dataset)


    result = process_results(mentions_dataset, predictions, input_text)

    end_wall = time.time()
    end_cpu = time.process_time()
    print("The wall-time is {}".format(end_wall-start_wall))
    print("The cpu-time is {}".format(end_cpu-start_cpu))
    return (((end_wall -start_wall), (end_cpu -start_cpu)))

wall_time_results = []
cpu_time_results = []

for batch in example_preprocessing(1):
    result = entity_linking(batch)
    wall_time_results.append(result[0])
    cpu_time_results.append(result[1])
    with open("wall_results_out_1000_sqlite.txt", "a") as o:
        print(result[0], file=o)
    with open("cpu_results_out_1000_sqlite.txt", "a") as o:
        print(result[1], file=o)

print(wall_time_results)
print(cpu_time_results)
