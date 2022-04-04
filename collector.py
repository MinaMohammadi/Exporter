from time import sleep
import calculator
from prometheus_client import Gauge, start_http_server
from threading import Thread

metrics = [
    Gauge("uptime", "server uptime"),
    Gauge("restapi_availability", "rest api is availiable from external network"),
    Gauge("gateway_accessibility", "gateway is accessable from external network"),
    Gauge("nginx_availability", "nginx server is availiable from external network"),
    Gauge("internet_connection", "access of host to internet"),
    Gauge("dns_check", "dns server can resolve address")
]


def run_forever(metric):
    while True:
        getattr(
            calculator, f"cal_{metric._name}")(metric)
        sleep(1)


if __name__ == '__main__':
    for metric in metrics:
        Thread(target=run_forever,
               args=(metric,)).start()

    start_http_server(9110)

    while True:
        sleep(2)
