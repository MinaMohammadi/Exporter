import time
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
import psutil
import time


class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):
        g = GaugeMetricFamily("uptime", 'Help text', labels=['target'])

        uptime= time.time() - psutil.boot_time()

        g.add_metric(["target"], uptime)
        
        yield g

        


if __name__ == '__main__':
    start_http_server(9100)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(1)