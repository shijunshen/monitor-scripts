from FetchData import FetchData
import yaml


def login(ISROOT, ip, port):
    # check the database config from yaml
    file = open('config.yaml', 'r', encoding="utf-8")
    dbinfo = yaml.load(file, Loader=yaml.FullLoader)['database']
    dbhost = dbinfo['host']
    dbport = dbinfo['port']
    dbname = dbinfo['db_name']
    dbuser = dbinfo['user']
    dbpwd = dbinfo['password']

    # root permissions login
    if ISROOT:
        username = 'xxxsupport'
        password = 'xxxsupport'
    # non root permissions login
    else:
        if ip in ['10.245.46.207', '10.245.46.218']:
            username = 'xxx'
            password = 'xxx'
        else:
            username = 'xxx'
            password = 'xxx'

    """ssh Link and Mysql DB Link"""
    fetch = FetchData(ip, port, username, password, dbhost=dbhost, dbport=dbport, dbname=dbname, dbuser=dbuser,
                      dbpwd=dbpwd)
    fetch.check_olt_cpu()
    return fetch, username
