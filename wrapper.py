#!/usr/bin/env python
import time
import sys
from watchgod import watch
from subprocess import Popen

if  len(sys.argv) > 2 :
    filename=sys.argv[1]
    token=sys.argv[2]
else:
    print ('Please, specify a name file to run and bot token')
    sys.exit()
    


p=Popen(['python3', filename, token])

for changes in watch('./'):
   print(changes)
   if any([ './'+filename in i for i in changes]):
      print("stoping!")
      p.terminate()
      time.sleep(10)
      print("stoped")
      p=Popen(['python3', filename,token])