import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()
import os
app_password=os.environ.get("APP_PASSWORD")
sender_email=os.environ.get("SENDER_EMAIL")


def send_email(receiver_email: str, subject: str, body: str):
    """Sends an email with the provided body and subject."""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.send_message(msg)
    server.quit()

    return "Email sent successfully!"

if __name__ == "__main__":
    # Test arguments if run directly
    # Note: Ensure receiver_email is valid or catch potential errors if using dummy value
    try:
        send_email("test_receiver@example.com", "Test Subject", "This is a test email sent using Python.")
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

