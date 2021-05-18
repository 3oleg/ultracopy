import os
import re
import sys
import time
import shutil
import subprocess

directory='/mnt/storage1/'
outdir='/opt/tars'
x16=r'[0-9A-F]+'
count=0
error=0
startedtime=time.time()
runningtime=time.time()
statist={"count":0,'run':time.time()}



def runcommand(command):
    res = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                           env={**os.environ, 'PATH': '/usr/sbin:/sbin:' + os.environ['PATH']})
    return map(lambda x: x.decode('utf-8'), res.communicate())


for l1 in [l for l in sorted(os.listdir(directory)) if re.fullmatch(x16, l)]:
    if l1 not in ['32', '33']:
       print (l1 + ' continue')
       continue
    for l2 in [l for l in sorted(os.listdir(directory+l1)) if re.fullmatch(x16, l)]:
        for l3 in [l for l in sorted(os.listdir(directory + l1 + '/' + l2)) if re.fullmatch(x16, l)]:

            runcommand('echo %s.%s.%s> current.txt' % (l1,l2,l3))
            path = directory + l1 + '/' + l2 + '/' + l3
            o,e=runcommand('find {0}{1}/{2}/{3} -name original.jpg -exec tar -rvPf /tmp/images.{1}.{2}.{3}.tar "{{}}" \;'.format(directory, l1, l2, l3))
            try:
                shutil.move('/tmp/images.{1}.{2}.{3}.tar'.format(directory, l1, l2, l3), outdir)
            except:
                pass

            count+=o.count('\n')
            error+=e.count('\n')

            curtime=time.time()
            speed=(count-statist["count"])/(curtime-statist["run"])
            statist["run"]=curtime
            statist["count"]=count
            print ("L3 directory completed %s [%s Archived, %s error] speed %if/s runned %is" % (directory + l1 + '/' + l2 + '/' + l3, count, error,speed,time.time()-startedtime))
            sys.stdout.flush()
        print ("L2 directory completed %s [%s Archived, %s error]" % (directory + l1 + '/' + l2, count, error))

