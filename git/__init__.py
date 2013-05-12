
import redis

redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

class CommandQueue:
    queue = 'bugit_processing_queue'
    users = 'bugit_processing_users'
    in_progress = 'bugit_in_progress'

def redis_db():
    return redis.StrictRedis(connection_pool = redis_pool)
