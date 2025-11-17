import redis
from src.core.config import config 

REDIS_URL = config.REDIS_URL

rd = redis.from_url(REDIS_URL)
rd.ping() 
rd.set('name', 'Kushal Raga')
print(rd.get('name'))

