
import os
import errno
from subprocess import call
import shutil

def make_dirs(path):
    try:
        os.makedirs(path, 0755)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def rm(file):
    try:
        os.unlink(file)
    except OSError as exception:
        if exception.errno != errno.ENOENT:
            raise

class RepositoryConf(object):

    def __init__(self, name, user, full_name, description, public, user_path="user"):
        self.user_path = user_path
        self.name = name
        self.user = user
        self.description = description
        self.user_name = full_name
        self.path = os.path.join(user, name)
        self.public = public
        self.collaborators = []


    def add_collaborator(self, user, permission):
        self.collaborators.append((user, permission))


    def config_block(self):
        lines = []
        lines.append("\n")
        lines.append("repo %s" % self.path)
        #lines.append("\tRW+ = @user-%s" % self.user)
        lines.append("\towner = %s" % self.user_name)
        lines.append("\tdesc = %s" % self.description)
        for c in self.collaborators:
            lines.append("\t%s = @user-%s" % (c[1], c[0]))
        if self.public:
            lines.append("\tR = @all")
            lines.append("\tR = daemon")
        #lines.append("\tR = gitweb")
        lines.append("\n")
        return '\n'.join(lines)


class GitoliteUserConf(object):
    def __init__(self, user_name, user_path="user", groups_path="groups"):
        self.user_path = user_path
        self.groups_path = groups_path
        self.user = user_name
        self.keys = []
        self.repositories = []
        self.group_file = os.path.join("conf", groups_path, "%s-group.conf" % user_name)
        self.repo_file = os.path.join("conf", user_path, "%s-config.conf" % user_name)
        self.key_path = os.path.join("keydir", user_path, user_name) 


    def add_repo(self, repo):
        self.repositories.append(repo)


    def add_user_key(self, key_name, key_text):
        self.keys.append(("%s-%s" % (self.user, key_name), key_text))


    def delete_user_keys(self):
        shutil.rmtree(self.key_path, ignore_errors=True)


    def clean_user(self):
        self.delete_user_keys()
        rm(self.group_file)
        rm(self.repo_file)


    def user_group(self):
        key_names = ' '.join([key[0] for key in self.keys])
        group = "@user-%s" % self.user
        return "%s = %s\n" % (group, key_names)
    

    def repo_config(self):
        configs = []
        for repo in self.repositories:
            configs.append(repo.config_block())
        return '\n'.join(configs)


    def write_user_keys(self):
        make_dirs(self.key_path)
        for key in self.keys:
            path = os.path.join(self.key_path, "%s.pub"%key[0])
            with open(path, 'w') as key_file:
                key_file.write(key[1])


    def write_repo_config(self):
        make_dirs(os.path.join("conf", self.user_path))
        with open(self.repo_file, 'w') as f:
            f.write(self.repo_config())


    def write_user_groups(self):
        make_dirs(os.path.join("conf", self.groups_path))
        with open(self.group_file, 'w') as gf:
            gf.write(self.user_group())


    def save(self):
        self.write_repo_config()
        self.write_user_keys()
        self.write_user_groups()


    def commit(self):
        message = "Update configs for %s" % self.user
        call(["git", "add", "%s/*" % self.key_path])
        call(["git", "add", self.group_file])
        call(["git", "add", self.repo_file])
        call(["git", "commit", "-am", message])


    def save_and_commit(self):
        self.save()
        self.commit()

