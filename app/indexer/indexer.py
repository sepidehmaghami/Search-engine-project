# app/indexer/indexer.py

from elasticsearch import Elasticsearch, helpers
import json
import os

class HotelIndexer:
    def __init__(self, host='localhost', port=9200, index_name='hotels'):
        # اتصال به Elasticsearch
        self.es = Elasticsearch([{'host': host, 'port': port}])
        self.index_name = index_name
        # در صورتی که ایندکس وجود ندارد، آن را ایجاد کنید.
        if not self.es.indices.exists(index=self.index_name):
            self.create_index()

    def create_index(self):
        settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "properties": {
                    "url": {"type": "keyword"},
                    "name": {"type": "text"},
                    "address": {"type": "text"},
                    "star_rating": {"type": "integer"},
                    "rating": {"type": "float"},
                    "reviews_count": {"type": "integer"},
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
        self.es.indices.create(index=self.index_name, body=settings)
        print(f"Index '{self.index_name}' created.")

    def index_hotels(self, hotels):
        """
        hotels: لیستی از دیکشنری‌های هتل‌ها (مانند داده‌های استخراج شده توسط خزنده‌ها)
        """
        actions = [
            {
                "_index": self.index_name,
                "_id": hotel.get('url'),
                "_source": hotel
            }
            for hotel in hotels
        ]
        helpers.bulk(self.es, actions)
        print("Indexing complete.")

if __name__ == '__main__':
    # به عنوان مثال، فرض می‌کنیم فایل JSON مربوط به سایت hotelyar.com ذخیره شده است.
    # file_name = 'hotelyar.com.json'
    
    file_name = 'eghamat24.com.json'
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            hotels = json.load(f)
        indexer = HotelIndexer()
        indexer.index_hotels(hotels)
    else:
        print(f"File '{file_name}' not found.")
