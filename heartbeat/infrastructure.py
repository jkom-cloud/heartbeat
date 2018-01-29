"""基础服务"""
import subprocess
import re

import requests

from heartbeat import credentials

def rabbit(env, timeout=5):
    url = 'http://172.20.20.207:15672/api/connections'
    usr = credentials['rabbit']['usr']
    pwd = credentials['rabbit']['pwd']
    clients = requests.get(url, auth=(usr, pwd), timeout=timeout).json()
    python_clients = [c for c in clients
        if c['client_properties']['platform'][:6] == 'Python'
    ]
    nodejs_clients = [c for c in clients
        if c['client_properties']['platform'][:7] == 'Node.JS'
    ]
    assert len(python_clients) > 0
    assert len(nodejs_clients) > 0

def redis(env, timeout=5):
    if env == 'prod':
        cmd = 'ssh jk@172.20.20.207 docker ps -f name=redis-prod'
    else:
        cmd = 'ssh jk@172.20.20.207 docker ps -f name=redis-test'
    p = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
    assert p.returncode == 0
    lines = p.stdout.decode().split('\n')
    container_id, image, command, created, status, ports, names = re.split(r'\s{2,}', lines[1])
    assert status[:2] == 'Up'
