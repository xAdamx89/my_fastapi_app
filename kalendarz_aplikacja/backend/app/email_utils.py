import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(to_email, subject, body):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    from_email = "adammazurek89@gmail.com"
    password = os.getenv("GMAIL_APP_PASSWORD")

    if not password:
        print("Brak hasła do Gmaila w zmiennych środowiskowych!")
        return

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("E-mail wysłany pomyślnie")
    except Exception as e:
        print(f"Błąd podczas wysyłania maila: {e}")