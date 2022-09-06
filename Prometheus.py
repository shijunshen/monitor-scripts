from prometheus_client import Gauge, start_http_server

class Prometheus:
    def __init__(self,value,hport):
        self.value = value
        self.hport = hport

        # initial dashboard
        self.cpu_usage = Gauge('cpu_usage', 'CPU USAGE', ['IP', 'mode'])
        self.mem_usage = Gauge('mem_usage', 'MEM USAGE', ['IP', 'mode'])
        self.core_file_times = Gauge('corefile', 'corefile times', ['IP', 'mode'])
        self.crash_process = Gauge('crash_process', 'CRASH process', ['IP', 'mode'])
        self.alarm_active = Gauge('alarm_active', 'alarm active', ['IP', 'mode'])
        self.ont_active = Gauge('ont_active', 'alarm event ont', ['IP', 'mode'])
        self.port_rate = Gauge('port_rate', 'all port rates', ['IP', 'port_name', 'rate_type'])
        self.ont_online_num = Gauge('ont_online_num', 'ONT ONLINE NUM', ['IP', 'mode'])
        self.disk_usage = Gauge('disk_usage', 'DISK USAGE', ['IP', 'mode'])
        self.sensors_temp = Gauge('sensors_temperature', 'SENSORS TEMPERATURE', ['IP', 'mode'])
        self.reboot_times = Gauge('reboot_times', 'REBOOT TIMES', ['IP', 'mode'])
        self.main_process_mem = Gauge('main_process_mem','MAIN PROCESS MEM',['IP','mode'])

    def run_server(self):
        # Gauge monitor items，http_code，only inis once or it'll report“ValueError：Duplicated timeseries in
        # CollectorRegistry”
        http_code = Gauge('http_code', 'HTTP CODE')
        http_code.set(self.value)

        # start http server
        start_http_server(self.hport)