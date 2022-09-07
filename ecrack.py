def crack():
    pass


if __name__ == '__main__':
    info = 'xxx'
    crack_info = info.split()
    # use ecrack.py to get the password
    date = crack_info[1:6]
    hostId = crack_info[0]
    print(crack(date,hostId)[0])

