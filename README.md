<p align="center">
  <h2 align="center">CampusNetworkLogin</h2>
  <p align="center">
    联通校园网自动登录
    <br/>
  </p>
</p>

***
**⚡ 支持**   
* [x] 每天定时登录
* [x] 同设备登录多个账号
* [x] 使用邮箱发送日志功能


## 🔧 教程

### 第一次运行请在主目录执行```pip install -r requirements.txt```命令安装对应的依赖
### 修改config.yaml配置文件
### 第一次运行请将当前网络的账号退出，否则会导致登录失败，到当前网络路由器后台重置网络后即可将账号退出，当电脑自动弹出联通登录页面即说明账号退出成功，此时就可以运行main.py文件进行第一次登录，第一次登录成功后就不需要通路由器后台进行账号退出
### 当程序可以正常登录和退出后，即可通过login.bat脚本文件在电脑上设置定时任务来实现每天登录网络
#### 注：当需要登录多账号的情况下需要以管理员权限运行，否则会出现WIFI切换失败导致登录失败的问题出现


欢迎提出新的点子、 Pull Request。  


## 💪 支持我们

如果我们这个项目对你有所帮助，请给我们一颗 ⭐️
