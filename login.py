import time
import ddddocr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
import os

from CampusNetworkLogin.data.data import build_data
from CampusNetworkLogin.mail import mail
from outputlog import outputlog
from wifi import get_current_wifi, switch_wifi


# 获取DOE元素
def base_find(driver, loc, timeout=30, poll_frequency=0.5):
    return WebDriverWait(driver, timeout, poll_frequency).until(lambda x: x.find_element(*loc))


# 获取文本方法
def get_text(driver, loc):
    return base_find(driver, loc).text


# 单击方法
def base_click(driver, loc):
    base_find(driver, loc).click()


# 输入框方法
def base_input(driver, loc, value):
    el = base_find(driver, loc)
    el.clear()
    el.send_keys(value)


# 获取验证码
def get_code(log_path, driver, loc):
    start_time = time.time()
    while True:
        el = base_find(driver, loc)
        el.click()
        # 截取图片
        el.screenshot('verifycode.jpg')
        ocr = ddddocr.DdddOcr()
        with open('verifycode.jpg', 'rb') as img:
            img_bytes = img.read()
        # 使用ocr引擎识别验证码图片
        code = ocr.classification(img_bytes)
        code_is_int = True
        try:
            code_int = int(code)
        except Exception as e:
            code_is_int = False
        end_time = start_time - time.time()
        # 判断验证码属于4位数的纯数字验证码
        if len(code) == 4 and code_is_int:
            return code
        # 超过300秒后跳出循环
        elif end_time > 300:
            outputlog(log_path, '获取验证码超时')
            return ''


def restart_zx_network(log_path, route_username, route_password):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    option.add_argument('no-sandbox')
    option.add_argument('disable-dev-shm-usage')
    option.add_experimental_option('useAutomationExtension', False)
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    outputlog(log_path, '正在进行网络重置')
    d = webdriver.Chrome()
    d.get('http://192.168.5.1/')
    d.maximize_window()
    router_username = (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[1]/div/div/div[1]/input')
    router_password = (By.XPATH, '//*[@id="default-login-pwd"]')
    router_login = (By.XPATH, '//*[@id="tologin"]')
    network = (By.XPATH, '//*[@id="header"]/div[2]/div[1]')
    off_network = (By.XPATH, '//*[@id="vue-dhcp-ipv6"]')
    open_network = (By.XPATH, '//*[@id="vue-dhcp-ipv6"]')
    submit = (By.XPATH, '//*[@id="vue-dhcp-submit"]')

    base_input(d, router_username, route_username)
    base_input(d, router_password, route_password)
    base_click(d, router_login)
    base_click(d, network)
    base_click(d, off_network)
    base_click(d, submit)
    time.sleep(10)
    base_click(d, open_network)
    base_click(d, submit)
    outputlog(log_path, '网络重置成功')


# 路由器重置网络，使其可以正常登录联通网络
def restart_td_network(log_path, route_password):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    option.add_argument('no-sandbox')
    option.add_argument('disable-dev-shm-usage')
    option.add_experimental_option('useAutomationExtension', False)
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    outputlog(log_path, '正在进行网络重置')
    d = webdriver.Chrome(option)
    d.get('http://192.168.0.1/')
    d.maximize_window()

    router_password = (By.XPATH, '/html/body/div/div/div[3]/div[2]/section/div/div/div[1]/label/input')
    router_login = (By.XPATH, '/html/body/div/div/div[3]/div[2]/section/button')
    network = (By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div/div[2]')
    off_network = (By.XPATH, '//*[@id="app"]/div/div[3]/div[1]/div/div[2]/div[3]/button')
    open_network = (By.XPATH, '//*[@id="app"]/div/div[3]/div[1]/div/div[2]/div[3]/button')

    base_input(d, router_password, route_password)
    base_click(d, router_login)
    base_click(d, network)
    base_click(d, off_network)
    time.sleep(5)
    d.refresh()
    base_click(d, open_network)
    outputlog(log_path, '网络重置成功')


# 登录联通网络
def login_network(log_path, username, password):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    option.add_argument('no-sandbox')
    option.add_argument('disable-dev-shm-usage')
    option.add_experimental_option('useAutomationExtension', False)
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    outputlog(log_path, '开始登录联通网络')
    driver = webdriver.Chrome()
    driver.get('http://221.7.244.134:8080/login_gx.jsp')
    driver.maximize_window()

    login_username = (By.XPATH, '//*[@id="bpssUSERNAME"]')
    login_password = (By.XPATH, '//*[@id="bpssBUSPWD"]')
    verify_code = (By.XPATH, '//*[@id="bpssVERIFY"]')
    login = (By.XPATH, '//*[@id="loginForm"]/table/tbody/tr[7]/td/input')
    image = (By.XPATH, '//*[@id="verifycode"]')
    nick_name = (By.XPATH, '//*[@id="showlogin"]/table/tbody/tr[2]/td[2]')
    base_input(driver, login_username, username)
    base_input(driver, login_password, password)
    start_time = time.time()
    login_count = 0
    while True:
        # 获取验证码
        verifycode = get_code(log_path, driver, image)
        outputlog(log_path, f'verifycode = {verifycode}')
        base_input(driver, verify_code, verifycode)
        base_click(driver, login)
        login_count += 1
        try:
            nickname = get_text(driver, nick_name)
        except Exception as e:
            outputlog(log_path, f'第{login_count}次登录失败，正在重试')
            nickname = ''
        if nickname == username:
            outputlog(log_path, '登录成功！')
            return
        time.sleep(1)
        # driver.switch_to.alert.dismiss()
        driver.back()
        time.sleep(10)
        end_time = time.time() - start_time

        if end_time > 600:
            outputlog(log_path, '登录超时')
            break


def main():
    dt = datetime.now()
    dt = dt.strftime("%Y%m%d%H%M%S")
    log_path = os.path.join(os.getcwd(), rf"logs\{dt}_log.txt")
    userinfo = build_data()
    for user in userinfo:
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
                outputlog(log_path, result)
                continue
        route_info = user[2]
        if route_info:
            if wifi_name == "123456":
                route_password = route_info['route_password']
                restart_td_network(log_path, route_password)
            if wifi_name == "只等妹妹":
                route_username = route_info['route_username']
                route_password = route_info['route_password']
                restart_zx_network(log_path, route_username, route_password)
        time.sleep(5)
        username = user[0]
        password = user[1]
        login_network(log_path, username, password)
    sender_qq = '2324899362@qq.com'  # 发件人邮箱
    sender_code = 'dzxrccfdfeghebai'  # 发件人授权码
    receiver_qq = ['2223522114@qq.com']  # 收件人邮箱
    mail(log_path, sender_qq, receiver_qq, sender_code)


main()
