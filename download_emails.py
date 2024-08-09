import imaplib
import datetime
import email
import os
import re
import PyPDF2
from pathlib import Path


# download attachments from emails for a given date range
def download_attachments_from_today():
    # connect to the hotmail IMAP server
    imap = imaplib.IMAP4_SSL('imap-mail.outlook.com')
    imap.login('innasherts@hotmail.com', 'inna2011')

    # select the inbox
    imap.select('INBOX').count()



    # search for all emails within the date range with attachments
    date = (datetime.date.today() - datetime.timedelta(days=30)).strftime('%d-%b-%Y')
    result, data = imap.uid('search', None, f'(SENTSINCE {date})', 'X-GM-RAW "has:attachment"')
    # print result subject and date of each email
    for uid in data[0].split():
        result, data = imap.uid('fetch', uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        print(email_message['Subject'], email_message['Date'])


if __name__ == '__main__':
    download_attachments_from_today()