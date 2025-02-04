import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
try:
    import RCd.config as config
except:
    class config:
        MAIL_SENDER = ""
# If modifying these SCOPES, delete the token.json file to re-authenticate.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    creds = None
    # Check if token.json exists (saved credentials).
    if os.path.exists('RCd/mail/token.json'):
        creds = Credentials.from_authorized_user_file('RCd/mail/token.json', SCOPES)
    # If no valid credentials, authenticate the user.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for future use.
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def create_message(to, subject, body):
    """Create a MIME email message."""
    message = MIMEText(body)
    message['to'] = to
    message['from'] = config.MAIL_SENDER
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_email_once(message):
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    try:
        response = service.users().messages().send(userId="me", body=message).execute()
        #print(f"Message sent successfully. Message ID: {response['id']}")
    except HttpError as error:
        print(f"An error occurred: {error}")

def send_otp(email, otp):
    recipient_email = email
    email_subject = f"OTP for {config.RCNAME}"
    email_body = f"Your OTP is {otp}."
    email_message = create_message(recipient_email, email_subject, email_body)
    send_email_once(email_message)

def send_forgot_passwd_mail(uname,passwd):
    recipient_email=uname+"@smail.iitm.ac.in"
    email_subject=f"Reverse Coding Password Recovery Mail for {config.RCNAME}"
    email_body=f"Your Password is {passwd} "
    email_message=create_message(recipient_email,email_subject,email_body)
    send_email_once(email_message)

if __name__ == '__main__':
    # Test email

    recipient_email = config.MAIL_SENDER
    email_subject = "Test Email through Gmail API"
    email_body = "This is a test email for RC setup."
    # Create and send the message.
    email_message = create_message(recipient_email, email_subject, email_body)
    send_email_once(email_message)
