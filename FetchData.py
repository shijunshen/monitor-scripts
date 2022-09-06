import re
import time

from Service import Service

root_username = "xxxsupport"


class FetchData(Service):
    def __init__(self, ip, port, username, password, dbhost, dbport, dbname, dbuser, dbpwd):
        super(FetchData, self).__init__(ip, port, username, password, dbhost, dbport, dbname, dbuser, dbpwd)

    # root permisson cli
    def root_cli(self, server, initial, INTERVAL):
        # get the initial data
        if initial:
            self.initial_uptime()


        Info = self.conn.selectFromUpTime(self.ip)[0]
        last_uptime = Info['UPTIME']
        card1_begin = Info['CARD1_REBOOT_TIMES_BEGIN']
        card2_begin = Info['CARD2_REBOOT_TIMES_BEGIN']
        sys_reboot, card1_reboot, card2_reboot, last_uptime = self.read_uptime(last_uptime, card1_begin, card2_begin,
                                                                               INTERVAL)

        server.reboot_times.labels(IP=self.ip, mode='system_{}'.format(self.ip)).set(sys_reboot)
        server.reboot_times.labels(IP=self.ip, mode='card1_{}'.format(self.ip)).set(card1_reboot)
        server.reboot_times.labels(IP=self.ip, mode='card2_{}'.format(self.ip)).set(card2_reboot)

        disk = self.disk_space_check()
        server.disk_usage.labels(IP=self.ip, mode='disk_usage_{}'.format(self.ip)).set(disk)

        temp = self.conn.selectFromMemCheck(self.ip, "lmd")
        temp1 = self.conn.selectFromMemCheck(self.ip, "ponmgrd")
        if temp is None:
            lmd_begin = 0
        else:
            lmd_begin = temp[0]['MEM']
        if temp1 is None:
            ponmgrd_begin = 0
        else:
            ponmgrd_begin = temp1[0]['MEM']
        lmd, ponmgrd = self.mem_check(lmd_begin, ponmgrd_begin)
        server.main_process_mem.labels(IP=self.ip, mode='xxxx'.format(self.ip)).set(lmd)
        server.main_process_mem.labels(IP=self.ip, mode='xxx'.format(self.ip)).set(ponmgrd)

    # general permisson cli
    def general_cli(self, server):
        if self.username == root_username:
            self.command('xxx')
        self.command("xxx")


        cpu_value = self.read_cpu() / 100
        server.cpu_usage.labels(IP=self.ip, mode='system_{}'.format(self.ip)).set(cpu_value)
        cpu_value_card1 = self.read_cpu_card('1/1') / 100
        server.cpu_usage.labels(IP=self.ip, mode='card1_{}'.format(self.ip)).set(cpu_value_card1)
        cpu_value_card2 = self.read_cpu_card('1/2') / 100
        server.cpu_usage.labels(IP=self.ip, mode='card2_{}'.format(self.ip)).set(cpu_value_card2)
        mem_value = self.read_mem() / 100
        server.mem_usage.labels(IP=self.ip, mode='system_{}'.format(self.ip)).set(mem_value)
        mem_value_card1 = self.read_mem_card('1/1') / 100
        server.mem_usage.labels(IP=self.ip, mode='card1_{}'.format(self.ip)).set(mem_value_card1)
        mem_value_card2 = self.read_mem_card('1/2') / 100
        server.mem_usage.labels(IP=self.ip, mode='card2_{}'.format(self.ip)).set(mem_value_card2)
        core_file_value = self.read_corefile()
        server.core_file_times.labels(IP=self.ip, mode='system_{}'.format(self.ip)).set(core_file_value)
        crash_value = self.read_crash()
        server.crash_process.labels(IP=self.ip, mode='system_{}'.format(self.ip)).set(crash_value)
        critical_value, major_value, minor_value, info_value = self.alarm_act()
        server.alarm_active.labels(IP=self.ip, mode='alarm_critical_{}'.format(self.ip)).set(critical_value)
        server.alarm_active.labels(IP=self.ip, mode='alarm_major_{}'.format(self.ip)).set(major_value)
        server.alarm_active.labels(IP=self.ip, mode='alarm_minor_{}'.format(self.ip)).set(minor_value)
        server.alarm_active.labels(IP=self.ip, mode='alarm_info_{}'.format(self.ip)).set(info_value)
        ont_missing, ont_departure = self.ont_action_check()
        server.ont_active.labels(IP=self.ip, mode='ont_missing_{}'.format(self.ip)).set(ont_missing)
        server.ont_active.labels(IP=self.ip, mode='ont_departure_{}'.format(self.ip)).set(ont_departure)
        pon_rate = self.port_rate_check()
        for key in pon_rate.keys():
            server.port_rate.labels(IP=self.ip, port_name=key, rate_type='fixed_rate').set(pon_rate[key][0])
            server.port_rate.labels(IP=self.ip, port_name=key, rate_type='assured_rate').set(pon_rate[key][1])
            server.port_rate.labels(IP=self.ip, port_name=key, rate_type='excess_rate').set(pon_rate[key][2])
        ont_number, aeont_number = self.ont_online_number()
        server.ont_online_num.labels(IP=self.ip, mode='ont_online_num_{}'.format(self.ip)).set(ont_number)
        server.ont_online_num.labels(IP=self.ip, mode='aeont_online_num_{}'.format(self.ip)).set(aeont_number)
        # sensor temperature begin
        card1, card2 = self.sensors_temperature()
        if len(card1) > 0:
            for i in range(0, len(card1[0])):
                server.sensors_temp.labels(IP=self.ip, mode='card1 ' + card1[0][i]).set(card1[1][i])
        if len(card2) > 0:
            for i in range(0, len(card2[0])):
                server.sensors_temp.labels(IP=self.ip, mode='card2 ' + card2[0][i]).set(card2[1][i])
        # sensor temperature end
