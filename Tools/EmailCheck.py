# -*- coding = utf-8 -*-
# @Time: 2023-08-24 16:21
# @Author :张志扬
# @File : EmailCheck.py
# @Software: PyCharm

import  random
import smtplib
import email.utils
from email.mime.text import MIMEText
authorizationKey = "rpljgyjfrbhageha"

def createCaptcha():
    n1 = random.randint(0, 9)
    n2 = random.randint(0, 9)
    n3 = random.randint(0, 9)
    n4 = random.randint(0, 9)
    return str(n1) + str(n2) + str(n3) + str(n4)


def emailCheck(userEmail,num):
    message = MIMEText(num)
    message['To'] = email.utils.formataddr(('xxx', userEmail))
    message['From'] = email.utils.formataddr(('FusionCode', '1274975655@qq.com'))
    message['Subject'] = 'FusionCode验证码'
    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
    server.login('1274975655@qq.com',authorizationKey)
    server.set_debuglevel(True)
    try:
        server.sendmail('1274975655@qq.com',[userEmail],msg=message.as_string())
    finally:
        server.quit()
