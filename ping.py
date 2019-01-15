#_*_ coding:utf8 _*_

import re
import subprocess
import sys


def check_alive(ip, count=1, timeout=1):
    cmd = 'ping -c %d -w %d %s' % (count, timeout, ip)

    p = subprocess.Popen(cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
    )

    result = p.stdout.read()
    regex = re.findall('100% packet loss', result)
    if len(regex) == 0:
        print("conn %s" % ip)
    else:
        print("uncon %s" % ip)


def main():
    with open('/root/ip.txt', 'r') as f:
        for line in f.readlines():
            ip = line.strip()
            check_alive(ip)


if __name__ == "__main__":
    sys.exit(main())
