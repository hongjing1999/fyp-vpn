import os
import sys


import pexpect

def run_command():
    os.chdir("algo")
    print(os.getcwd())
    algo = pexpect.spawn('sh script.sh')
    algo.logfile = sys.stdout.buffer
    algo.expect(b'Server address prompt]\r\nSelect the server to update user list below:\r\n    1. 178.128.102.222')
    algo.sendline("1")
    # algo.expect(b'Enter the password for the private CA key')
    # algo.sendline("PJqHgnehb7qnMdik")
    algo.expect(pexpect.EOF, timeout=None)
    algo.close()
    print(algo.exitstatus, algo.signalstatus)
    os.chdir("..")
    print(os.getcwd())




