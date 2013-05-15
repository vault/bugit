
from common.redis import redis_db, CommandQueue


def dispatch_repo_work(sender, **kwargs):
    obj = kwargs['instance']
    if not hasattr(obj, 'owner'):
        return

    user = obj.owner.username
    r = redis_db()

    if not r.sismember(CommandQueue.users, user):
        r.sadd(CommandQueue.users, user)
        r.rpush(CommandQueue.queue, user)

