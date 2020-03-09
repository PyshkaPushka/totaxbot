#!/usr/bin/env python
import time
from watchgod import watch
from subprocess import Popen
p=Popen(['python3', 'devbot.py'])

for changes in watch('./'):
   print(changes)
   if any([ './devbot.py' in i for i in changes]):
      print("stoping!")
      p.terminate()
      time.sleep(10)
      print("stoped")
      p=Popen(['python3', 'devbot.py'])