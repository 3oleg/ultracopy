import os
import sys
import time
import subprocess

count = 0
error = 0
startedtime = time.time()
runningtime = time.time()
statist = {"count": 0, 'run': time.time()}

outdir = '/opt/tars'
servers = ('s4.mycomp.ru', 's5.mycomp.ru')


def runcommand(command):
    res = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                           env={**os.environ, 'PATH': '/usr/sbin:/sbin:' + os.environ['PATH']})
    return map(lambda x: x.decode('utf-8'), res.communicate())


while True:
    for server in servers:
        files = []
        o, e = runcommand('ssh %s ls /opt/tars' % server)
        if not e:
            files = [i for i in o.split("\n") if 'images' in i]
            print(files)

        for file in files[:50]:
            com = 'umask 000 && ssh %s "cat /opt/tars/%s" | tar --no-same-permissions -xvPf -' % (server, file)
            o, e = runcommand(com)
            count += o.count('\n')
            if not e:
                print("Archive %s extracted (%s files). Deleting" % (file, o.count('\n')))
                runcommand('ssh %s rm /opt/tars/%s' % (server, file))
            else:
                print('%s: %s' % (com, e))
            sys.stdout.flush()

    print('total unextracting %s files in %d sec' % (count, time.time() - startedtime))
    time.sleep(10)

