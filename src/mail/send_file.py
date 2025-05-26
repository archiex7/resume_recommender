import win32com.client
import os
import tempfile


def send_outlook_email(subject, body, to, attachment_path=None, sender=None):
    outlook = win32com.client.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)
    mail.Subject = subject
    mail.Body = body
    mail.To = to
    
    if sender:
        mail.Sender = sender

    if attachment_path:
        attachment_path = os.path.abspath(attachment_path)
        attachment_name = os.path.basename(attachment_path)
        attachment = mail.Attachments.Add(attachment_path, DisplayName=attachment_name)

    mail.Send()