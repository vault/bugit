#!/usr/bin/env python

from subprocess import Popen, PIPE, call
import MySQLdb
import re
import os

DB = {
   'name':'bugit_testing',
   'host':'localhost',
   'user':'bugit_desc',
   'pass':'81c94361be2668ddb7ec123e739605b4'
}


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
    #TODO: actually filter this. I'm terrible, I know
    return readme_text


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
    db = MySQLdb.connect(passwd=DB['pass'], db=DB['name'], user=DB['user'], host=DB['host'])
    cursor = db.cursor()
    cursor.execute("SELECT id from auth_user where username = %s;", repo_user)
    owner_id = cursor.fetchone()[0]
    print "Owner id is ", owner_id
    SQL = """
        UPDATE common_repository SET long_description = %s, description_format = %s
        WHERE owner_id = %s AND name = %s;
    """
    cursor.execute(SQL, (readme_text, readme_format[0], owner_id, repo_name))


if __name__ == '__main__':
    try:
        (text, fmt)  = extract_readme()
        (user, name) =  extract_repo()
        text = clean_readme(text)
        fmt = readme_format(fmt)
        update_readme(text, fmt, user, name)
    except Exception, e:
        print "There was a problem: ", e

