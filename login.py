import time
import requests
from common import get_verifycode
from outputlog import outputlog


# 登录
def login(log_path, username, password, cookie):
    start_time = time.time()
    while True:
        end_time = start_time - time.time()
        verify_code = get_verifycode(log_path, cookie)
        params = {
            'bpssUSERTYPE': '1',
            'bpssUSERNAME': username,
            'bpssBUSPWD': password,
            'bpssVERIFY': verify_code,
        }
        res = requests.get('http://221.7.244.134:8080/login.do', params=params, cookies=cookie)
        if res.status_code == 200:
            if "您输入的帐号,密码或开户地有误,请重新输入" in res.text:
                outputlog(log_path, '账号未退出，请退出后再重新登录')
                return None
            elif "验证码输入错误！" in res.text:
                if end_time > 300:
                    outputlog(log_path, '登录超时')
                    return None
                outputlog(log_path, '验证码错误，正在重新获取')
                continue
            return res.text
        else:
            outputlog(log_path, f'login请求失败,status_code = {res.status_code}')
            return None
