import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def send_email(subject, body, to_email, attachment_path):
    # Set up the email server details for Outlook.com
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587
    smtp_username = 'innasherts@hotmail.com'
    smtp_password = 'inna2011'

    # Set up the email message
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the PDF file
    attachment = open(attachment_path, 'rb')
    part = MIMEBase('application', 'pdf')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{attachment_path}"')
    msg.attach(part)

    # Attach the body text
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_email, msg.as_string())

    print("Email sent successfully!")


def main():
    # Example usage
    subject = 'המשכורת לחודש ספטמבר 2021'
    body = rf'שלום, מצ"ב המשכורת שלך לחודש ספטמבר 2021.'
    to_email = 'innasherts@hotmail.com'
    attachment_path = rf'C:\Users\innas\OneDrive\Рабочий стол\workers\Alisheva Malka\salaries\alisheva-malka-302898507-9-2023.pdf'

    send_email(subject, body, to_email, attachment_path)


if __name__ == '__main__':
    main()