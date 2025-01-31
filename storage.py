# data_storage/storage.py

import json
import os
from elasticsearch import Elasticsearch
import logging

# پیکربندی لاگینگ
logging.basicConfig(
    filename='storage.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class DataStorage:
    def __init__(self, output_dir='data', elastic_host='elasticsearch', elastic_port=9200):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.elasticsearch = Elasticsearch([{'host': elastic_host, 'port': elastic_port}])
        self._setup_elasticsearch()

    def _setup_elasticsearch(self):
        if not self.elasticsearch.indices.exists(index="hotels"):
            self.elasticsearch.indices.create(index="hotels")
            logging.info("Elasticsearch index 'hotels' created.")

    def save_to_json(self, data):
        filename = os.path.join(self.output_dir, f"{self._sanitize_filename(data['name'])}.json")
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logging.info(f"Data saved to {filename}")
        except Exception as e:
            logging.error(f"Failed to save data to JSON for {data['name']}: {e}")

    def index_into_elasticsearch(self, data):
        try:
            self.elasticsearch.index(index="hotels", body=data)
            logging.info(f"Data indexed into Elasticsearch for hotel: {data['name']}")
        except Exception as e:
            logging.error(f"Failed to index data into Elasticsearch for {data['name']}: {e}")

    def process_data(self, data):
        self.save_to_json(data)
        self.index_into_elasticsearch(data)

    def _sanitize_filename(self, name):
        return "".join(c if c.isalnum() else "_" for c in name)

def process_json_files(directory='data'):
    """
    این تابع برای پردازش فایل‌های JSON ذخیره شده استفاده می‌شود.
    می‌توانید منطق پردازش اضافی را در اینجا اضافه کنید.
    """
    storage = DataStorage(directory)
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # انجام پردازش اضافی در صورت نیاز
                    logging.info(f"Processed {filename}")
            except Exception as e:
                logging.error(f"Failed to process {filename}: {e}")
