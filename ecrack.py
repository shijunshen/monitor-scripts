def crack():
    pass


if __name__ == '__main__':
    info = 'XG801-West-Lake Tue Sep 06 15:17:32 2022'
    crack_info = info.split()
    # use ecrack.py to get the password
    date = crack_info[1:6]
    hostId = crack_info[0]
    print(crack(date,hostId)[0])

