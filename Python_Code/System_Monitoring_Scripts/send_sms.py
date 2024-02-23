import email
import smtplib
import ssl
from providers import PROVIDERS

def send_sms_via_email(
        number: str,
        message: str,
        provider: str, 
        sender_credentials: tuple,
        subject: str = "sent using Python",
        smtp_server = "smtp.gmail.com",
        smtp_port: int = 465,
):
    sender_email, email_password = sender_credentials
    receiver_email = f"{number}@{PROVIDERS.get(provider).get('sms')}"

    email_message = f"Subject:{subject}\nTo:{receiver_email}\n{message}"

    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=ssl.create_default_context()) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, email_message)

def main():
    number = "4407498307"
    message = "what's up? compostmonitor here"
    provider = "T-Mobile"
    sender_credentials = ("ideascompostmonitor@gmail.com", "uptrrccfbehyrxso")

    send_sms_via_email(number, message, provider, sender_credentials, subject = "compostmonitor_test")

if __name__ == "__main__":
    main()
