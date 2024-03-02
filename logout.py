import time
from datetime import datetime
import requests
from common import current_network_status, get_cookie, get_ip
from outputlog import outputlog


# 登出
def logout(log_path, username):
    cookie = get_cookie()
    ip = get_ip()
    current_time = datetime.now().strftime("%Y%m%d%H%M%S%f")[:17]
    res = requests.get('http://221.7.244.134:8080/login_gx.jsp', cookies=cookie).text
    CSRFToken_HW = res.split("CSRFToken_HW' value='")[1].split("' /></form>")[0]
    params = f"CSRFToken_HW={CSRFToken_HW}&ATTRIBUTE_USERNAME={username}&wlanuserip={ip}&wlanacname=&authType=01&wlanusermac=&flowID={current_time}+{username}&terminalType=0&ssid="
    url = f'http://221.7.244.134:8080/logout.do?{params}'
    res = requests.get(url, cookies=cookie)
    if res.status_code == 200:
        if 'SUCCESS' in res.text:
            outputlog(log_path, '登出后网络测试')
            network_status = current_network_status(log_path)
            if network_status:
                outputlog(log_path, '参数错误，账号并未完全退出')
                return False
            else:
                outputlog(log_path, '账号成功登出')
            time.sleep(3)
            return True
        else:
            outputlog(log_path, '未知错误')
            outputlog(log_path, res.text)
            return False
    else:
        outputlog(log_path, f'logout请求失败,status_code = {res.status_code}')
        return False
