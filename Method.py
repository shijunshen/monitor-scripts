import re
import time
import select
from Login import Login

root_username = "xxx"


def ReFind(str1, march, start=0):
    """Search all the string find out all the text which fullfill the re

    Args:
        str1 (string): the string which going to be search
        march (Match type of the re.compile()): your re.compile()type
        start (int, optional): start position of the string . Defaults to 0.

    Returns:
        string: all the text which founded
    """
    searchres = march.search(str1, start)
    if searchres is not None:
        TmpResut = searchres.group()
        startPos = searchres.end()
        if startPos < len(str1):
            a = ReFind(str1, march, startPos)
            if a is not None:
                TmpResut += ',' + a
            return TmpResut
        else:
            return TmpResut
    else:
        return None


class CPU(Login):
    def __init__(self, ):
        super(CPU, self).__init__()
        pass

    def cpu_cal(self, ):
        """check out OLT CPU
        action: need check out which value is high and not accepted"""
        cpu_match = 0.0
        self.command('xxx')
        command_line = "xxx"
        output = self.command(command_line)
        patt = r"root\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\w\s+(\d+.\d)"
        cpu1_pattern = re.compile(patt)
        cpu1_match = cpu1_pattern.findall(output)
        if self.debug:
            print("cpu:", cpu1_match)
        for cpu1 in cpu1_match:
            # print(float(cpu1))
            cpu_match += float(cpu1)
        self.ssh2.send(("\003" + "\r").encode('utf-8'))
        time.sleep(1)
        output = self.ssh2.recv(3000)

        clock = re.search(r'\".+\"', str(self.command("xxx")))
        assert clock != None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20]

        if self.debug:
            print("exit: ", output.decode())

        return [cpu_match / 4], clock

    def cpu_cal_card(self, number, ):
        """check out OLT CPU
        action: need check out which value is high and not accepted"""
        cpu_match = 0.0
        self.command('xxx')
        command_line = "xxx"
        output = self.command(command_line)
        patt = r"xxx"
        cpu1_pattern = re.compile(patt)
        cpu1_match = cpu1_pattern.findall(output)
        if self.debug:
            print("cpu:", cpu1_match)
        for cpu1 in cpu1_match:
            # print(float(cpu1))
            cpu_match += float(cpu1)
        self.ssh2.send(("xxx"))
        time.sleep(1)
        output = self.ssh2.recv(3000)
        if self.debug:
            print("exit: ", output.decode())

        clock = re.search(r'\".+\"', str(self.command("xxx")))
        assert clock != None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20]

        return [cpu_match], clock


class Memory(Login):
    def __init__(self, ):
        super(Memory, self).__init__()
        pass

    def mem_cal(self, ):
        """check out OLT memory"""
        mem_match = 0
        command_line = "xxx"
        output = self.command(command_line)
        patt = r"xxx"
        mem1_pattern = re.compile(patt)
        mem1_match = mem1_pattern.findall(output)
        if self.debug:
            print("mem:", mem1_match)
        for mem1 in mem1_match:
            # print(float(mem1))
            mem_match += float(mem1)
        self.ssh2.send(("\003" + "\r").encode('utf-8'))
        time.sleep(1)
        output = self.ssh2.recv(3000)
        if self.debug:
            print("exit: ", output.decode())

        clock = re.search(r'\".+\"', self.command("xxx"))
        assert clock != None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20]

        return [mem_match], clock

    def mem_cal_card(self, number, ):
        """check out OLT memory"""
        mem_match = 0
        command_line = "show info {}".format(number)
        output = self.command(command_line)
        patt = r"xxx"
        mem1_pattern = re.compile(patt)
        mem1_match = mem1_pattern.findall(output)
        if self.debug:
            print("mem:", mem1_match)
        for mem1 in mem1_match:
            # print(float(mem1))
            mem_match += float(mem1)
        self.ssh2.send("xxx")
        time.sleep(1)
        output = self.ssh2.recv(3000)
        if self.debug:
            print("exit: ", output)

        clock = re.search(r'\".+\"', self.command("xxx"))
        assert clock != None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20]

        return [mem_match], clock

    def mem_check_log(self, name):

        command_line = f"xxx"
        output = self.command(command_line)
        if re.search('xxx', output) is not None:
            return 0, 0
        data = output.split('\r\r\n')[-2]
        TIME = data.split(',')[0]
        memory = data.split(',')[1].split()[1]

        return TIME, memory


class Alarm(Login):
    def __init__(self, ):
        super(Alarm, self).__init__()
        pass

    def active_alarm_check(self, ):
        """check active alarm"""
        alarm_label = 'xxx'
        # if self.username == root_username:
        #     self.command('cli')
        self.command('xxx')
        clock = re.search(r'\".+\"', str(self.command("xxx")))
        assert clock != None, "xxx".format(self.ip)
        clock = clock.group()[1:20]
        crital_value = 0
        major_value = 0
        minor_value = 0
        info_value = 0
        command_line = "xxx"
        output = self.command(command_line)
        # print(output.decode())
        if alarm_label in output:
            for line in output.splitlines():
                # print("alarm: {}".format(line))
                if alarm_label in line:
                    alarm_pattern = re.compile("xxx")
                    alarm_match = re.search(alarm_pattern, line)
                    # print('alarm label: ', alarm_match.group(1))
                    if alarm_match.group(1) == 'xxx':
                        crital_value += 1
                    elif alarm_match.group(1) == 'xxx':
                        major_value += 1
                    elif alarm_match.group(1) == 'xxx':
                        minor_value += 1
                    elif alarm_match.group(1) == 'xxx':
                        info_value += 1
                    else:
                        print("xxx")
                else:
                    pass
            # if self.username == root_username:
            #     self.command('exit')
            return [crital_value, major_value, minor_value, info_value], clock
        else:
            print('xxx')
            # if self.username == root_username:
            #     self.command('exit')
            if self.debug:
                print('xxx')
            return False, clock

    def ont_alarm_check(self, ):
        self.command("\n")
        """check active alarm"""
        ont_miss = 'xxx'
        ont_departure = 'xxx'
        clock = re.search(r'\".+\"', str(self.command("xxx")))
        assert clock != None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20]
        ont_miss_value = 0
        ont_departure_value = 0

        command_line = ['xxx']
        for command in command_line:
            output = self.command(command)
            if ont_miss or ont_departure in output:
                for line in output.splitlines():
                    if ont_miss in line or ont_departure in line:
                        alarm_pattern = re.compile("xxx")
                        alarm_match = re.search(alarm_pattern, line)
                        if alarm_match:
                            if alarm_match.group(1) == 'xxx':
                                ont_miss_value += 1
                            if alarm_match.group(1) == 'xxx':
                                ont_departure_value += 1
                            else:
                                pass
                                # print("no missing")
                        else:
                            pass
                    else:
                        pass
                print('miss value: ', ont_miss_value, ont_departure_value)
            else:
                pass
                # print('nothing missing')


            self.command("\n")
        # channel.close()
        return [ont_miss_value, ont_departure_value], clock


class Other(Login):
    def __init__(self, ):
        super(Other, self).__init__()
        pass

    # root cli
    def uptime(self, ):
        """check system uptime"""
        command_line = "xxx"
        output = self.command(command_line)
        uptime_pattern = re.compile("xxx")
        uptime_match = re.search(uptime_pattern, output)
        if self.debug:
            assert uptime_match != None, "IP={}".format(self.ip)
            print("uptime: {}".format(uptime_match.group(1)))

        """check each card uptime"""
        # check cards' number (1 or 2)
        if self.username == root_username:
            self.command("xxx")
        self.command("xxx")
        # get clock
        msg = self.command("xxx")

        # check the cards' number
        temp1 = re.search(r"xxx", msg)
        temp2 = re.search(r"xxx", msg)

        clock = re.search(r'\".+\"', self.command("xxx"))
        assert clock != None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20]

        if self.username == root_username:
            self.debugLogin()

        card1_reboot_times = 0
        card1_reboot_info = 0
        card2_reboot_times = 0
        card2_reboot_info = 0
        if temp1 != None and temp2 != None:
            """there are two cards"""
            msg = self.command("xxx")
            msg = msg.split("\n")[-2].split()
            # login to another card
            sign = self.command("xxx")
            msg_ = self.command("xxx")
            msg_ = msg_.split("\n")[-2].split()

            # check the default login card, sometimes run cli "sshMate" is card1 to card2, and sometimes is card2 to card1
            if re.search("xxx", sign) != None:
                card1_reboot_times = msg[0]
                card1_reboot_info = msg[4]
                card2_reboot_times = msg_[0]
                card2_reboot_info = msg_[4]
            else:
                card1_reboot_times = msg_[0]
                card1_reboot_info = msg_[4]
                card2_reboot_times = msg[0]
                card2_reboot_info = msg[4]
            self.command("xxx")

        else:
            """there is just one card"""
            msg = self.command("xxx")
            msg = msg.split("\n")[-2].split()
            if temp1 != None:
                # only card1
                card1_reboot_times = msg[0]
                card1_reboot_info = msg[4]
            else:
                # only card2
                card2_reboot_times = msg[0]
                card2_reboot_info = msg[4]

        return [uptime_match.group(1)], [card1_reboot_times, card1_reboot_info], [card2_reboot_times,
                                                                                  card2_reboot_info], clock

    def disk_space(self):
        if self.username == root_username:
            self.command("xxx")
        self.command("xxx")
        clock = re.search(r'\".+\"', self.command("xxx"))
        assert clock is not None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20]
        if self.username == root_username:
            self.debugLogin()

        str1 = self.command("xxx")
        tempstr = re.search(r'xxx', str1)
        usage = 0
        if tempstr:
            usage = int(str(tempstr.group()).split()[-1][:-1])
            print(usage)
        return float(usage), clock

    # general cli
    def core_file(self, ):
        """check core file
        action :still need find all for two cards"""
        core_match = 0

        clock = re.search(r'\".+\"', str(self.command("xxx")))
        assert clock != None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20]

        command_line = """xxx"""
        output = self.command(command_line)
        patt = r"xxx"
        core_file_pattern = re.compile(patt)
        core_file_match = core_file_pattern.findall(output)
        if self.debug:
            print("core_file: {}".format(core_file_match))
        for core1 in core_file_match:
            print(core1)
            core_match += int(core1)

        return [core_match], clock

    def crash_process(self, ):
        """check OLT uptime
        name application-restart
        primary-element aemgrd
        dcli arcmgrd dump summary
        df -k"""
        restart = 'xxx'
        clock = re.search(r'\".+\"', str(self.command("xxx")))
        assert clock != None, "xxx".format(self.ip)
        clock = clock.group()[1:20]
        command_line = "xxx"
        output = self.command(command_line)

        if restart in output:
            crash_process_pattern = re.compile(b"xxx")
            crash_process_match = re.search(crash_process_pattern, output)
            if crash_process_match:
                print("crash_process: {}".format(crash_process_match.group(1)))
                return [crash_process_match.group(1)], clock
            else:
                print('nothing matched')
        else:
            if self.debug:
                print('nothing crashed')
            return False, clock

    def real_rate_check(self, ):
        """check active alarm"""
        fixed_rate = 'xxx'
        assured_rate = 'xxx'
        excess_rate = 'xxx'

        clock = re.search(r'\".+\"', str(self.command("xxx")))
        assert clock is not None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20]

        # scan for all pon port
        scan = self.command("xxx")
        pattern = re.compile("xxx")


        pons = ReFind(scan, pattern)
        if pons is not None:
            pons = pons.split(",")
        else:
            return {}, clock

        command_line = []
        for i in range(len(pons)):
            command_line.append("xxx")
        print(command_line)

        fixed_rate_value = []
        assured_rate_value = []
        excess_rate_value = []
        for command in command_line:
            output = self.command(command)
            if fixed_rate in output or assured_rate in output or excess_rate in output:
                for line in output.splitlines():
                    if fixed_rate in line:
                        alarm_pattern = re.compile("xxx")
                        alarm_match = re.search(alarm_pattern, line)
                        if alarm_match:
                            print('xxx ', alarm_match.group(1))
                            fixed_rate_value.append(float(alarm_match.group(1)))
                    elif assured_rate in line:
                        alarm_pattern = re.compile("xxx")
                        alarm_match = re.search(alarm_pattern, line)
                        if alarm_match:
                            print('xxx ', alarm_match.group(1))
                            assured_rate_value.append(float(alarm_match.group(1)))
                    elif excess_rate in line:
                        alarm_pattern = re.compile("xxx")
                        alarm_match = re.search(alarm_pattern, line)
                        if alarm_match:
                            print('xxx', alarm_match.group(1))
                            excess_rate_value.append(float(alarm_match.group(1)))
                    else:
                        pass
                print('xxx')
                print("xxx", fixed_rate_value)
                print("xxx", assured_rate_value)
                print("xxx", excess_rate_value)
            else:
                print('nothing matched')
                if self.debug:
                    print('nothing missing')
                assured_rate_value.append(0.0)
                fixed_rate_value.append(0.0)
                excess_rate_value.append(0.0)
                print('xxx')
                print("xxx", fixed_rate_value)
                print("xxx", assured_rate_value)
                print("xxx", excess_rate_value)


        # dict{  'pon name':[fixed_rate_value, assured_rate_value, excess_rate_value]  }
        pon_value_dict = {}
        for i in range(len(pons)):
            pon_value_dict[pons[i]] = [fixed_rate_value[i],assured_rate_value[i],excess_rate_value[i]]
        print(pon_value_dict)
        self.command('\n')

        return pon_value_dict, clock

    def ont_online(self):
        clock = re.search(r'\".+\"', str(self.command("xxx")))
        assert clock != None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20]
        ont_num = int(str(re.search(r'\w+\-\w+\s+\w+\-\w+\s+\d+',self.command("xxx")).group().split()[-1]))
        aeont_num = int(str(re.search(r'\w+\-\w+\-\w+\s+\w+\-\w+\s+\d+',
                                      self.command("xxx")).group().split()[-1]))
        return [ont_num, aeont_num], clock

    def temperature(self):
        self.command('xxx')
        str1 = self.command('xxx')
        card1 = re.search(r'xxx', str1).group()
        card2 = re.search(r'xxx', str1).group()

        card1 = re.search(r'xxx', card1)
        card2 = re.search(r'xxx', card2)
        card1_sensor_name = []
        card1_temperature = []
        card2_sensor_name = []
        card2_temperature = []
        if card1 != None:
            card1 = card1.group().split('\n')
            for index in range(3, len(card1) - 2):
                temp1 = card1[index].split()
                card1_sensor_name.append(temp1[0])
                card1_temperature.append(float(temp1[1]))
        if card2 != None:
            card2 = card2.group().split('\n')
            for index in range(3, len(card2) - 2):
                temp2 = card2[index].split()
                card2_sensor_name.append(temp2[0])
                card2_temperature.append(float(temp2[1]))
        clock = re.search(r'\".+\"', self.command("xxx"))
        assert clock != None, "xxx".format(self.ip)
        clock = clock.group()[1:20]
        return [card1_sensor_name, card1_temperature], [card2_sensor_name, card2_temperature], clock
