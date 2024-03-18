
------------------------------------
<p align="center">
  <h2 align="center">桂林理工大学南宁分校校园网自动登录</h2>
</p>
<br>

![cover](https://github.com/Ling5924/Images/blob/master/CNL/campus.png)

***
**⚡ 支持**   
* [x] 每天定时登录
* [x] 同设备登录多个账号
* [x] 使用邮箱发送日志功能

## 🔧 快速搭建


**Windows: 快速部署包**

* 我们为 Windows 用户制作了一个快速启动包，可以在 [Release](https://github.com/Ling5924/CampusNetworkLogin/releases) 中找到。    

* 文件名为：`Windows-quickstart-CampusNetworkLogin-v2.0.0.zip`

* 快速部署包中会含有 python 解释器，所以无需再下载

* 第一次启动运行 start.cmd 输入配置即可完成任务计划程序的创建
* 运行 start.cmd 和 stop.cmd 都需要以管理员身份运行

* stop.cmd 用于停止任务计划程序，停止后重新运行 start.cmd 即可再次创建

## 🦊 教程
* 需下载python3.11及以下的解释器，python3.12该项目不兼容
* 第一次运行请在主目录执行```pip install -r requirements.txt```命令安装对应的依赖
* 修改config.yaml配置文件
* 当程序可以正常登录和退出后，即可通过login.bat脚本文件在电脑上创建任务计划程序来实现每天登录网络
### 注：当需要登录多账号的情况下需要以管理员权限运行，否则会出现WIFI切换失败导致登录失败的问题出现


欢迎提出新的点子、 Pull Request。  

## 📷 Windows创建任务计划程序教程
![cover](https://github.com/Ling5924/Images/blob/master/CNL/1.png)
![cover](https://github.com/Ling5924/Images/blob/master/CNL/2.png)
![cover](https://github.com/Ling5924/Images/blob/master/CNL/3.png)
![cover](https://github.com/Ling5924/Images/blob/master/CNL/4.png)
![cover](https://github.com/Ling5924/Images/blob/master/CNL/5.png)
![cover](https://github.com/Ling5924/Images/blob/master/CNL/6.png)
![cover](https://github.com/Ling5924/Images/blob/master/CNL/7.png)


## 💪 支持我们

如果我们这个项目对你有所帮助，请给我们一颗 ⭐️
