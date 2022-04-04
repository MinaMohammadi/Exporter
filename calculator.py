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

def cal_nginx_availability(metric):
    NGINX_ADDR = os.environ.get("NGINX_ADDR")
    res = urllib.request.urlopen(NGINX_ADDR)

    metric.set(res.status == 200)


def cal_internet_connection(metric):
    EXTERNAL_ADDR = os.environ.get("EXTERNAL_ADDR")
    res = urllib.request.urlopen(EXTERNAL_ADDR)

    metric.set(res.status == 200)


def cal_dns_check(metric):
    DNS_ADDR = os.environ.get("DNS_ADDR")
    DNS_IP = os.environ.get("DNS_IP")
    ip = socket.gethostbyname(DNS_ADDR)

    metric.set(ip == DNS_IP)
