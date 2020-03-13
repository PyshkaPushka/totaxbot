#!/usr/bin/env python
import time
import sys
from watchgod import watch
from subprocess import Popen
import subprocess


if  len(sys.argv) > 2 :
    filename=sys.argv[1]
    token=sys.argv[2]
else:
    print ('Please specify a file name to run and a Bot API token')
    sys.exit()
    
p=Popen(['python3', filename, token])

for changes in watch('./'):
   print(changes)
   if any([ './'+filename in i for i in changes]):
      print("stoping!")
      p.terminate()
      try:
        p.wait(timeout=10)
      except subprocess.TimeoutExpired:
        print("The process is still alive, kill it!")
        p.kill()
        p.wait()
      time.sleep(5) 
      print("stoped")
      p=Popen(['python3', filename, token])
