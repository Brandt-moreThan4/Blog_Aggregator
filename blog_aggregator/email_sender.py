import json
import smtplib
from email.message import EmailMessage
import smtplib
import ssl
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


with open('config.json') as f:
    config = json.load(f)


def email_new_posts(df_posts:pd.DataFrame) -> pd.DataFrame:
    html_content = construct_email_message(df_posts)
    send_email(html_content)


def construct_email_message(df_posts:pd.DataFrame) -> pd.DataFrame:
    intro_message = '<div>Hey there, see the new posts below.</div><br>'
    df_html = df_posts.to_html()

    complete_html_message = intro_message + df_html

    return complete_html_message


def send_email(html_content:str,receiver:str="brandtgreen97@gmail.com"):
    """Send an email from automatedemailsbg@gmail.com to the receiver with the specified content."""

    ctx = ssl.create_default_context()
    password = config['app_password'] 
    sender = config['email']    

    # Create the message
    message = MIMEMultipart("alternative")
    message["Subject"] = "New Blog Posts have arrived!"
    message["From"] = sender
    message["To"] = receiver

    message.attach(MIMEText(html_content, "html"))
    
    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message.as_string())

