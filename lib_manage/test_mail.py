import smtplib
from email.mime.text import MIMEText

# Email configuration
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.zoho.in'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'genisistesting@zohomail.in'  # Your Zoho email
EMAIL_HOST_PASSWORD = ''  # Your Zoho password
DEFAULT_FROM_EMAIL = 'genisistesting@zohomail.in'  # Your Zoho email
SERVER_EMAIL = 'genisistesting@zohomail.in'  # Your Zoho email

def send_email(to_email, subject, message):
    # Create the message
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = DEFAULT_FROM_EMAIL
    msg['To'] = to_email

    # Send the email
    try:
        server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)  # Using SSL
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)  # Login to the server
        server.sendmail(DEFAULT_FROM_EMAIL, [to_email], msg.as_string())  # Send email
        print('Email sent successfully!')
    except Exception as e:
        print(f'Error sending email: {e}')
    finally:
        server.quit()  # Ensure the server is closed properly

# Example usage
if __name__ == '__main__':
    send_email('21z247@psgtech.ac.in', 'Test Email', 'This is a test email sent from Python.')
