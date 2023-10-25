import time
import requests

from common import current_network_status
from outputlog import outputlog


# 登出 0 成功 1 网络未连接 2 失败
def logout(log_path, cookie, params):
    url = f'http://221.7.244.134:8080/logout.do?{params}'
    current_network = True
    outputlog(log_path, '登出前网络测试')
    for _ in range(3):
        current_network = current_network_status(log_path)
        if current_network:
            break
        time.sleep(3)
    if current_network:
        res = requests.get(url, cookies=cookie)
    else:
        return 1
    if res.status_code == 200:
        if 'SUCCESS' in res.text:
            outputlog(log_path, '登出后网络测试')
            network_status = current_network_status(log_path)
            if network_status:
                outputlog(log_path, '参数错误，账号并未完全退出')
                outputlog(log_path, '请把对应的cache文件删除后重新登录')
                return 2
            else:
                outputlog(log_path, '账号成功登出')
            time.sleep(3)
            return 0
        else:
            outputlog(log_path, '未知错误')
            outputlog(log_path, res.text)
            return 2
    else:
        outputlog(log_path, f'logout请求失败,status_code = {res.status_code}')
        return 2
