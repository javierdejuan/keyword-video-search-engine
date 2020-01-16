# search engine for words in a video (python)
This repository explains how to build a search engine for keywords in a video using google speech api and Elasticsearch.

## Requirements
You would need a google api credentials, and an Elastic Search (version higer than 7.4) server running either in remote or in local

## Process
The process is split into 2 scripts witten in Python3:
*__transcribe.py__: This module downloads a video from youtube, transforms the video in the correct format then stores it in a google bucket and then performs the transcription, returning a json file with words and their time ocurrence within the video.
*__bulkinjectionES.py__: This module gets the result (in a json file) and injects it into an ElasticSearch server.

Then, you can enable a __"google like"__ search with completion. This is done through the "magic" of elasticsearch, modelling the index as follows:

```python
  mapping={
        "mappings": {
            "properties": {
             "start" : {
                "type" : "float"
                    },
             "timestamp" : {
              "type" :"date"
            },
         "word" : {
                "type" : "search_as_you_type",
                "max_shingle_size" : 3
            }
        }
       }
     }
```
