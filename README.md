# search engine for words in a video (python)
This repository explains how to build a search engine for keywords in a video using google speech api and Elasticsearch.

## Requirements
You would need a google api credentials, and an Elastic Search server running either in remote or in local

## Process
The process is split into 2 scripts witten in Python3:
*transcribe.py: This module downloads a video from youtube, stores it in a google bucket and then perfomrs the transcription
*bulkinjectionES: This module gets the result (in a json file) and injects it into an ElasticSearch server
