from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Function to send SMS alert
def send_sms_alert(body):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
    to_phone_number = os.getenv("TO_PHONE_NUMBER")

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body=body,
            from_=from_phone_number,
            to=to_phone_number
        )
        print("SMS alert sent successfully.")
    except Exception as e:
        print(f"Failed to send SMS alert: {e}")

# Example usage
if __name__ == "__main__":
    send_sms_alert("This is a test SMS alert message.")
