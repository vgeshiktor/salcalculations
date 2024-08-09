# import the library
import calendar
import datetime
import locale
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import PyPDF2


def send_email(subject, body, to_email, attachment_path):
    # Set up the email server details for Outlook.com
    smtp_server = "smtp-mail.outlook.com"
    smtp_port = 587
    smtp_username = "innasherts@hotmail.com"
    smtp_password = "inna2011"

    # Set up the email message
    msg = MIMEMultipart()
    msg["From"] = smtp_username
    msg["To"] = to_email
    msg["Subject"] = subject

    # Attach the PDF file
    attachment = open(attachment_path, "rb")
    part = MIMEBase("application", "pdf")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f'attachment; filename="{Path(attachment_path).name}"',
    )
    msg.attach(part)

    # Attach the body text
    msg.attach(MIMEText(body, "plain"))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_email, msg.as_string())

    print("Email sent successfully!")


locale.setlocale(locale.LC_ALL, "he_IL.UTF-8")
workers_base_folder: str = r"C:\Users\innas\OneDrive\Рабочий стол\workers"

workers: dict[str, dict[str, str]] = {
    "36155331": {
        "name": "Yaarit Fridman",
        "name_he": "יערית פרידמן",
        "prefix": "yaarit-fridman",
        "folder": "",
        "email": "fridman.roni@gmail.com",
    },
    "60176187": {
        "name": "Gali Ater",
        "name_he": "גלי עטר",
        "prefix": "gali-ater",
        "folder": "",
        "email": "galiatar10@gmail.com",
    },
    "323336792": {
        "name": "Natalia Himchenko",
        "name_he": "נטליה חימצ'נקו",
        "prefix": "natalia-himchenko",
        "folder": "",
        "email": "nata051873@gmail.com",
    },
    # '323586628':    {'name': 'Victoria Brosilovski',    'prefix': 'victoria-brosilovski',   'folder': '', 'email': ''},
    "302898507": {
        "name": "Alisheva Malka",
        "name_he": "אלישבע מלכה",
        "prefix": "alisheva-malka",
        "folder": "",
        "email": "e0509302023@gmail.com",
    },
    # '345313316':    {'name': 'Daniela Rezhnovski',      'prefix': 'daniela-rezhnovski',     'folder': '', 'email': ''},
    # '200899615':    {'name': 'Shachar Neemani',         'prefix': 'shachar-Neemani',        'folder': '', 'email': ''},
    # '336274600':    {'name': 'Irina Kaplan',            'prefix': 'irina-kaplan',           'folder': '', 'email': ''},
    "345323117": {
        "name": "Natalia Burianov",
        "name_he": "נטליה בוריאנוב",
        "prefix": "natalia-burianov",
        "folder": "",
        "email": "schatzi2@yandex.ru",
    },
    "311072508": {
        "name": "Ilana Tzemah",
        "name_he": "אילנה צמח",
        "prefix": "ilana-tzemah",
        "folder": "",
        "email": "ilanazemach94@gmail.com",
    },
    "302615372": {
        "name": "Moran Hilo",
        "name_he": "מורן חילו",
        "prefix": "moran-hilo",
        "folder": "",
        "email": "moranhilu@gmail.com",
    },
    "308236371": {
        "name": "Nofar Erlich",
        "name_he": "נופר ארליך",
        "prefix": "nofar-erlich",
        "folder": "",
        "email": "dudie38@gmail.com",
    },
    "307418871": {
        "name": "Orit Podkaminski",
        "name_he": "אורית פודקמינסקי",
        "prefix": "orit-podkaminski",
        "folder": "",
        "email": "oritpod790@gmail.com",
    },
    "320721582": {
        "name": "Tamara Alexandrov",
        "name_he": "תמרה אלכסנדרוב",
        "prefix": "tamara-alexandrov",
        "folder": "",
        "email": "alexsandrovtamara@gmail.com",
    },
    "342377876": {
        "name": "Mirna Sirey",
        "name_he": "סירי מירנה",
        "prefix": "mirna-sirey",
        "folder": "",
        "email": "innasherts@hotmail.com",
    },
}

# open the PDF file
pdf_file = open(
    r"C:\Users\innas\OneDrive\Рабочий стол\workers\salaries\sal-slip-archive\sal-06-2024.pdf",
    "rb",
)

# create a PDF Reader object
pdf_reader = PyPDF2.PdfReader(pdf_file)

# loop through the pages
for page_num in range(len(pdf_reader.pages)):
    # create a PDF Writer object for each page
    pdf_writer = PyPDF2.PdfWriter()

    # add the page to the writer object
    page = pdf_reader.pages[page_num]
    pdf_writer.add_page(page)

    # extract text from pdf
    text: str = page.extract_text()
    text.replace("\n", "")

    # get current month and year
    import dateutil.relativedelta

    now = datetime.datetime.now()
    payment_date = now + dateutil.relativedelta.relativedelta(months=-1)

    # iterate over workers dict
    for worker_id, worker in workers.items():
        name = worker["name"]
        prefix = worker["prefix"]
        # to_email = 'innasherts@hotmail.com'
        to_email = worker["email"]

        if text.find(worker_id) != -1:
            # create a new file
            page_file_name = (
                rf"{workers_base_folder}\{name}\salaries\{prefix}-{worker_id}-"
                rf"{payment_date.month}-{payment_date.year}.pdf"
            )
            print(f"creating file for {name}: \t\t\t {page_file_name}")

            if not os.path.exists(os.path.dirname(page_file_name)):
                os.makedirs(os.path.dirname(page_file_name))

            if os.path.exists(page_file_name):
                print(f"file {page_file_name} already exists")
                continue

            new_pdf_file = open(page_file_name, "wb")

            # write the page to a new file
            pdf_writer.write(new_pdf_file)

            # close new pdf file
            new_pdf_file.close()

            email = worker["email"]
            name_he = worker["name_he"]
            print(f"sending email to {email}")
            title = f"תלוש שכר עבור"
            subject = f"{payment_date.year} {calendar.month_name[payment_date.month]} {title}"
            print(f"subject: {subject}")
            print(f"\n")
            body = (
                f"שלום {name_he},\n\nמצורף תלוש שכר עבור {calendar.month_name[payment_date.month]} "
                f"{payment_date.year}.\n\nבברכה,\nאינה"
            )
            print(f"body: {body}")
            send_email(subject, body, to_email, page_file_name)

# close the original PDF file
pdf_file.close()
