import time
import requests
from outputlog import outputlog


# 登出
def logout(log_path, cookie, params):
    url = f'http://221.7.244.134:8080/logout.do?{params}'
    res = requests.get(url, cookies=cookie)
    if res.status_code == 200:
        if 'SUCCESS' in res.text:
            try:
                res_ping = requests.get('https://www.baidu.com', timeout=3)
            except Exception as e:
                outputlog(log_path, e)
                outputlog(log_path, '访问百度失败，账号已退出')
                return True
            if res_ping.status_code == 200:
                outputlog(log_path, '参数错误，账号并未完全退出')
                outputlog(log_path, '请把对应的cache文件删除后重新登录')
                return False
            time.sleep(3)
            return True
        else:
            outputlog(log_path, '未知错误')
            outputlog(log_path, res.text)
            return False
    else:
        outputlog(log_path, f'logout请求失败,status_code = {res.status_code}')
        return False
