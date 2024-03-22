import subprocess
import time

from outputlog import outputlog


# 获取当前WIFI名称
def get_current_wifi():
    cmd = 'netsh wlan show interfaces'
    p = subprocess.Popen(cmd,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    wifi_info = p.stdout.read().decode('gb2312', errors='ignore')
    if wifi_info:
        wifi_name = wifi_info.split(':')[-2].strip().split(' ')[0]
        return wifi_name
    else:
        return None


# 切换指定WIFI
def switch_wifi(log_path, wifi_name):
    connects = 0
    while True:
        stop_result, start_result = restart_wifi()
        time.sleep(3)
        connect_cmd = f'netsh wlan connect name="{wifi_name}"'
        p = subprocess.Popen(connect_cmd,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)
        result = p.stdout.read().decode('gb2312', errors='ignore').strip()
        time.sleep(3)
        outputlog(log_path, stop_result)
        outputlog(log_path, start_result)
        current_wifiname = get_current_wifi()
        # if '已成功完成连接请求。' in result:
        if current_wifiname == wifi_name:
            outputlog(log_path, f"{wifi_name}{result}")
            return True
        elif connects > 3:
            outputlog(log_path, f'{wifi_name}无法进行连接')
            return False
        else:
            connects += 1
            outputlog(log_path, f'连接失败，{result}')
            outputlog(log_path, f'正在进行第{connects}次重新连接')
            time.sleep(5)


# 重置WIFI服务
# 使用该方法需要管理员权限运行脚本
def restart_wifi():
    stop_wifi_cmd = 'net stop WlanSvc'
    start_wifi_cmd = 'net start WlanSvc'
    p = subprocess.Popen(stop_wifi_cmd,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    stop_result = p.stdout.read().decode('gb2312', errors='ignore').strip()
    p1 = subprocess.Popen(start_wifi_cmd,
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          shell=True)
    start_result = p1.stdout.read().decode('gb2312', errors='ignore').strip()
    time.sleep(3)
    return stop_result, start_result
