import json
import os
from datetime import datetime
from common import get_cookie, write_cache, load_yaml
from login import login
from logout import logout
from mail import mail
from outputlog import outputlog
from wifi import get_current_wifi, switch_wifi


def main():
    dt = datetime.now()
    dt = dt.strftime("%Y%m%d%H%M%S")
    log_path = os.path.join(os.getcwd(), rf"logs\{dt}_log.txt")
    config_path = os.path.join(os.getcwd(), rf"config.yaml")
    user_info, mail_info = load_yaml(config_path)
    for user in user_info:
        outputlog(log_path, f'--------------------------------------')
        current_wifi = get_current_wifi()
        outputlog(log_path, f'当前WIFI为: {current_wifi}')
        wifi_name = user['wifi_name']
        if current_wifi == wifi_name:
            outputlog(log_path, '当前WIFI为目标WIFI,不需要进行切换')
        else:
            outputlog(log_path, '当前WIFI不是目标WIFI,正在进行切换')
            result, stop_result, start_result = switch_wifi(wifi_name)
            outputlog(log_path, stop_result)
            outputlog(log_path, start_result)
            if '已成功完成连接请求。' in result:
                outputlog(log_path, f"{wifi_name}{result}")
            else:
                outputlog(log_path, f'连接失败，{result}')
                continue
        username = user['username']
        password = user['password']
        cache_path = os.path.join(os.getcwd(), rf"cache\{username}_cache.json")
        if os.path.exists(cache_path):
            with open(cache_path, 'r') as file:
                data = json.load(file)
            cookie = data.get("cookie")
            params = data.get("logout_params")
            if cookie and params:
                logout_result = logout(log_path, cookie, params)
            else:
                outputlog(log_path, f'用户{username}_cache文件不完整，无法进行登出')
                continue
            if logout_result:
                outputlog(log_path, f'用户{username}退出成功')
            else:
                outputlog(log_path, f'用户{username}退出失败')
                continue
        else:
            outputlog(log_path, f'用户{username}_cache文件未找到，无法进行登出')
        cookie = get_cookie()
        print(username, password, cookie)
        response = login(log_path, username, password, cookie)
        if response:
            outputlog(log_path, f'用户{username}登录成功')
            write_result = write_cache(log_path, cache_path, response, cookie)
            if write_result:
                outputlog(log_path, f'用户{username}_cache文件写入成功')
            else:
                outputlog(log_path, f'用户{username}_cache文件写入失败')
        else:
            outputlog(log_path, f'用户{username}登录失败')
    if mail_info["is_open"]:
        sender_qq = mail_info["sender_qq"]  # 发件人邮箱
        receiver_qq = mail_info["receiver_qq"]  # 收件人邮箱
        sender_code = mail_info["sender_code"]  # 发件人授权码
        mail(log_path, sender_qq, receiver_qq, sender_code)


main()
