import dj_redis_url
from decouple import config
from redis import Redis

REDIS = dj_redis_url.config(default=config('REDIS_URL'))
redis_client = Redis(host=REDIS['HOST'], port=REDIS['PORT'], password=REDIS['PASSWORD'])
SESSION_TTL = 60 * 60 * 24  # Session expiration time in seconds.
