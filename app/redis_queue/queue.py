import redis

from app.url import is_file_url


class Queue:
    def __init__(self,host,port):
        self.redis_client = redis.StrictRedis(host=host, port=port,db=3, decode_responses=True)

    def push_to_queue(self,name, value):
        if self.redis_client.get(value) == "1":
            return
        self.redis_client.set(value, 1)

        if is_file_url(value):
            return
        self.redis_client.rpush(f"redis_queue_{name}", value)

    def pop_from_queue(self,name):
        return self.redis_client.lpop(f"redis_queue_{name}")
