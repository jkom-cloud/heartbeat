"""数据分析服务"""
import requests
import zerorpc

def pc_jrisk_service(env, timeout=5):
    """https://github.com/jkom-cloud/pc-jrisk-service"""
    if env == 'test':
        url = 'http://172.20.20.207:9001/assessments/models'
    else:
        url = 'http://172.20.20.207:9002/assessments/models'
    r = requests.get(url, timeout=timeout)
    resp = r.json()
    assert len(resp) > 0

def ocr_server(env, timeout=5):
    """https://jkom-git.chinaeast.cloudapp.chinacloudapi.cn/analytics/ocr"""
    if env == 'test':
        url = 'http://42.159.195.125:5000/tasks/abc'
    else:
        url = 'http://42.159.195.125:8000/tasks/abc'
    r = requests.get(url, timeout=timeout)
    assert r.json()['detail'] == 'task not exists'

def pdata(env):
    """https://github.com/jkom-cloud/pdata"""
    c = zerorpc.Client()
    if env == 'test':
        user_id = 90153882
        test_id = 16545
        url = 'tcp://172.20.20.207:4242'
    else:
        user_id = 90153882
        test_id = 1928
        url = 'tcp://172.20.30.202:4242'
    c.connect(url)
    assert '鼓楼' in c.get_test_data(user_id, test_id)['source']
