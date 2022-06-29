from email.mime.text import MIMEText
from email.header import Header
import smtplib

def send(receiver,subject,text):
    # 第三方 SMTP 服务
    mail_host = "smtp.exmail.qq.com"  # 设置服务器
    mail_user = "zengchenglong@yonghongtech.com"  # 用户名
    mail_pass = "wan520Zcl"  # 口令

    sender = 'zengchenglong@yonghongtech.com'
    receivers =receiver # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(text, 'plain', 'utf-8')
    message['From'] = Header(sender, 'utf-8')  # 发送者
    message['To'] = Header(receivers, 'utf-8')  # 接收者

    #subject = text.split('的')[0]
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)