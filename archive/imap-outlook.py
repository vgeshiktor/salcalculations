import datetime
import email
import imaplib
import os

# Your Outlook.com credentials
username = "innasherts@hotmail.com"
password = "inna2011"

# Connect to the mailbox server
mail = imaplib.IMAP4_SSL("imap-mail.outlook.com")

# Login to the mailbox
mail.login(username, password)

# Select the mailbox
mail.select("INBOX")

# Get the date range for the last month
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=30)

# Convert dates to the required format for the IMAP search query
start_date_str = start_date.strftime("%d-%b-%Y")
end_date_str = end_date.strftime("%d-%b-%Y")

# Search for messages within the date range with attachments
search_query = f"(SINCE {start_date_str} BEFORE {end_date_str} NOT HEADER Content-Type text/plain)"

# Search for emails within the date range
status, message_ids = mail.search(None, search_query)

# Retrieve messages and download attachments
if status == "OK":
    message_ids = message_ids[0].split()
    for msg_id in message_ids:
        status, msg_data = mail.fetch(msg_id, "(RFC822)")
        if status == "OK":
            email_message = email.message_from_bytes(msg_data[0][1])
            subject = email_message["subject"]
            date_received = email_message["date"]
            print(f"Subject: {subject}, Date Received: {date_received}")

            for part in email_message.walk():
                if part.get_content_maintype() == "multipart":
                    continue
                if part.get("Content-Disposition") is None:
                    continue

                filename = part.get_filename()
                if filename:
                    # Download the attachment
                    file_path = os.path.join("attachments", filename)
                    if not os.path.exists("attachments"):
                        os.mkdir("attachments")
                    with open(file_path, "wb") as f:
                        f.write(part.get_payload(decode=True))
                    print(f"Attachment '{filename}' downloaded.")
else:
    print("Failed to retrieve messages.")

# Logout and close the connection
mail.logout()
