# email
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# infrastructure
import configparser
from pathlib import Path
from .prettyprint import prettyprint as pprint, MessageType as mt


class Postman():

    def __init__(self, config_global: configparser.ConfigParser,) -> None:
        # debugging mode
        self.debug = config_global['app']['debug'] == 'True'

        self.credentials = {
            'user': config_global['email']['user'], 'pass': config_global['email']['pass']}
        self.sender = config_global['email']['user']
        self.recipients = config_global['email']['recipients'].split(', ')
        self.subject = 'New Chatlog from PolyBot'
        self.body = 'Hi!\nAnother user just chatted with me. I\'ve attached the conversation.\n\nCheers!\n\n'
        self.error_body = 'Hi!\nAnother user just chatted with me. Unfortunately there was an error when creating the chat log attachment, so I couldn\'t attach it.\n\nSad PolyBot noises\n\n'
        self.chatlogs_dir = Path("../chat_logs")

    def send(self, filename: str):
        """
        sends the most recent chat log to receiver
        """

        filepath = self.chatlogs_dir / Path(f'{filename}.json')

        # create message object instance
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = ', '.join(self.recipients)
        msg['Subject'] = self.subject

        # create message and attachment
        try:
            with open(filepath, 'rb') as f:
                attachment = MIMEApplication(f.read())
                attachment.add_header(
                    'Content-Disposition', 'attachment', filename=f'{filename}.json')
        except Exception as e:
            msg.attach(MIMEText(self.error_body +
                       f'\nHere is the error message:\n{e}', 'plain'))
            pprint(f'Error when creating email attachment: {e}', msg_type=mt.ERROR)
        else:
            msg.attach(MIMEText(self.body, 'plain'))
            msg.attach(attachment)

        if self.debug:
            pprint('Debugging mode is on, not sending email', msg_type=mt.WARNING)
            return
        else:
            try:
                # create server
                server = smtplib.SMTP('mail.gmx.com', 587)
                # establish secure connection
                server.starttls()
                # Login to server
                server.login(self.credentials['user'],
                             self.credentials['pass'])
                # send the message via the server
                server.sendmail(self.sender, self.recipients, msg.as_string())
                # end server
                server.quit()
            except smtplib.SMTPException as e:
                pprint([f'SMTP error occurred: {e}'], msg_type=mt.INFO)
            except Exception as e:
                pprint([f'Error while sending email: {e}'], msg_type=mt.INFO)
            else:
                pprint(
                    f'Successfully sent chatlog {filename.split("_")[-1]} to {msg["To"]}', msg_type=mt.SUCCESS)
