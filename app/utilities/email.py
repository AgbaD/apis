#!/usr/bin/python3
# Author:   @AgbaD | @Agba_dr3

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app, render_template
import smtplib
import ssl


def send_mail(subject, template, to, **kwargs):
    message = MIMEMultipart("alternative")
    message["Subject"] = current_app.config['MAIL_PREFIX'] + subject
    message["From"] = current_app.config['TMM_SUPPORT']
    message["To"] = to

    text = render_template(template + ".txt", **kwargs)
    html = render_template(template + ".html", **kwargs)

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("mail.privateemail.com", 465, context=context) as server:
        server.login(current_app.config['TMM_SUPPORT'], current_app.config['TMM_SUPPORT_PASSWORD'])
        print("Sending email to {}".format(to))
        server.sendmail(
            current_app.config['TMM_SUPPORT'], to, message.as_string()
        )
        print("Mail sent to {} successfully".format(to))
        print()
