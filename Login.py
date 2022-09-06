import time
import paramiko
import select

from ecrack import crack
import re


class Login:
    def __init__(self):
        self.ssh = None
        self.ssh2 = None
        self.ip = None
        self.port = None
        self.username = None
        self.password = None
        self.debug = True
        self.cli_finish_flag = None
        self.timer = 10000000

    # debug mode login
    def debugLogin(self):
        output = str(self.command("shell"))
        crack_info = re.search(r"\S+\s\w+\s\w+\s\w+\d+\s[\d:]+\s\d+", output)
        assert crack_info != None, "ip={}：'root' login failed!! Can't match the string used for ecrack.py".format(
            self.ip)
        crack_info = crack_info.group().split()
        # use ecrack.py to get the password
        date = crack_info[1:6]
        hostId = crack_info[0]
        pwd = crack(date=date, hostId=hostId)
        assert len(pwd) == 1, "ip={}：'root' login failed!! len(pwd) > 1, which has not been processed yet".format(
            self.ip)
        pwd = pwd[0]
        self.command(pwd)

    def change_config(self):
        # Skip initial msg
        output = self.command("xxx")
        pattern = r"xxx"
        match = re.search(pattern, output)
        if match == None:
            return None
        else:
            pre_config = match.group().split()[2]
            if pre_config == "xxx":
                self.command("xxx")
                self.command("xxx")
                self.command("xxx")
                return pre_config
            return None

    def change_config_back(self, pre_config):
        if pre_config != None:
            self.command("xxx")
            self.command("xxx" + str(pre_config))
            self.command("xxx")
        else:
            pass

    def check_olt_cpu(self, ):
        """SSH main"""
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.ip, self.port, self.username, self.password)
        self.ssh2 = self.ssh.invoke_shell()
        self.ssh2.send(b"\n")

        # get the finish flag of each command
        time.sleep(10)
        output = str(self.ssh2.recv(999999999),encoding='utf-8')

        print(output)
        temp = re.search('ssh on \S+',output)
        temp = temp.group().split()[-1]
        self.cli_finish_flag = [temp + "#", "root@" + temp, "Enter xxxsupport role password"]
        print(self.cli_finish_flag)

        return self.ssh2

    def command(self, command_line):
        """CLI command running"""
        for com in command_line.splitlines():
            if self.debug:
                print(f"com {self.ip}: ", com)

            self.ssh2.send(com + "\n")
            output = ""

            # avoid endless loop
            timer = self.timer
            while timer:
                rl, wl, xl = select.select([self.ssh2], [], [], 0.0)
                if len(rl) > 0:
                    recv = str(self.ssh2.recv(9999999), encoding='utf-8')
                    output += recv
                    # if finish flag exists , then break
                    if len([x for x in self.cli_finish_flag if x in recv]) != 0:
                        break
                    if com == 'exit':
                        time.sleep(1)
                        recv = str(self.ssh2.recv(9999999), encoding='utf-8')
                        break
                    timer = self.timer
                timer -= 1
            if timer == 0:
                self.ssh2.close()
                self.ssh.close()
                assert False,self.ip+'The remote server is not responding……'
            print(output.replace('\r',''))
            return output

