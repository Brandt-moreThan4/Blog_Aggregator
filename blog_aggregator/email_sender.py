import json
import smtplib
from email.message import EmailMessage
import smtplib
import ssl



with open('config.json') as f:
    config = json.load(f)




ctx = ssl.create_default_context()
password = config['app_password']    # Your app password goes here
sender = config['email']    # Your e-mail address
receiver = "brandtgreen97@gmail.com" # Recipient's address
message = """
Hello from Python.
"""

with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
    server.login(sender, password)
    server.sendmail(sender, receiver, message)


print(config)