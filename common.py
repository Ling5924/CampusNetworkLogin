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


# 获取本机的公网IP地址
def get_ip():
    try:
        ip = requests.get('https://ident.me').text.strip()
        return ip
    except:
        return None


# 获取验证码
def get_verifycode(log_path, cookie):
    start_time = time.time()
    while True:
        end_time = start_time - time.time()
        if end_time > 300:
            outputlog(log_path, '验证码识别超时')
            return None
        current_datetime = str(datetime.now().strftime('%a %b %d %Y %H:%M:%S GMT%z (%Z)'))
        res = requests.get(f'http://221.7.244.134:8080/verifycode.jpg?{current_datetime}', cookies=cookie)
        if res.status_code == 200:
            image_content = res.content
            ocr = ddddocr.DdddOcr()
            code = ocr.classification(image_content)
            try:
                int(code)
            except Exception as e:
                continue
            # 判断验证码属于4位数的纯数字验证码
            if len(code) == 4:
                outputlog(log_path, f'图片识别成功，识别结果为：{code}')
                return code
            else:
                continue
        else:
            outputlog(log_path, "图片获取失败，状态码：", res.status_code)
            continue


# 读取config.yaml的配置信息
def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
    # 访问配置信息
    network_config = config['network']
    mail_config = config['mail']
    return network_config, mail_config


# 判断当前网络状态  False: 未连接  True: 正常
def current_network_status(log_path):
    try:
        res_ping = requests.get('https://www.baidu.com')
    except Exception as e:
        outputlog(log_path, e)
        outputlog(log_path, '访问百度失败，当前网络未连接')
        return False
    if res_ping.status_code == 200 and '百度一下，你就知道' in res_ping.content.decode():
        outputlog(log_path, '访问百度成功，当前网络正常')
        return True
    else:
        outputlog(log_path, '访问百度失败，当前网络未连接')
        return False
