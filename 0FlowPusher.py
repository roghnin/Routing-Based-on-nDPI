import httplib
import json
import time
 
class StaticFlowPusher(object):
 
    def __init__(self, server):
        self.server = server
 
    def get(self, data):
        ret = self.rest_call({}, 'GET')
        return json.loads(ret[2])
 
    def set(self, data):
        ret = self.rest_call(data, 'POST')
        return ret[0] == 200
 
    def remove(self, objtype, data):
        ret = self.rest_call(data, 'DELETE')
        return ret[0] == 200
 
    def rest_call(self, data, action):
        path = '/wm/staticflowpusher/json'
        headers = {
            'Content_type': 'application/json',
            'Accept': 'application/json',
            }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        print ret
        conn.close()
        return ret
        
def remain(min):
    count = 0
    while (count < min):
        count += 1
        n = min - count
        time.sleep(1)
        out="%04d"%n
        print "\r\r\r"+out


timeout=40
pusher=StaticFlowPusher('127.0.0.1')
flow1={
    "eth_type":"0x0800",
    "cookie":"0",
    "priority":"32768",
    "active":"true",
    "hard_timeout":str(timeout),
    "name":"flow_mod_1",
    "switch":"00:00:00:00:00:00:00:01",
    "ipv4_src":"10.0.0.1",
    "ipv4_dst":"10.0.0.2",
    "actions":""
    }

pusher.set(flow1)
remain(timeout)
