import psutil
def getInfo():
    info = {}
    info['cpu'] = psutil.cpu_percent()
    info['mem'] = round(psutil.virtual_memory().used / (1024 * 1024 * 1024))
    info['temp-cpu'] = psutil.sensors_temperatures()['coretemp'][1][1]
    #psutil.net_connections()
    return info
