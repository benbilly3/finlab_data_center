import datetime
from django_q.models import Success, Failure
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
import os


class EmailNotification:

    @classmethod
    def send_email(cls, sender, sender_password, receivers, subject, content):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ", ".join(receivers)
        text = MIMEText(content, 'html')
        msg.attach(text)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(sender, sender_password)
        server.sendmail(sender, receivers, msg.as_string())
        server.close()

    @classmethod
    def crawler_html_table(cls, subtitle, obj_list):
        content = f"<h2>{subtitle}({len(obj_list)})</h2>\
        <table border='1'><tr><td>Id</td><td>Group</td><td>Started</td><td>Stopped</td><td>Result</td></tr>"
        if len(obj_list) > 0:
            for i, f in enumerate(obj_list):
                msg = f"<tr><td>{i + 1}</td><td>{f['group']}</td><td>{f['started']}</td><td>{f['stopped']}</td><td>" \
                      f"{f['result']}</td></tr>"
                content += msg
        content += "</table>"
        return content

    @classmethod
    def push_crawlers_processed_report(cls):
        now = datetime.date.today()
        success = Success.objects.filter(started__gt=now).order_by('started').values('started', 'stopped', 'group',
                                                                                     'result')
        success_get_data = []
        success_but_data_not_existed = []
        exception_fail = []
        for i in range(len(success)):
            if 'Finish' in str(success[i]['result']):
                success_get_data.append(success[i])
            elif 'Fail' in str(success[i]['result']):
                success_but_data_not_existed.append(success[i])
            else:
                exception_fail.append(success[i])
        fail = list(
            Failure.objects.filter(started__gt=now).order_by('started').values('started', 'stopped', 'group',
                                                                               'result'))
        fail += exception_fail
        subtitle_list = ['Fail', 'Success but data not existed', 'Success get data']
        obj_list = [fail, success_but_data_not_existed, success_get_data]

        content = ''
        for subtitle, obj in zip(subtitle_list, obj_list):
            content += cls.crawler_html_table(subtitle, obj)

        gmail_user = os.getenv('GMAIL', settings.CONFIG_DATA.get("GMAIL"))
        gmail_password = os.getenv('GMAIL_PASSWORD', settings.CONFIG_DATA.get("GMAIL_PASSWORD"))
        receivers = [gmail_user]
        now_str = str(now.strftime("%Y-%m-%d"))
        subject = f"【Finlab Data-Center Crawlers Process Report-{now_str}】"
        cls.send_email(gmail_user, gmail_password, receivers, subject, content)
        msg = "Finish!sent daily crawlers processed report by email"
        return msg
