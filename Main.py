# -*- coding: utf-8 -*-
# coding: utf-8
# Date ：2022/01/07
# https://github.com/prometheus/client_python#gauge
# __author__ = 'Maojun Wang'


import yaml
from Prometheus import Prometheus
from Run_script import Run_script

"""macro definition"""
file = open('config.yaml', 'r', encoding="utf-8")
ISROOT = bool(yaml.load(file, Loader=yaml.FullLoader)['ISROOT'])  # the login permission
#   continuous use "yaml.load" twice will cause the second result is none, because the cursor
# has went to the end of the file, you should exec "file.seek(0)" to return the cursor to begining
file.seek(0)
INTERVAL = (yaml.load(file, Loader=yaml.FullLoader)['INTERVAL'])

"""configure and run prometheus server"""
server = Prometheus(value=404, hport=5000)
server.run_server()
Run_script(ISROOT=ISROOT, INTERVAL=INTERVAL, server=server).run()
