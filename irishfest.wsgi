#!/usr/bin/python
import os, site, sys

# Tell wsgi to add the Python site-packages to it's path.
site.addsitedir('/home/jgonzales/.virtualenvs/irishfest/lib/python2.7/site-packages')

# Fix markdown.py (and potentially others) using stdout
sys.stdout = sys.stderr

# Calculate the path based on the location of the WSGI script.
project = os.path.dirname(__file__)
workspace = os.path.dirname(project)
sys.path.append(workspace)

# Tell wsgi to add additional folders to it's Python path such as apps or lib.
sys.path.append('/home/jgonzales/webapps/irishfest/src/irishfest')

os.environ['DJANGO_SETTINGS_MODULE'] = 'irishfest.settings'
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()

# Tell wsgi to add additional folders to it's Python path such as apps or lib. 
from django.conf import settings
sys.path.insert(0, os.path.join(settings.PROJECT_ROOT, "apps"))
sys.path.insert(0, os.path.join(settings.PROJECT_ROOT, "lib"))