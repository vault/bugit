
import os, sys

this = os.path.dirname(os.path.abspath(__file__))
up1 = os.path.join(this, '..')
up2 = os.path.join(this, '..', '..')

paths = [up1, up2]

for path in paths:
    if path not in sys.path:
        sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'bugit.settings'

from gitolite import GitoliteUserConf, RepositoryConf
from common.models import User, PublicKey, Repository

from common.redis_client import redis_db, CommandQueue

from subprocess import call


def next_user(r):
    resp = r.blpop(CommandQueue.queue)
    user = resp[1]
    r.sadd(CommandQueue.processing, user)
    r.srem(CommandQueue.users, user)
    return user


def config_repo(config, repo, user):
    rc = RepositoryConf(repo.name, user.username, 
            user.get_full_name(), repo.description, repo.is_public)

    for c in repo.collaborators.all():
        rc.add_collaborator(c.username)

    config.add_repo(rc)

    if not repo.is_created:
        repo.is_created = True
        repo.save()


def config_key(config, key):
    config.add_user_key(key.description, key.pubkey)
    if not key.is_active:
        key.is_active = True
        key.save()


def process_user(r, user_name):
    print "Procesing", user_name
    user = User.objects.get(username=user_name)

    config = GitoliteUserConf(user.username)
    config.clean_user()

    for repo in user.owner_set.all():
        config_repo(config, repo, user)

    for key in user.publickey_set.all():
        config_key(config, key)

    config.save_and_commit()

    r.srem(CommandQueue.processing, user_name)


if __name__ == '__main__':


    print "Getting redis..."
    r = redis_db()

    print "CD-ing..."
    os.chdir("/srv/bugit/gitolite-admin")

    print "Updating local config..."
    call(["git", "pull"])

    print "Processing remnants..."
    for item in r.smembers(CommandQueue.processing):
        process_user(r, item)

    print "Entering main-loop"
    while True:
        user_name = next_user(r)
        call(["git", "pull"])
        process_user(r, user_name)
        call(["git", "push"])
        
