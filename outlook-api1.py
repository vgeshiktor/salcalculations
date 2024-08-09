import os
import datetime
import base64
import requests
from outlook_api import API
from pyOutlook import OutlookAccount



# Function to download attachments from an email
def download_attachment(attachment, email_subject, download_folder):
    file_name = attachment["name"]
    file_data = base64.b64decode(attachment["contentBytes"])

    save_path = os.path.join(download_folder, email_subject)
    os.makedirs(save_path, exist_ok=True)
    file_path = os.path.join(save_path, file_name)

    with open(file_path, "wb") as f:
        f.write(file_data)

    print(f"Attachment '{file_name}' saved to '{file_path}'")


def main():
    # Replace with your Outlook.com credentials
    username = "innasherts@hotmail.com"
    password = "inna2011"

    # Replace with your desired download folder
    download_folder = "attachments_download"

    # Authenticate with the Outlook.com API
    api = API(username, password)

    # Calculate the date range for the last month
    today = datetime.date.today()
    last_month = today - datetime.timedelta(days=30)

    # Get emails within the date range
    emails = api.get_messages(datetime_from=last_month, datetime_to=today)

    # Filter emails with attachments
    emails_with_attachments = [email for email in emails if email.get("hasAttachments", False)]

    # Download attachments from each email
    for email in emails_with_attachments:
        email_subject = email["subject"]
        attachments = email["attachments"]
        for attachment in attachments:
            download_attachment(attachment, email_subject, download_folder)


if __name__ == "__main__":
    main()
