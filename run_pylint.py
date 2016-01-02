# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import site
import sys
from pylint import lint as lint_mod
from subprocess import Popen, PIPE

site.addsitedir(os.getcwd())

def _get_env():
    '''Extracts the environment PYTHONPATH and appends the current sys.path to
    those.'''
    env = dict(os.environ)
    env[b'PYTHONPATH'] = os.pathsep.join(sys.path)
    return env


# Start pylint
# pip install pylint
# Ensure we use the python and pylint associated with the running epylint
parent_path = os.path.dirname(os.getcwd())
child_path = os.path.basename(os.getcwd())
lint_path = lint_mod.__file__
cmd = [r'C:\Python27\python.exe', lint_path] + [
    '--msg-template', '{path}:{line}: {category} ({msg_id}, {symbol}, {obj}) {msg}',
    '--max-line-length=79', child_path]
process = Popen(cmd, stdout=PIPE, cwd=parent_path, env=_get_env(),
                universal_newlines=True)

currently_saving = False
rpt_data = []
for line in process.stdout:
    line = line.strip()
    if line == 'Raw metrics':
        currently_saving = True
    if currently_saving:
        rpt_data.append(line)
    # remove pylintrc warning
    if line.startswith("No config file found"):
        continue

    print line

process.wait()
with open('bleh.txt', 'w') as ofstream:
    for line in rpt_data:
        ofstream.write(line + '\n')
sys.exit()
