import json
import os
import time
from datetime import datetime
from common import write_cache, load_yaml, current_network_status
from login import login
from logout import logout
from mail import mail
from outputlog import outputlog
from wifi import get_current_wifi, switch_wifi


def main():
    result_list = []
    dt = datetime.now()
    dt = dt.strftime("%Y%m%d%H%M%S")
    log_path = os.path.join(os.getcwd(), rf"logs\{dt}_log.txt")
    config_path = os.path.join(os.getcwd(), rf"config.yaml")
    user_info, mail_info = load_yaml(config_path)
    count = 0
    for user in user_info:
        result_list.append({user['wifi_name']: False})
    try:
        for user in user_info:
            connect_state = True
            outputlog(log_path, f'--------------------------------------')
            wifi_is_open = user['wifi_is_open']
            if wifi_is_open:
                current_wifi = get_current_wifi()
                outputlog(log_path, f'当前WIFI为: {current_wifi}')
                wifi_name = user['wifi_name']
                if current_wifi == wifi_name:
                    outputlog(log_path, '当前WIFI为目标WIFI,不需要进行切换')
                else:
                    outputlog(log_path, '当前WIFI不是目标WIFI,正在进行切换')
                    connect_state = switch_wifi(log_path, wifi_name)
            username = user['username']
            password = user['password']
            cache_path = os.path.join(os.getcwd(), rf"cache\{username}_cache.json")
            if connect_state:
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
                    if logout_result == 0:
                        outputlog(log_path, f'用户{username}退出成功')
                    elif logout_result == 1:
                        outputlog(log_path, f'用户{username}当前为网络未连接状态')
                    elif logout_result == 2:
                        outputlog(log_path, f'用户{username}退出失败')
                        continue
                else:
                    outputlog(log_path, f'用户{username}_cache文件未找到，无法进行登出')
                response, cookie = login(log_path, username, password)
                if response:
                    outputlog(log_path, f'用户{username}登录成功')
                    result_list[count][user['wifi_name']] = True
                    count += 1
                    write_result = write_cache(log_path, cache_path, response, cookie)
                    if write_result:
                        outputlog(log_path, f'用户{username}_cache文件写入成功')
                    else:
                        outputlog(log_path, f'用户{username}_cache文件写入失败')
                else:
                    outputlog(log_path, f'用户{username}登录失败')
            else:
                outputlog(log_path, f'用户{username}登录失败')
    except Exception as e:
        outputlog(log_path, e)
    finally:
        if mail_info["is_open"]:
            outputlog(log_path, f'邮件发出前网络测试')
            sender_network = current_network_status(log_path)
            sender_wifi = get_current_wifi()
            network_state = True
            if sender_network:
                outputlog(log_path, f'{sender_wifi}网络正常,不需要进行切换')
            else:
                network_state = False
                outputlog(log_path, f'{sender_wifi}网络异常,正在进行切换')
                for user in user_info:
                    wifi_name = user['wifi_name']
                    if wifi_name != sender_wifi:
                        connect_state = switch_wifi(log_path, wifi_name)
                        if connect_state:
                            time.sleep(3)
                            current_network = current_network_status(log_path)
                            if current_network:
                                outputlog(log_path, f'{wifi_name}网络正常')
                                network_state = True
                                break
                            else:
                                outputlog(log_path, f'{wifi_name}网络异常,正在进行切换')
                        else:
                            outputlog(log_path, f'{wifi_name}无法进行连接,正在进行切换')
            if network_state:
                sender_qq = mail_info["sender_qq"]  # 发件人邮箱
                receiver_qq = mail_info["receiver_qq"]  # 收件人邮箱
                sender_code = mail_info["sender_code"]  # 发件人授权码
                mail(log_path, result_list, sender_qq, receiver_qq, sender_code)
            else:
                outputlog(log_path, '所有网络异常，邮件发送失败')


main()