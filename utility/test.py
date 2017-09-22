from django.conf import settings

import smtplib
from email.mime.text import MIMEText


def main(subject, message, to):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = settings.DEFAULT_FROM_EMAIL
    msg["To"] = to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
        s.sendmail(settings.DEFAULT_FROM_EMAIL, to, msg.as_string())
        s.quit()
        print("Success!")
    except smtplib.SMTPException as e:
        print("Falied,%s" % e)
