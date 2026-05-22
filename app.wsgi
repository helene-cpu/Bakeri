import sys
import site
import os

site.addsitedir('/var/www/bakeri/env/lib/python3.13/site-packages')

sys.path.insert(0, '/var/www/bakeri')

os.chdir('/var/www/bakeri')

os.environ['VIRTUAL_ENV'] = '/var/www/bakeri/env'
os.environ['PATH'] = '/var/www/bakeri/env/bin:' + os.environ['PATH']

from app import app as application
