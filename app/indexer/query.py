import os
from elasticsearch import Elasticsearch

def search_hotels(es, index_name, query_text):
    # If the search term is empty, we use match_all
    if not query_text.strip():
        search_body = {
            "query": {
                "match_all": {}
            }
        }
    else:
        search_body = {
            "query": {
                "bool": {
                    "should": [
                        # Search in top-level fields (name, address and URL)
                        {
                            "multi_match": {
                                "query": query_text,
                                "fields": ["name", "address", "url"]
                            }
                        },
                        # Search in nested fields related to rooms
                        {
                            "nested": {
                                "path": "rooms",
                                "query": {
                                    "multi_match": {
                                        "query": query_text,
                                    # If the document is hotelyar, the room_name field is present
                                    # And if the document is eghamat24, the type and board_type fields are present
                                        "fields": ["rooms.type", "rooms.room_name", "rooms.board_type"]
                                    }
                                }
                            }
                        },
                        # Search nested fields related to comments
                        {
                            "nested": {
                                "path": "comments",
                                "query": {
                                    "multi_match": {
                                        "query": query_text,
                                        # In some documents the comment key is "user" and in some it is "username"
                                        "fields": ["comments.user", "comments.username", "comments.text"]
                                    }
                                }
                            }
                        },

                        # Search for location, country, and rating information (in documents like lastsecond)
                        {
                            "multi_match": {
                                "query": query_text,
                                "fields": ["location.titleFa", "country.titleFa", "grade.title"]
                            }
                        }
                    ],
                    "minimum_should_match": 1
                }
            }
        }
    
    result = es.search(index=index_name, body=search_body)
    return result

if __name__ == '__main__':
    es = Elasticsearch(
        "https://localhost:9200",
        basic_auth=("elastic", "Ug1o-XGw9*DaSmIQciSJ"),
        verify_certs=False,
        request_timeout=30
    )
    
    index_name = "hotels"
    query_text = input("Enter search term: ")
    
    results = search_hotels(es, index_name, query_text)
    
    print("\on Search results:")
    for hit in results['hits']['hits']:
        print("-" * 50)
        print(f"امتیاز: {hit['_score']}")
        print("اطلاعات هتل:")
        for key, value in hit['_source'].items():
            print(f"{key}: {value}")
