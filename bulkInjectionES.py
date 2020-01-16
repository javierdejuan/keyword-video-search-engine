#!/usr/bin/python

# import Python's JSON library for its loads() method
import json
import sys, getopt

# import time for its sleep method
from time import sleep

# import the datetime libraries datetime.now() method
from datetime import datetime

# use the elasticsearch client's helpers class for _bulk API
from elasticsearch import Elasticsearch, helpers


# define a function that will load a text file
def get_data_from_text_file(self):
    # the function will return a list of docs
    return [l.strip() for l in open(str(self), encoding="utf8", errors='ignore')]


def main(argv):
    inputfile = ''
    index_name = ''
    try:
        opts, args = getopt.getopt(argv,"hf:i:",["ffile=","iindex="])
    except getopt.GetoptError:
        print ('bulkinjectionEs.py -f <inputfile> -i <index>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('bulkinjectionEs.py -f <inputfile> -i <index>')
            sys.exit()
        elif opt in ("-f", "--ffile"):
            inputfile = arg
        elif opt in ("-i", "--iindex"):
            index_name = arg

    if not inputfile or not index_name:
      print ('usage: bulkinjectionEs.py -f <inputfile> -i <index>')
      quit()

    print ('Input file is :', inputfile)
    print ('index name is :', index_name)



    # declare a client instance of the Python Elasticsearch library
    client = Elasticsearch([{'host': <your elastic search host>, 'port': <port_number>}])



    # call the function to get the string data containing docs
    docs = get_data_from_text_file(inputfile)

    # print the length of the documents in the string
    print ("String docs length:", len(docs))

    # define an empty list for the Elasticsearch docs
    doc_list = []

    # use Python's enumerate() function to iterate over list of doc strings
    for num, doc in enumerate(docs):

    # catch any JSON loads() errors
        try:
            # convert the string to a dict object
            dict_doc = json.loads(doc)
            # add a new field to the Elasticsearch doc
            dict_doc["timestamp"] = datetime.now()
            # add a dict key called "_id" if you'd like to specify an ID for the doc
            dict_doc["_id"] = num
            # append the dict object to the list []
            doc_list += [dict_doc]

        except json.decoder.JSONDecodeError as err:
            # print the errors
            print ("ERROR for num:", num, "-- JSONDecodeError:", err, "for doc:", doc)

    print ("Dict docs length:", len(doc_list))

    # attempt to index the dictionary entries using the helpers.bulk() method
    try:
        print ("\nAttempting to create index:",index_name)

        mapping={
        "mappings": {
        "properties": {
        "start" : {
                "type" : "float"
                    },
        "timestamp" : {
        "type" : "date"
            },
        "word" : {
                "type" : "search_as_you_type",
                "max_shingle_size" : 3
            }
        }
        }
        }

        if client.indices.exists(index=index_name):
            response = client.indices.delete(index=index_name)

        response = client.indices.create(
            index=index_name,
            body=mapping,
            ignore=400 
        )
        if 'acknowledged' in response:
            if response['acknowledged'] == True:
                print ("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])

        # catch API error response
        elif 'error' in response:
            print ("ERROR:", response['error']['root_cause'])
            print ("TYPE:", response['error']['type'])
        
    except Exception as err:

        # print any errors returned while making the helpers.bulk() API call
        print("Elasticsearch client.indices.create() ERROR:", err)
        quit() 

    try:
        print ("\nAttempting to index the list of docs using helpers.bulk()")

        # use the helpers library's Bulk API to index list of Elasticsearch docs
        resp = helpers.bulk(
        client,
        doc_list,
        index = index_name,
        doc_type = "_doc"
        )
        # print the response returned by Elasticsearch
        print ("helpers.bulk() RESPONSE:", resp)
        print ("helpers.bulk() RESPONSE:", json.dumps(resp, indent=4))

    except Exception as err:

        # print any errors returned while making the helpers.bulk() API call
        print("Elasticsearch helpers.bulk() ERROR:", err)
        quit()


if __name__ == "__main__":
    main(sys.argv[1:])
