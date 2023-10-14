import json
import os
import time

import ddddocr
import requests
from datetime import datetime

from data.data import build_data
from mail import mail
from outputlog import outputlog
from wifi import get_current_wifi, switch_wifi


# 获取cookie
def get_cookie():
    res = requests.get('http://221.7.244.134:8080/login_gx.jsp')
    cookie = str(res.cookies).split('=')[1].split('for')[0].strip()
    j_cookie = {
        "JSESSIONID": cookie
    }
    return j_cookie


# 使用ocr引擎识别验证码图片
def identify_images(log_path, images_path):
    ocr = ddddocr.DdddOcr()
    with open(images_path, 'rb') as img:
        img_bytes = img.read()
    code = ocr.classification(img_bytes)
    code_is_int = True
    try:
        int(code)
    except Exception as e:
        code_is_int = False
    # 判断验证码属于4位数的纯数字验证码
    if len(code) == 4 and code_is_int:
        outputlog(log_path, f'图片识别成功，识别结果为：{code}')
        return code
    else:
        outputlog(log_path, '验证码识别失败')
        return ''


# 获取验证码图片并保存
def get_verifycode_images(log_path, cookie):
    current_datetime = datetime.now()
    formatted_datetime = str(current_datetime.strftime('%a %b %d %Y %H:%M:%S GMT%z (%Z)'))
    res = requests.get(f'http://221.7.244.134:8080/verifycode.jpg?{formatted_datetime}', cookies=cookie)
    # 检查响应状态码
    if res.status_code == 200:
        # 从响应中获取图片内容
        image_content = res.content
        # 将图片内容保存到文件
        images_path = os.path.join(os.getcwd(), rf"verifycode.jpg")
        with open(images_path, 'wb') as file:
            file.write(image_content)
        outputlog(log_path, f"图片获取成功，已保存到 {images_path}")
        return images_path
    else:
        outputlog(log_path, "图片获取失败，状态码：", res.status_code)
        return None


# 获取验证码
def get_verifycode(log_path, cookie):
    start_time = time.time()
    while True:
        images_path = get_verifycode_images(log_path, cookie)
        verifycode = identify_images(log_path, images_path)
        end_time = start_time - time.time()
        if verifycode:
            return verifycode
        else:
            outputlog(log_path, '正在重新获取图片')
        if end_time > 300:
            outputlog(log_path, '获取验证码超时')
            return None


def write_cache(log_path, cache_path, response, cookie):
    try:
        logout_params = response.split('gurl')[1].split('?')[1].split('"')[0]
        outputlog(log_path, 'logout_params匹配成功')
    except Exception as e:
        outputlog(log_path, '出现未知错误，未找到logout_params')
        outputlog(log_path, e)
        return None
    data = {
        "cookie": cookie,
        "logout_params": logout_params
    }
    outputlog(log_path, f'new_cookie: {cookie}')
    outputlog(log_path, f'new_params: {logout_params}')
    outputlog(log_path, '正在写入缓存')
    with open(cache_path, 'w') as file:
        json.dump(data, file, indent=4)
    return logout_params


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


def logout(log_path, cookie, params):
    url = f'http://221.7.244.134:8080/logout.do?{params}'
    res = requests.get(url, cookies=cookie)
    if res.status_code == 200:
        if 'SUCCESS' in res.text:
            try:
                res_ping = requests.get('https://www.baidu.com', timeout=3)
            except Exception as e:
                outputlog(log_path, e)
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


def main():
    dt = datetime.now()
    dt = dt.strftime("%Y%m%d%H%M%S")
    log_path = os.path.join(os.getcwd(), rf"logs\{dt}_log.txt")
    userinfo = build_data()
    for user in userinfo:
        outputlog(log_path, f'------------------------------------------')
        current_wifi = get_current_wifi()
        outputlog(log_path, f'当前WIFI为: {current_wifi}')
        wifi_name = user[3]
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
        username = user[0]
        password = user[1]
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
    sender_qq = 'xxxxx@qq.com'  # 发件人邮箱
    receiver_qq = ['xxxxx@qq.com']  # 收件人邮箱
    sender_code = 'xxxxxx'  # 发件人授权码
    mail(log_path, sender_qq, receiver_qq, sender_code)


main()
