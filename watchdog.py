#!/usr/bin/env python
import time, sys, os.path
from subprocess import Popen, TimeoutExpired

if len(sys.argv) > 2:
    filename = sys.argv[1]
    update_mark = sys.argv[2]
else:
    print('Arguments: <PyProgram> <UpdateMarkFileName>')
    sys.exit()


def run_python():
    print("Starting")
    return Popen(['python3', filename])


def check_for_update(p):
    if os.path.isfile(update_mark):
        print("Update exists")
        os.remove(update_mark)
        print("Stopping!")
        p.terminate()
        try:
            p.wait(timeout=10)
        except TimeoutExpired:
            print("The process is still alive, kill it!")
            p.kill()
            p.wait()
        time.sleep(5)
        print("Stopped")


while True:
    p = run_python()

    while p.poll() is None:
        check_for_update(p)
        time.sleep(1)