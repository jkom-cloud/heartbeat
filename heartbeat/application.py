"""应用层服务"""
import subprocess
import re

import requests

def precise_application_interface(env, timeout=5):
    """https://github.com/jkom-cloud/precise-application-interface"""
    if env == 'test':
        url = 'http://172.20.20.207:8080/base-data?type=correlationType-type[report]'
    else:
        url = 'http://172.20.30.202:8080/base-data?type=correlationType-type[report]'
    r = requests.get(url, timeout=timeout)
    resp = r.json()
    assert len(resp['correlationType-type[report]']) > 0

def log_worker(env, timeout=5):
    """https://github.com/jkom-cloud/log-worker"""
    if env == 'prod':
        url = 'http://172.20.20.207:5006/notifications/'
        cmd = 'ssh jk@172.20.20.207 docker ps -f name=log_worker_prod'
    else:
        url = 'http://172.20.20.207:5005/notifications/'
        cmd = 'ssh jk@172.20.20.207 docker ps -f name=log_worker'
    resp = requests.get(url, timeout=timeout).json()
    if resp['total'] >= 10:
        assert len(resp['rows']) == 10
    else:
        assert len(resp['rows']) < 10
    p = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
    assert p.returncode == 0
    lines = p.stdout.decode().split('\n')
    container_id, image, command, created, status, ports, names = re.split(r'\s{2,}', lines[1])
    assert status[:2] == 'Up'
