from time import sleep
import calculator
from prometheus_client import Gauge, start_http_server
import threading

gauge_uptime = Gauge("uptime", "uptime value")
gauge_restapi_availability = Gauge("restapi_availability", "uptime value")
gauge_gateway_availability = Gauge("gateway_availability", "uptime value")
gauge_nginix_availability = Gauge("nginix_availability", "uptime value")
gauge_internet_connection = Gauge("internet_connection", "uptime value")
gauge_dns_check = Gauge("dns_check", "uptime value")

def run_forever(metric):
    while True:
        getattr(
            calculator, f"cal_{metric._name}")(metric)
        sleep(1)


if __name__ == '__main__':
    start_http_server(9999)
    threading.Thread(target=run_forever,
                     args=(gauge_restapi_availability,)).start()
    threading.Thread(target=run_forever,
                     args=(gauge_uptime,)).start()
    threading.Thread(target=run_forever,
                     args=(gauge_gateway_availability,)).start()
    threading.Thread(target=run_forever,
                     args=(gauge_nginix_availability,)).start()
    threading.Thread(target=run_forever,
                     args=(gauge_internet_connection,)).start()  
    ding.Thread(target=run_forever,
                     args=(gauge_dns_check,)).start()
    while True:
        sleep(2)
