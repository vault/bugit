
import os, sys, pwd, grp, syslog, signal
import optparse

from .gitolite import GitoliteUserConf, RepositoryConf

from bugit.common.models import User
from bugit import settings
from bugit.common.redis_client import redis_db, CommandQueue

from subprocess import call

DEBUG = False

def log(message, level=syslog.LOG_INFO):
    if not DEBUG:
        syslog.syslog(level, message)
    else:
        print message


def drop_permissions(username='nobody', groupname='nogroup'):
    if os.getuid() != 0:
        return

    uid = pwd.getpwnam(username).pw_uid
    gid = grp.getgrnam(groupname).gr_gid

    os.setgroups([])
    os.setgid(gid)
    os.setuid(uid)
    os.umask(077)


def daemonize():
    if os.fork() == 0:
        # child process
        signal.signal(signal.SIGHUP, signal.SIG_IGN)
        pid = os.fork()

        if pid != 0:
            os._exit(0)
        else:
            write_pid_file()
    else:
        os._exit(0)


def write_pid_file():
    os.umask(077)
    pid = os.getpid()
    exists = True
    pidpath = '/var/run/git-worker.pid'
    try:
        pidfile = open(pidpath, 'r')
        pidfile.close()
    except IOError as error:
        if error.errno == 13:
            log("Can't write PID file, exiting", syslog.LOG_ERR)
            sys.exit(1)
        elif error.errno == 2:
            exists = False

    if exists:
        log("PID file already exists. We may not have shut down properly. Overwriting.",
                syslog.LOG_ERR)

    try:
        pidfile = open(pidpath, 'w')
        pidfile.write(str(pid))
        pidfile.close()
    except IOError as error:
        if error.errno == 13:
            log("Can't write PID file, exiting", syslog.LOG_ERR)
        sys.exit(1)



def next_user(r):
    resp = r.blpop(CommandQueue.queue)
    user = resp[1]
    r.sadd(CommandQueue.processing, user)
    r.srem(CommandQueue.users, user)
    return user


def config_repo(config, repo, user):
    permission_map = {'R':'R', 'W':'RW', 'O':'RW+'}
    rc = RepositoryConf(repo.name, user.username, 
            user.get_full_name(), repo.description, repo.is_public)

    for c in repo.collaboration_set.all():
        perm = permission_map[c.permission]
        rc.add_collaborator(c.user.username, perm)

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
    log("Procesing user '%s'"% user_name)
    user = User.objects.get(username=user_name)

    config = GitoliteUserConf(user.username)
    config.clean_user()

    for repo in user.owner_set.all():
        config_repo(config, repo, user)

    for key in user.publickey_set.all():
        config_key(config, key)

    config.save_and_commit()

    r.srem(CommandQueue.processing, user_name)


def main():
    parser = optparse.OptionParser(description='Run gitolite config daemon')
    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Don't daemonize, log to stdout")
    (options, args) = parser.parse_args()
    DEBUG = options.debug

    if not DEBUG:
        null = open("/dev/null", 'w')
        sys.stdout = null
        sys.stderr = null

    if not DEBUG:
        daemonize()
        drop_permissions(settings.WORKER_USER, settings.WORKER_GROUP)

    syslog.openlog('git-worker')
    log(settings.WORKER_USER +  settings.WORKER_GROUP)

    log("Connecting to redis")
    r = redis_db()

    if not DEBUG:
        log("Changing to gitolite-admin directory")
        home = pwd.getpwnam(settings.WORKER_USER)[5]
        log(home)
        admin = os.path.join(home, 'gitolite-admin')
        os.chdir(admin)

    log("Updating gitolite-admin config...")
    call(["git", "pull"])

    log("Processing pre-existing users")
    for item in r.smembers(CommandQueue.processing):
        process_user(r, item)

    log("Entering main-loop")
    while True:
        user_name = next_user(r)
        call(["git", "pull"])
        process_user(r, user_name)
        call(["git", "push"])
        

if __name__ == '__main__':
    main()

