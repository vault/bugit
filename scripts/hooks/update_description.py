#!/usr/bin/env python

from subprocess import Popen, PIPE, call
import re
import os
import sys


app_path = open('/etc/bugit/settings').read().strip()
sys.path.append(app_path)
bugit_path = os.path.join(app_path, 'bugit')
sys.path.append(bugit_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'bugit.settings'
git_notify = os.path.join(bugit_path, 'lib', "git-notifier", 'git-notifier')

from bugit.common.models import Repository


def extract_readme():
    """Finds the readme file and returns it with extension

    Users git cat-file on the master branch only, and returns the first 
    match for readme. May not be stable as filenames change.
    """
    tree = Popen(["git", "cat-file", "-p", "master^{tree}"], stdout=PIPE).communicate()[0]
    lines = tree.strip().split('\n')

    for line in lines:
        parts = line.split('\t')
        fname = parts[1]
        fhash = parts[0].split(' ')[2]
        m = re.match(r'readme(\.(\w*))?', fname, re.IGNORECASE)
        if m is not None:
            ext = m.group(2) if m.group(2) else 'txt'
            text = Popen(['git', 'cat-file', '-p', fhash], stdout=PIPE).communicate()[0]
            return (text, ext)



def extract_repo():
    """Figure out the name of the git repo
    
    Assume it's named [1]/[2] where [2] is the folder containing
    the .git directory"""
    path = os.getcwd().split('/')
    while path:
        ret = call(['git', 'rev-parse'])
        if ret == 0:
            name = path[-1]
            user = path[-2]
            parts = name.split('.')
            if parts[-1] == 'git':
                name = '.'.join(parts[:-1])
            else:
                name = '.'.join(parts)
            return (user, name)
        path = path[:-1]
    return (None, None)


def clean_readme(readme_text):
    """Remove any 'bad' characters from the readme_text

    Since people are uploading arbitrary things this is a pretty huge security
    opportunity. We need to make sure people don't start tossing binaries into it
    or some weird browser exploits.
    """
    control_chars = ''.join(map(unichr, range(0,32)+range(127,160)))
    pattern = re.compile(r'[%s]' % re.escape(control_chars), re.I|re.U)
    clean_text = '\n'.join(map(lambda l: pattern.sub('', l), readme_text.split('\n')))
    return clean_text


def readme_format(fmt):
    """Look at the extension of the readme and return the format"""
    formats = {
            'md'       : 'M',
            'markdown' : 'M',
            'txt'      : 'T',
    }
    if fmt in formats:
        return formats[fmt]
    else:
        return 'T'


def update_readme(readme_text, readme_format, repo_user, repo_name):
    """Update the repo description
    
    Logs in to MySQL and sets the repo description to what it was
    calculated to be from the repository.
    """
    if repo_user is None or repo_name is None:
        return

    repo = Repository.objects.get(owner__username=repo_user, name=repo_name)
    repo.long_description = readme_text
    repo.description_format = readme_format
    repo.save()


def email_collaborators(repo_user, repo_name):
    repo = Repository.objects.get(owner__username=repo_user, name=repo_name)
    if repo.email_on_update:
        to_email = repo.collaborators.exclude(userprofile__never_email=True)
        sender = os.environ['GL_USER'].split("-")[0]
        sender = "%s@bu.edu"%sender
        commit = 'https://eng-git.bu.edu/view/%s/%s/commit?id='%(repo_user, repo_name)
        url = 'https://eng-git.bu.edu/repo/%s/%s/' % (repo_user, repo_name)
        prefix = '[eng-git] [%s/%s]'% (repo_user, repo_name)
        l = ",".join([user.email for user in to_email])

        notify_cmd = [git_notify, "--emailprefix=%s"%prefix, "--hostname=eng-git.bu.edu", 
                "--mailinglist=%s"%l, "--repouri=%s"%url, "--sender=%s"%sender,
                '--link='+commit+'%s' ]
        call(notify_cmd)


if __name__ == '__main__':
    try:
        (text, fmt)  = extract_readme()
        (user, name) =  extract_repo()
        text = clean_readme(text)
        fmt = readme_format(fmt)
        update_readme(text, fmt, user, name)
        email_collaborators(user, name)
    except Exception, e:
        print "There was a problem: ", e

