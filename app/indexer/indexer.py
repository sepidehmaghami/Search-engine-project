import os
import sys
import json
from elasticsearch import Elasticsearch, helpers

def create_index(es, index_name):
    mapping = {
        "mappings": {
            "properties": {
                "url": {"type": "keyword"},
                "name": {"type": "text", "analyzer": "standard"},
                "star_rating": {"type": "integer"},
                "rating": {"type": "float"},
                "reviews_count": {"type": "integer"},
                "address": {"type": "text"},
                "whole_room_count": {"type": "integer"},
                "height": {"type": "keyword"},
                "rooms": {
                    "type": "nested",
                    "properties": {
                        "room_name": {"type": "text"},
                        "room_price": {"type": "integer"},
                        "room_discount": {"type": "keyword"}
                    }
                },
                "comments": {
                    "type": "nested",
                    "properties": {
                        "username": {"type": "text"},
                        "score": {"type": "float"},
                        "text": {"type": "text"}
                    }
                }
            }
        }
    }
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
    es.indices.create(index=index_name, body=mapping)
    print(f"Index '{index_name}' created.")

def index_data(es, index_name, data):
    actions = []
    for d in data:
        print(json.dumps(d, indent=2, ensure_ascii=False))  # Check data before sending
        actions.append({
            "_index": index_name,
            "_source": d
        })

    try:
        helpers.bulk(es, actions)
        print(f"{len(actions)} Documents have been added to index '{index_name}'.")
    except helpers.BulkIndexError as e:
        print("An indexing error occurred:")
        for error in e.errors:  
            print(json.dumps(error, indent=2, ensure_ascii=False))


def main():
    # json_path = os.path.join(os.path.dirname(__file__), "..", "hotelyar.com.json")
    # json_path = os.path.join(os.path.dirname(__file__), "..", "eghamat24.com.json")
    json_path = os.path.join(os.path.dirname(__file__), "..", "lastsecond.json")
    if not os.path.exists(json_path):
        print(f"JSON file not found at {json_path}.")
        sys.exit(1)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    es = Elasticsearch(
        "https://localhost:9200",
        basic_auth=("elastic", "Ug1o-XGw9*DaSmIQciSJ"),
        verify_certs=False,  
        request_timeout=30
    )

    index_name = "hotels"
    
    create_index(es, index_name)
    index_data(es, index_name, data)
    
    print("Indexing complete.")

if __name__ == "__main__":
    main()
