# search engine for words in a video (python)
This repository explains how to build a search engine for keywords in a video using google speech api and Elasticsearch.

## Requirements
You would need a google api credentials, and an Elastic Search server running either in remote or in local

## Process
The process is split into 2 scripts witten in Python3:
* _transcribe.py_: This module downloads a video from youtube, stores it in a google bucket and then perfomrs the transcription, returning a json file with words and their time ocurrence within the video.
* _bulkinjectionES.py: This module gets the result (in a json file) and injects it into an ElasticSearch server.

Then, you can enable a "google like" search with completion. This is done through the "magic" of elasticsearch, modelling the index as follows:
Markup :  `code()`
 var specificLanguage_code = 
    {
        "data": {
            "lookedUpPlatform": 1,
            "query": "Kasabian+Test+Transmission",
            "lookedUpItem": {
                "name": "Test Transmission",
                "artist": "Kasabian",
                "album": "Kasabian",
                "picture": null,
                "link": "http://open.spotify.com/track/5jhJur5n4fasblLSCOcrTp"
            }
        }
    }
Markup : ```javascript


