import json
import random
import time
from REL.mention_detection import MentionDetection
from REL.utils import process_results
from REL.entity_disambiguation import EntityDisambiguation
from REL.ner import Cmns, load_flair_ner

def example_preprocessing_1(batch_size):
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

def example_preprocessing_2():
   
    textList = []
    print("Started Reading JSON file which contains multiple JSON document")
    with open('sample_5k') as f:
        for jsonObj in f:
            studentDict = json.loads(jsonObj)
            textList.append(studentDict)
    #print(len(textList))
    processed_list = []

    random_num_list = random.sample(range(0, 4999), 20)

    for num in random_num_list:
        text = textList[num]['body']
        new_item = {"test_doc{}".format(num):[text, []]}
        processed_list.append(new_item)


    print(len(processed_list))
    return processed_list

def entity_linking(input_text):

    wiki_version = "wiki_2014"


    base_url = "/home/ege/REL"

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

def speed_analysis_1():
    wall_time_results = []
    cpu_time_results = []

    for batch in example_preprocessing_1(1):
        start_wall = time.time()
        start_cpu = time.process_time()

        result = entity_linking(batch)
        
        end_wall = time.time()
        end_cpu = time.process_time()
        
        result_wall = end_wall-start_wall
        result_cpu = end_cpu-start_cpu
        print("The wall-time is {}".format(result_wall))
        print("The cpu-time is {}".format(result_cpu))
        
        wall_time_results.append(result_wall)
        cpu_time_results.append(result_cpu)
        with open("wall_results_out_1000_sqlite.txt", "a") as o:
            print(result_wall, file=o)
        with open("cpu_results_out_1000_sqlite.txt", "a") as o:
            print(result_cpu, file=o)

    print(wall_time_results)
    print(cpu_time_results)

def speed_analysis_2():
    for batch in example_preprocessing_2():
        
        for i in range(10):
            print(i)
            entity_linking(batch)
            with open("wall_query_CREATEINDEX_results_duckdb.txt", "a") as f :
                f.write("\n")
            with open("cpu_query_CREATEINDEX_results_duckdb.txt", "a") as f:
                f.write("\n")

            with open("wall_query_CLEAR_results_duckdb.txt", "a") as f :
                f.write("\n")
            with open("cpu_query_CLEAR_results_duckdb.txt", "a") as f:
                f.write("\n")

            with open("wall_query_INSERTBATCHEMB_results_duckdb.txt", "a") as f:
                f.write("\n")
            with open("cpu_query_INSERTBATCHEMB_results_duckdb.txt", "a") as f:
                f.write("\n")

            with open("wall_query_INSERTBATCHWIKI_results_duckdb.txt", "a") as f:
                f.write("\n")
            with open("cpu_query_INSERTBATCHWIKI_results_duckdb.txt", "a") as f:
                f.write("\n")

            with open("wall_query_LOOKUP_results_sqlite_3.txt", "a") as f:
                f.write("\n")
            with open("cpu_query_LOOKUP_results_sqlite_3.txt", "a") as f:
                f.write("\n")

            with open("wall_query_LOOKUPWIK_results_sqlite_3.txt", "a") as f:
                f.write("\n")
            with open("cpu_query_LOOKUPWIK_results_sqlite_3.txt", "a") as f:
                f.write("\n")

        with open("wall_query_CREATEINDEX_results_duckdb.txt", "a") as f:
            f.write("\n\n")
        with open("cpu_query_CREATEINDEX_results_duckdb.txt", "a") as f:
            f.write("\n\n")

        with open("wall_query_CLEAR_results_duckdb.txt", "a") as f:
            f.write("\n\n")
        with open("cpu_query_CLEAR_results_duckdb.txt", "a") as f:
            f.write("\n\n")

        with open("wall_query_INSERTBATCHEMB_results_duckdb.txt", "a") as f:
            f.write("\n\n")
        with open("cpu_query_INSERTBATCHEMB_results_duckdb.txt", "a") as f:
            f.write("\n\n")

        with open("wall_query_INSERTBATCHWIKI_results_duckdb.txt", "a") as f:
            f.write("\n\n")
        with open("cpu_query_INSERTBATCHWIKI_results_duckdb.txt", "a") as f:
            f.write("\n\n")

        with open("wall_query_LOOKUP_results_sqlite_3.txt", "a") as f:
            f.write("\n\n")
        with open("cpu_query_LOOKUP_results_sqlite_3.txt", "a") as f:
            f.write("\n\n")

        with open("wall_query_LOOKUPWIK_results_sqlite_3.txt", "a") as f:
            f.write("\n\n")
        with open("cpu_query_LOOKUPWIK_results_sqlite_3.txt", "a") as f:
            f.write("\n\n")

speed_analysis_2()