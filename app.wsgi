import os
import sys

cwd = os.getcwd()
env_dir = os.path.join(cwd, 'env')
project_dir = os.path.join(cwd, 'webcheck')

INTERP = os.path.join(env_dir, 'bin', 'python3.6')
if sys.executable != INTERP:
	os.execl(INTERP, *sys.argv)

# Add virtualenv packages to the start of the path
sys.path.insert(0, os.path.join(env_dir, 'bin'))
sys.path.insert(0, os.path.join(env_dir, 'lib', 'python3.6', 'site-packages'))

# (so it will be checked last).
sys.path.append(project_dir)

from webcheck import app as application