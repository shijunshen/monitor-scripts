import re

import yaml
import threading
import time
from Dao import monitor_SQL
# global olt
from SSH import login


class Run_script:
    def __init__(self, ISROOT, INTERVAL, server):
        self.ISROOT = ISROOT
        self.INTERVAL = INTERVAL
        self.server = server

    # script loop
    def loop_run(self, ip, port, initial):
        print('session ip list: ', ip)
        """use username and psw to login and SSH link"""
        fetch, username = login(ISROOT=self.ISROOT, ip=ip, port=port)
        if self.ISROOT:
            # flag of config changed
            pre_config = None
            # test whether can login in the debug mood
            fetch.command('\n')
            output = fetch.command("xxx")
            fetch.command('\n')
            # can't login in the debug mood, need to change config
            if re.search(r"error", output) is not None:
                pre_config = fetch.change_config()
                fetch.sshclose()
                fetch, username = login(ISROOT=self.ISROOT, ip=ip, port=port)
                fetch.command('\n')
            # login in the debug mood again after change the config
            fetch.debugLogin()
            """Fetch data begin"""

            fetch.root_cli(server=self.server, initial=initial, INTERVAL=self.INTERVAL)
            fetch.general_cli(server=self.server)
            if pre_config is not None:
                fetch.change_config_back(pre_config=pre_config)
        else:
            fetch.general_cli(server=self.server)
        """close SSH link"""
        fetch.sshclose()

    def run(self):
        # the ips needed to be connected
        file = open('config.yaml', 'r', encoding="utf-8")
        milan_dict = yaml.load(file, Loader=yaml.FullLoader)['ips']
        print(milan_dict)
        print(milan_dict.keys())

        # check the program that weather it is first time start
        initial = True

        # after every loop, the script auto ssh all the ip again to avoid some of them disconnect
        while True:

            # clean the thread pool
            l = []
            count = 0

            # create the thread pool
            for ip, port in milan_dict.items():
                t = threading.Thread(target=self.loop_run, args=(ip, port, initial))
                l.append(t)

            # thread start
            for t in l:
                t.start()
                count += 1

            # thread synchronized
            for t in l:
                t.join()

            initial = False
            print(f'script pause for {self.INTERVAL} seconds, please waiting.......................')
            time.sleep(self.INTERVAL)
