import smtplib
from datetime import datetime
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from outputlog import outputlog


def mail(log_path, result_list, sender_qq, receiver_qq, sender_code):
    host_server = 'smtp.qq.com'  # qq邮箱smtp服务器
    #  m_date = datetime.now().date()
    mail_title = ''
    for x in result_list:
        if list(x.values())[0]:
            y = "成功"
        else:
            y = "失败"
        mail_title += f"{list(x.keys())[0]}: {y} "  # 邮件标题n
    #  mail_title = f'{m_date}的日志'
    with open(log_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # 邮件正文内容
    # print(content)

    mail_content = content

    msg = MIMEMultipart()
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq
    msg["To"] = Header("日志邮箱", "utf-8")
    msg.attach(MIMEText(mail_content, 'plain', 'utf-8'))

    attachment = MIMEText(open(log_path, 'rb').read(), 'base64', 'utf-8')
    attachment["Content-Type"] = 'application/octet-stream'

    filename = log_path.split('\\')[-1]
    attachment["Content-Disposition"] = f'attachment; filename={filename}'

    msg.attach(attachment)

    try:
        smtp = smtplib.SMTP_SSL(host_server)  # ssl登录连接到邮件服务器
        # smtp.set_debuglevel(1)  # 0是关闭，1是开启debug
        smtp.ehlo(host_server)  # 跟服务器打招呼，告诉它我们准备连接，最好加上这行代码
        smtp.login(sender_qq, sender_code)
        outputlog(log_path, "邮件发送成功")
        smtp.sendmail(sender_qq, receiver_qq, msg.as_string())
        smtp.quit()
    except smtplib.SMTPException as e:
        outputlog(log_path, "无法发送邮件")
        outputlog(log_path, e)