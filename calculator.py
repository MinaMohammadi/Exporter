from icmplib import ping
import requests
import ctypes
import struct
import urllib.request
import socket



def cal_uptime(metric):
    libc = ctypes.CDLL('libc.so.6')
    buf = ctypes.create_string_buffer(4096)  # generous buffer to hold
    # struct sysinfo
    if libc.sysinfo(buf) != 0:
        print('failed')
        metric.set(-1)
        return

    uptime = struct.unpack_from('@l', buf.raw)[0]
    metric.set(uptime)
    return


def cal_restapi_availability(metric):
    REST_API_ENDPOINT = "https://api.bukhara-chkh.ir/user"

    test_phb_data = {
        "phoneNumber": "989222222222",
        "username": "test"
    }

    try:
        resp = requests.post(
            f"{REST_API_ENDPOINT}/insert", test_phb_data, timeout=3)
        if resp.status_code != 200 and resp.status_code != 400:
            metric.set(0)
            return
    except Exception as e:
        metric.set(0)
        return

    try:
        resp = requests.delete(
            f"{REST_API_ENDPOINT}/delete", data=test_phb_data, timeout=3)
        if resp.status_code != 200:
            metric.set(0)
            return
    except Exception as e:
        metric.set(0)
        return
    metric.set(1)


def cal_gateway_availability(metric):
    GATEWAY_ADDR = "192.168.0.232"
    res = ping(GATEWAY_ADDR, interval=0.5, privileged=False)
    metric.set(res.is_alive)


def cal_nginix_availability(metric):
    Nginix_ADDR = "192.168.0.202"
    ngx = ping(Nginix_ADDR, interval=0.5, privileged=False)
    metric.set(ngx.is_alive)

def cal_internet_connection(metric):
    internet= urllib.request.urlopen('http://google.com') 

    metric.set(internet.is_alive)
        
    
def cal_dns_check(metric):
    hostname= "http://bukhara-chkh.ir"
    dns= socket.gethostbyname(hostname)  

    metric.set(dns)

