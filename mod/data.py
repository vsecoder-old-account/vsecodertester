import psutil
import datetime
import platform
import socket

def stat():
    mem = psutil.virtual_memory()
    active_since = datetime.datetime.fromtimestamp(psutil.boot_time())
    cpu = psutil.cpu_percent()
    internet = psutil.net_io_counters()
    #st = speedtest.Speedtest()

    status_cpu = '🟢'
    if cpu > 70: status_cpu = '🔴'
    elif cpu > 30: status_cpu = '🟡'
    else: status_cpu = '🟢'
    
    status_memory = '🟢'
    if mem.percent > 70: status_memory = '🔴'
    elif mem.percent > 30: status_memory = '🟡'
    else: status_memory = '🟢'
    
    status_disk = '🟢'
    if psutil.disk_usage('/').percent > 70: status_disk = '🔴'
    elif psutil.disk_usage('/').percent > 30: status_disk = '🟡'
    else: status_disk = '🟢'

    data = {
        'ip': socket.gethostbyname(socket.getfqdn()),
        'uptime': str(datetime.datetime.now() - active_since),
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'cpu': {
            'used': psutil.cpu_count() / 100 * cpu,
            'free': psutil.cpu_count() - psutil.cpu_count() / 100 * cpu,
            'total': psutil.cpu_count(),
            'percent': cpu
        },
        'memory': {
            'total': round(mem.total / 1024 / 1024),
            'avaliable': round(mem.available / 1024 / 1024),
            'used': round(mem.used / 1024 / 1024),
            'free': round(mem.free / 1024 / 1024),
            'active': round(mem.active / 1024 / 1024),
            'inactive': round(mem.inactive / 1024 / 1024),
            'cached': round(mem.cached / 1024 / 1024),
            'buffers': round(mem.buffers / 1024 / 1024),
            'shared': round(mem.shared / 1024 / 1024),
            'percent': mem.percent
        },
        'disk': {
            'total': round(psutil.disk_usage('/').total / 1024 / 1024),
            'used': round(psutil.disk_usage('/').used / 1024 / 1024),
            'free': round(psutil.disk_usage('/').free / 1024 / 1024),
            'percent': psutil.disk_usage('/').percent
        },
        'status': {
            'cpu': status_cpu,
            'memory': status_memory,
            'disk': status_disk
        },
        'internet': {
            #'upload': st.upload(),
            #'donwload': st.donwload(),
            #'ping': st.ping(),
            'bytes_sent': internet.bytes_sent,
            'bytes_recv': internet.bytes_recv,
            'packets_sent': internet.packets_sent,
            'packets_recv': internet.packets_recv,
            'errin': internet.errin,
            'errout': internet.errout,
            'dropin': internet.dropin,
            'dropout': internet.dropout
        }
    }
    return data