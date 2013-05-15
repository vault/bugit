
import redis

#redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

class CommandQueue:
    queue = 'bugit_processing_queue'
    users = 'bugit_processing_users'
    processing = 'bugit_in_progress'

def redis_db():
    return redis.Redis(host='localhost', port=6379, db=0)

