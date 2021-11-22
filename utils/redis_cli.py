import json

import redis


class RedisCli:

    def __init__(self):
        self.pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True, db=2)
        self.r = redis.StrictRedis(connection_pool=self.pool)

    def set(self, key, value, ex=259200):
        if isinstance(value, list) or isinstance(value, dict):
            value = json.dumps(value)
        # 设置3*24h的过期时间
        if ex:
            self.r.set(key, value, ex)
        else:
            self.r.set(key, value)

    def get(self, key):
        val = self.r.get(key)
        try:
            val = json.loads(val)
        except:
            pass
        return val

    def delete(self, key):
        return self.r.delete(key)

    def keys(self):
        return self.r.keys()


redisCli = RedisCli()