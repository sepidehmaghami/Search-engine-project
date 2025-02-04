from elasticsearch import Elasticsearch

class HotelSearcher:
    def __init__(self, host='localhost', port=9200, index_name='hotels'):
        self.es = Elasticsearch([{'host': host, 'port': port}])
        self.index_name = index_name

    def search_hotels(self, query, size=10):
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["name", "address", "rooms.room_name", "comments.text"]
                }
            }
        }
        response = self.es.search(index=self.index_name, body=body, size=size)
        return response['hits']['hits']

if __name__ == '__main__':
    searcher = HotelSearcher()
    # به عنوان مثال، جستجویی بر اساس عبارت "هتل بزرگ" انجام می‌دهیم.
    results = searcher.search_hotels("هتل بزرگ")
    for hit in results:
        source = hit['_source']
        print(f"Name: {source.get('name')}\nURL: {source.get('url')}\n{'-'*30}")
