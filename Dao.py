import pymysql

class monitor_SQL:
    def __init__(self,host,port,database,user,passwd):
        self.conn = pymysql.connect(
            host=host,
            port=port,
            database=database,
            charset="utf8",
            user=user,
            passwd=passwd
        )

    """initial clean tables"""
    def cleanUpTime(self,IP):
        try:
            with self.conn.cursor() as cursor:
                sql = f"delete from up_time where IP='{IP}';"
                cursor.execute(sql)
                self.conn.commit()
                print("clean uptime table successfully")
        except Exception as e:
            self.conn.rollback()
            print("clean up_time failed")

    """write to DB"""
    def addToCpuTotalUse(self,CPU,IP,TIME):
        try:
            with self.conn.cursor() as cursor:
                sql = f"insert into cpu_total_use (CPU,IP,TIME) value {CPU,IP,TIME};"
                cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("add to cpu_total_time failed")

    def addToMemTotalUse(self,MEM,IP,TIME):
        try:
            with self.conn.cursor() as cursor:
                sql = f"insert into mem_total_use (MEM,IP,TIME) value {MEM,IP,TIME};"
                cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("add to mem_total_time failed")

    def addToCpuUseCard(self,CPU,CARD,IP,TIME):
        try:
            with self.conn.cursor() as cursor:
                sql = f"insert into cpu_use_card (CPU,CARD,IP,TIME) value {CPU,CARD,IP,TIME};"
                cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("add to cpu_use_card failed")

    def addToMemUseCard(self,MEM,CARD,IP,TIME):
        try:
            with self.conn.cursor() as cursor:
                sql = f"insert into mem_use_card (MEM,CARD,IP,TIME) value {MEM,CARD,IP,TIME};"
                cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("add to mem_use_card failed")

    def addToCrash(self,CRASH,IP,TIME):
        try:
            with self.conn.cursor() as cursor:
                sql = f"insert into crash (CRASH,IP,TIME) value {CRASH,IP,TIME};"
                cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("add to crash failed")

    def addToAlarm(self,COUNT,IP,TIME):
        critical_value, major_value, minor_value, info_value = COUNT
        try:
            with self.conn.cursor() as cursor:
                sql = f"insert into alarm (CRITICAL,MAJOR,MINOR,INFO,IP,TIME) value {critical_value,major_value,minor_value,info_value,IP,TIME};"
                cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("add to alarm failed")

    def addToOntAlarm(self,COUNT,IP,TIME):
        ont_missing, ont_departure = COUNT
        try:
            with self.conn.cursor() as cursor:
                sql = f"insert into ont_alarm (ONT_MISSING,ONT_DEPARTURE,IP,TIME) value {ont_missing,ont_departure,IP,TIME};"
                cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("add to ont_alarm failed")

    def addToPortRate(self,PORT_NAME,FIXED_RATE,ASSURED_RATE,EXCESS_RATE,IP,TIME):
        try:
            with self.conn.cursor() as cursor:
                sql = f"insert into port_rate (PORT_NAME,FIXED_RATE,ASSURED_RATE,EXCESS_RATE,IP,TIME) value {PORT_NAME,FIXED_RATE,ASSURED_RATE,EXCESS_RATE,IP,TIME};"
                cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("add to port_rate failed")

    def addToCoreFile(self,COUNT,IP,TIME):
        try:
            with self.conn.cursor() as cursor:
                sql = f"insert into core_file (CORE_FILE,IP,TIME) value {COUNT,IP,TIME};"
                cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("add to core_file failed")

    def addToUpTime(self,SECONDS,IP,REBOOT,TIME,CARD1_REBOOT_TIMES,CARD1_REBOOT_INFO,CARD2_REBOOT_TIMES,CARD2_REBOOT_INFO,CARD1_REBOOT_TIMES_BEGIN,CARD2_REBOOT_TIMES_BEGIN):
        try:
            with self.conn.cursor() as cursor:
                sql = "select * from up_time where ip='{}'".format(IP)
                cursor.execute(sql)
                data = cursor.fetchall()
                if len(data) == 0:
                    sql = f"insert into up_time (UPTIME,IP,REBOOT_TIMES,TIME,CARD1_REBOOT_TIMES,CARD1_REBOOT_INFO,CARD2_REBOOT_TIMES,CARD2_REBOOT_INFO,CARD1_REBOOT_TIMES_BEGIN,CARD2_REBOOT_TIMES_BEGIN) value {SECONDS,IP,REBOOT,TIME,CARD1_REBOOT_TIMES,CARD1_REBOOT_INFO,CARD2_REBOOT_TIMES,CARD2_REBOOT_INFO,CARD1_REBOOT_TIMES_BEGIN,CARD2_REBOOT_TIMES_BEGIN};"
                    cursor.execute(sql)
                else:
                    sql = "update up_time set UPTIME='{}',REBOOT_TIMES='{}',TIME='{}',CARD1_REBOOT_TIMES='{}',CARD1_REBOOT_INFO='{}',CARD2_REBOOT_TIMES='{}',CARD2_REBOOT_INFO='{}',CARD1_REBOOT_TIMES_BEGIN='{}',CARD2_REBOOT_TIMES_BEGIN='{}' where IP='{}'".format(SECONDS,REBOOT,TIME,CARD1_REBOOT_TIMES,CARD1_REBOOT_INFO,CARD2_REBOOT_TIMES,CARD2_REBOOT_INFO,CARD1_REBOOT_TIMES_BEGIN,CARD2_REBOOT_TIMES_BEGIN,IP)
                    cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("add to up_time failed")

    def addToOntOnLineNumber(self,COUNT,IP,TIME):
        try:
            with self.conn.cursor() as cursor:
                sql = f"insert into ont_on_line_number (ONT,AEONT,IP,TIME) value {COUNT[0],COUNT[1],IP,TIME};"
                cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("add to ont_on_line_number failed")

    def addToDiskTotalUse(self,USE,IP,TIME):
        try:
            with self.conn.cursor() as cursor:
                sql = f"insert into disk_total_use (DISK,IP,TIME) value {USE,IP,TIME};"
                cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("add to disk_total_use failed")

    def addToMemCheck(self,NAME,IP,TIME,MEM):
        try:
            with self.conn.cursor() as cursor:
                sql = f"insert into mem_check (NAME,IP,TIME,MEM) value {NAME,IP,TIME,MEM};"
                cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("add to mem_check failed")

    """read from DB"""
    def selectFromCpuTotalUse(self):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "select * from cpu_total_use"
                cursor.execute(sql)
                info = cursor.fetchall()
                return info
        except Exception as e:
            self.conn.rollback()
            print("read from cpu_total_use failed")

    def selectFromMemTotalUse(self):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "select * from mem_total_use"
                cursor.execute(sql)
                info = cursor.fetchall()
                return info
        except Exception as e:
            self.conn.rollback()
            print("read from mem_total_use failed")

    def selectFromCrash(self):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "select * from crash"
                cursor.execute(sql)
                info = cursor.fetchall()
                return info
        except Exception as e:
            self.conn.rollback()
            print("read from crash failed")

    def selectFromAlarm(self):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "select * from alarm"
                cursor.execute(sql)
                info = cursor.fetchall()
                return info
        except Exception as e:
            self.conn.rollback()
            print("read from alarm failed")

    def selectFromOntAlarm(self):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "select * from ont_alarm"
                cursor.execute(sql)
                info = cursor.fetchall()
                return info
        except Exception as e:
            self.conn.rollback()
            print("read from ont_alarm failed")

    def selectFromPortRate(self):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "select * from port_rate"
                cursor.execute(sql)
                info = cursor.fetchall()
                return info
        except Exception as e:
            self.conn.rollback()
            print("read from port_rate failed")

    def selectFromCoreFile(self):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "select * from core_file"
                cursor.execute(sql)
                info = cursor.fetchall()
                return info
        except Exception as e:
            self.conn.rollback()
            print("read from core_file failed")

    def selectFromUpTime(self,ip):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "select REBOOT_TIMES from up_time where IP='{}'".format(ip)
                cursor.execute(sql)
                REBOOT_TIMES = cursor.fetchall()
                if len(REBOOT_TIMES) == 0:
                    return [{'REBOOT_TIMES':0,'UPTIME':0,'CARD1_REBOOT_TIMES':0,'CARD2_REBOOT_TIMES':0}]

                sql = "select * from up_time where IP='{}'".format(ip)
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        except Exception as e:
            self.conn.rollback()
            print(ip + " read from up_times failed")

    def selectFromMemCheck(self,ip,name):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "select * from mem_check where IP='{}' and name='{}'".format(ip,name)
                cursor.execute(sql)
                result = cursor.fetchall()
                if len(result) == 0:
                    return None
                return result
        except Exception as e:
            self.conn.rollback()
            print(ip + " read from mem_check failed")


    """close DB link"""
    def close(self):
        self.conn.close()
