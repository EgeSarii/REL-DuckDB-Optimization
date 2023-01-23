import json
import time
from REL.mention_detection import MentionDetection
from REL.utils import process_results
from REL.entity_disambiguation import EntityDisambiguation
from REL.ner import Cmns, load_flair_ner

def example_preprocessing():
    # user does some stuff, which results in the format below.
    textList = []
    print("Started Reading JSON file which contains multiple JSON document")
    text1 = "Obama will visit Germany. And have a meeting with Merkel tomorrow."
    processed = {"test_doc1": [text1, []]}
    return processed


def entity_linking():

    wiki_version = "wiki_2014"

    input_text = example_preprocessing()

    base_url = "/home/ege/REL"
    start = time.time()
    start2 = time.process_time()
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

    end = time.time()
    end2 =time.process_time()
    print(result)

    print("The wall-time is {}".format(end-start))
    print("The cpu-time is {}".format(end2-start2))

entity_linking()