import re
import time
import datetime

from Method import CPU, Memory, Alarm, Other
from Dao import monitor_SQL


class Service(CPU, Memory, Alarm, Other):
    """https://www.jianshu.com/p/a64ad351ebb2
    https://blog.csdn.net/specter11235/article/details/89198032"""

    def __init__(self, ip, port, username, password, dbhost, dbport, dbname, dbuser, dbpwd):
        super(Service, self).__init__()
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

        self.dbhost = dbhost
        self.dbport = dbport
        self.dbname = dbname
        self.dbuser = dbuser
        self.dbpwd = dbpwd

        """the information of Database connection"""
        self.conn = monitor_SQL(host=dbhost, port=dbport, database=dbname, user=dbuser, passwd=dbpwd)
        """initial reboot times information"""

    def initial_uptime(self):
        # clean up_time table
        self.conn.cleanUpTime(self.ip)
        free, card1, card2, clock = self.uptime()

        # Assign the initial value of system startup time which is the time of script startup
        # to facilitate the subsequent calculation of system restart times
        self.conn.addToUpTime(SECONDS=int(free[0]), IP=self.ip, REBOOT=0, TIME=clock,
                              CARD1_REBOOT_TIMES_BEGIN=card1[0], CARD1_REBOOT_INFO=0,
                              CARD2_REBOOT_TIMES_BEGIN=card2[0], CARD2_REBOOT_INFO=0, CARD1_REBOOT_TIMES=0,
                              CARD2_REBOOT_TIMES=0)

    def read_uptime(self, last_uptime, card1_reboot_times_begin, card2_reboot_times_begin, INTERVAL):
        # uptime
        free, card1, card2, clock = self.uptime()
        seconds = free[0]
        # system and card reboot times

        card1_reboot = int(card1[0]) - int(card1_reboot_times_begin)
        card2_reboot = int(card2[0]) - int(card2_reboot_times_begin)

        Info = self.conn.selectFromUpTime(self.ip)[0]
        reboot_times = int(Info['REBOOT_TIMES'])

        # the system reboot
        if (int(seconds) < int(last_uptime) and int(seconds) < INTERVAL):
            reboot_times += 1
            #   when system reboot, the two cards don't start at the same time, so if don't check one more time,
            # the reboot times number will be so big, because the CARD_REBOOT_TIMES_BEGIN has become zero and
            # the "card_reboot = card - card_reboot_times_begin"
            time.sleep(10)
            free, card1, card2, clock = self.uptime()
            seconds = free[0]
            card1_reboot_times_begin = card1[0]
            card2_reboot_times_begin = card2[0]

            # update database
            self.conn.addToUpTime(SECONDS=int(seconds), IP=self.ip, REBOOT=reboot_times, TIME=clock,
                                  CARD1_REBOOT_TIMES=0,
                                  CARD1_REBOOT_INFO=0,
                                  CARD2_REBOOT_TIMES=0,
                                  CARD2_REBOOT_INFO=0,
                                  CARD1_REBOOT_TIMES_BEGIN=card1_reboot_times_begin,
                                  CARD2_REBOOT_TIMES_BEGIN=card2_reboot_times_begin)
            return reboot_times, 0, 0, int(seconds)

        # the system don't reboot but cards do
        elif int(card1[0]) != 0 and int(card2[0]) != 0 and (
                int(card1[0]) > int(card1_reboot_times_begin) or int(card2[0]) > int(card2_reboot_times_begin)):
            self.conn.addToUpTime(SECONDS=int(seconds), IP=self.ip, REBOOT=reboot_times, TIME=clock,
                                  CARD1_REBOOT_TIMES=card1_reboot,
                                  CARD1_REBOOT_INFO=card1[1],
                                  CARD2_REBOOT_TIMES=card2_reboot,
                                  CARD2_REBOOT_INFO=card2[1],
                                  CARD1_REBOOT_TIMES_BEGIN=card1_reboot_times_begin,
                                  CARD2_REBOOT_TIMES_BEGIN=card2_reboot_times_begin)
        else:
            pass
        # system reboot times, card1 reboot times, card2 reboot times
        return reboot_times, card1_reboot, card2_reboot, int(seconds)

    def disk_space_check(self):
        usage, clock = self.disk_space()
        self.conn.addToDiskTotalUse(USE=usage, IP=self.ip, TIME=clock)
        return usage

    # only use in mem_check
    def mem_check_judge(self, TIME, memory, name):
        if TIME == 0 and memory == 0:
            return
        preTIME = self.conn.selectFromMemCheck(self.ip, name)[-1]['TIME']
        if preTIME is None:
            self.conn.addToMemCheck(name, self.ip, TIME, memory)
        else:
            preTIME = preTIME.strftime("%Y-%m-%d %H:%M:%S")
            TIME1 = datetime.datetime.strptime(TIME, "%Y-%m-%d %H:%M:%S")
            preTIME = datetime.datetime.strptime(preTIME, "%Y-%m-%d %H:%M:%S")

            # convert to timestamp to compare
            TIME1 = time.mktime(TIME1.timetuple())
            preTIME = time.mktime(preTIME.timetuple())
            if preTIME < TIME1:
                self.conn.addToMemCheck(name, self.ip, TIME, memory)
            else:
                return

    def mem_check(self, lmd_begin, pon_begin):
        TIME, lmd_memory = self.mem_check_log("lmd")
        self.mem_check_judge(TIME, lmd_memory, "lmd")
        TIME, pon_memory = self.mem_check_log("ponmgrd")
        self.mem_check_judge(TIME, pon_memory, "ponmgrd")

        return float(lmd_memory), float(pon_memory)
        # return (float(lmd_memory) - float(lmd_begin)), (float(pon_memory) - float(pon_begin))

    def read_cpu(self):
        # total memory usage
        free, clock = self.cpu_cal()
        cpu_usage = free[0]
        self.conn.addToCpuTotalUse(CPU=cpu_usage, IP=self.ip, TIME=clock)
        return cpu_usage

    def read_cpu_card(self, number):
        # card cpu usage
        free, clock = self.cpu_cal_card(number, )
        cpu_usage_card = free[0]
        self.conn.addToCpuUseCard(cpu_usage_card, number, self.ip, TIME=clock)
        return cpu_usage_card

    def read_mem(self):
        # total memory usage
        free, clock = self.mem_cal()
        mem_usage = free[0]
        self.conn.addToMemTotalUse(MEM=mem_usage, IP=self.ip, TIME=clock)
        return mem_usage

    def read_mem_card(self, number):
        # card memory usage
        free, clock = self.mem_cal_card(number, )
        mem_usage = free[0]
        self.conn.addToMemUseCard(MEM=mem_usage, CARD=number, IP=self.ip, TIME=clock)

        return mem_usage

    def read_corefile(self):
        # corefile
        free, clock = self.core_file()
        corefile = free[0]
        self.conn.addToCoreFile(COUNT=int(corefile), IP=self.ip, TIME=clock)
        return int(corefile)

    def read_crash(self):
        # crash process
        free, clock = self.crash_process()
        if free:
            crash = free[0]
            if crash:
                print('crash process:', crash)
                self.conn.addToCrash(CRASH=1, IP=self.ip, TIME=clock)
                return 1
            else:
                self.conn.addToCrash(CRASH=0, IP=self.ip, TIME=clock)
                return 0
        else:
            self.conn.addToCrash(CRASH=0, IP=self.ip, TIME=clock)
            return 0

    def alarm_act(self):
        # active alarm
        COUNT, clock = self.active_alarm_check()
        self.conn.addToAlarm(COUNT=COUNT, IP=self.ip, TIME=clock)
        return COUNT

    def ont_action_check(self):
        # ont alarm
        COUNT, clock = self.ont_alarm_check()
        self.conn.addToOntAlarm(COUNT=COUNT, IP=self.ip, TIME=clock)
        return COUNT

    def port_rate_check(self):
        # ont alarm
        rate, clock = self.real_rate_check()
        for key in rate.keys():
            self.conn.addToPortRate(PORT_NAME=key,FIXED_RATE=rate[key][0],ASSURED_RATE=rate[key][1],EXCESS_RATE=rate[key][2], IP=self.ip, TIME=clock)
        return rate

    def ont_online_number(self):
        number, clock = self.ont_online()
        self.conn.addToOntOnLineNumber(COUNT=number, IP=self.ip, TIME=clock)
        return number

    # still not write into DB

    def sensors_temperature(self):
        card1, card2, clock = self.temperature()
        return card1, card2

    def sshclose(self):
        if self.ssh2:
            self.conn.close()
            self.('xxx')
            self.ssh2.close()
            self.ssh.close()
