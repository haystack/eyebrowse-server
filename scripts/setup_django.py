import os
import sys

curdir, curfile = os.path.split(os.path.abspath(__file__))
parentdir = os.path.normpath(os.path.join(curdir, '..'))
sys.path.append(parentdir)

os.environ["DJANGO_SETTINGS_MODULE"] = "eyebrowse.settings"
