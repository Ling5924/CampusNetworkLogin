import json
import os
import time
from datetime import datetime
import ddddocr
import requests
import yaml
from outputlog import outputlog


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


# 读取config.yaml的配置信息
def load_yaml(file_path):
    with open('config.yaml', 'r', encoding='utf-8') as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)

    # 访问配置信息
    network_config = config['network']
    mail_config = config['mail']
    return network_config, mail_config
