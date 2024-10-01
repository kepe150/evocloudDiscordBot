import psutil
def getInfo():
    info = {}
    info['cpu'] = psutil.cpu_percent()
    info['mem'] = round(psutil.virtual_memory().used / (1024 * 1024 * 1024))
    info['test'] = psutil.sensors_temperatures
    #psutil.net_connections()
    return info


print(getInfo())