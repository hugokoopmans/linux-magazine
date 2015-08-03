# get utc timestamp
    rightnow = time.time()
    utc = datetime.datetime.utcfromtimestamp(int(rightnow)) # int voor seconden
