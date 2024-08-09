import requests
import json
import datetime
import os

# Your Microsoft Graph API endpoint for getting messages
messages_url = "https://graph.microsoft.com/v1.0/me/messages"

# Your Azure AD app credentials
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
tenant_id = "YOUR_TENANT_ID"

# Set up the authentication parameters
token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
payload = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "resource": "https://graph.microsoft.com",
}
headers = {"Content-Type": "application/x-www-form-urlencoded"}

# Get the access token using the app credentials
response = requests.post(token_url, data=payload, headers=headers)
access_token = response.json()["access_token"]

# Calculate the date range for the last month
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=30)

# Convert the dates to ISO format
start_date_iso = start_date.isoformat()
end_date_iso = end_date.isoformat()

# Set up the query parameters for filtering messages
query_parameters = {
    "$filter": f"receivedDateTime ge {start_date_iso} and receivedDateTime le {end_date_iso}",
    "$select": "id,subject,hasAttachments",
}

# Send the request to Microsoft Graph API to fetch the messages
response = requests.get(messages_url, headers={"Authorization": f"Bearer {access_token}"}, params=query_parameters)
messages = response.json()["value"]

# Download attachments from messages with attachments
for message in messages:
    if message["hasAttachments"]:
        message_id = message["id"]
        attachments_url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments"

        response = requests.get(attachments_url, headers={"Authorization": f"Bearer {access_token}"})
        attachments = response.json()["value"]

        for attachment in attachments:
            attachment_id = attachment["id"]
            attachment_name = attachment["name"]
            download_url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments/{attachment_id}/$value"

            response = requests.get(download_url, headers={"Authorization": f"Bearer {access_token}"})

            # Save the attachment to the current directory
            with open(attachment_name, "wb") as f:
                f.write(response.content)
                print(f"Attachment '{attachment_name}' downloaded.")

print("Download complete.")
