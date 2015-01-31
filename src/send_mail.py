#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import email
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import smtplib

def sendEmail(authInfo, fromAdd, toAdd, subject, plainText, htmlText):
        strFrom = fromAdd
        strTo = ', '.join(toAdd)
        server = authInfo.get('server')
        user = authInfo.get('user')
        passwd = authInfo.get('password')
        if not (server and user and passwd) :
                print 'incomplete login info, exit now'
                return
        # 设定root信息
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = subject
        msgRoot['From'] = strFrom
        msgRoot['To'] = strTo
	msgRoot['Date'] = email.Utils.formatdate() 
        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide which they want to display.
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        #设定纯文本信息
        msgText = MIMEText(plainText, 'plain', 'utf-8')
        msgAlternative.attach(msgText)
        #设定HTML信息
        msgText = MIMEText(htmlText, 'html', 'utf-8')
        msgAlternative.attach(msgText)
        #设定内置图片信息
        #fp = open('test.jpg', 'rb')
        #msgImage = MIMEImage(fp.read())
        #fp.close()
        #msgImage.add_header('Content-ID', '<image1>')
        #msgRoot.attach(msgImage)
        #发送邮件
        smtp = smtplib.SMTP()
        #设定调试级别，依情况而定
        smtp.set_debuglevel(0)
        smtp.connect(server)
        #smtp.login(user,passwd)
        smtp.sendmail(strFrom, toAdd, msgRoot.as_string())
        smtp.quit()
        return


if __name__ == '__main__' :
        authInfo = {}
        authInfo['server'] = '10.7.2.18'
        authInfo['user'] = 'zhixian.yang'
        authInfo['password'] = '****'
        fromAdd = 'zhixian.yang@renren-inc.com'
	toAdd = list()
	for eml in sys.argv[3:]:
		toAdd.append(eml);
        sendEmail(authInfo, fromAdd, toAdd, sys.argv[1], sys.argv[2], sys.argv[2])

