import redis
import hashlib

class URLManager:
    def __init__(self, redis_host='localhost', redis_port=6379, queue_key='url_queue', visited_key='visited_urls'):
        self.queue_key = queue_key
        self.visited_key = visited_key
        try:
            self.redis = redis.Redis(host=redis_host, port=redis_port, db=0)
            self.redis.ping()
        except redis.exceptions.ConnectionError:
            print("Unable to connect to Redis. Ensure the server is running on the specified host and port.")
            return

    def add_url(self, url):
        url_hash = self._hash_url(url)
        if not self.redis.sismember(self.visited_key, url_hash):
            self.redis.lpush(self.queue_key, url)
            self.redis.sadd(self.visited_key, url_hash)
            print(f"URL added: {url}")
        else:
            print(f"URL was added before: {url}")
            
    def get_url(self):
        url = self.redis.rpop(self.queue_key)
        if url:
            decoded_url = url.decode('utf-8')
            print(f"URL received: {decoded_url}")
            return decoded_url
        print("No URL available to receive.")
        return None

    def has_urls(self):
        return self.redis.llen(self.queue_key) > 0

    def _hash_url(self, url):
        return hashlib.md5(url.encode('utf-8')).hexdigest()

if __name__ == "__main__":
    url_manager = URLManager()
    initial_urls = [
        "https://www.eghamat24.com/IranHotels.html",
        # "https://hotelyar.com/city/27/%D9%87%D8%AA%D9%84%D9%87%D8%A7%DB%8C-%D9%85%D8%B4%D9%87%D8%AF",
        # "https://lastsecond.ir/hotels/mashhad"
    ]
    for url in initial_urls:
        url_manager.add_url(url)
    
    # print("URLs in the queue:")    
    # # url_manager.get_url()
