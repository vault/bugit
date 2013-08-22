#!/usr/bin/python

import sys, os

app_path = open('/etc/bugit/settings').read().strip()
sys.path.append(app_path)

bugit_path = os.path.join(app_path, 'bugit')
sys.path.append(bugit_path)
worker_path = os.path.join(bugit_path, 'scripts', 'daemon')
sys.path.append(worker_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'bugit.settings'

import worker

worker.main()

