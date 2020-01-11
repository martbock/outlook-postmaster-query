from jinja2 import FileSystemLoader, Environment, select_autoescape
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP, SMTPException

from exceptions import EmailException


class EmailNotifier:
    BLOCKED_TEMPLATE = {'html': 'blocked_notification.html', 'txt': 'blocked_notification.txt'}

    def __init__(self, config):
        file_loader = FileSystemLoader('templates')
        self.jinja_env = Environment(loader=file_loader, autoescape=select_autoescape())
        self.config = config

    def _render_blocked_notification(self, template_uri, recipient_name, blocked_result):
        """Render the HTML template for the 'Blocked IP' notification."""
        template = self.jinja_env.get_template(template_uri)
        return template.render(
            recipient_name=recipient_name,
            table=blocked_result,
            ip_range_count=len(blocked_result),
            homepage_url=self.config['outlook']['links']['homepage'],
            delisting_url=self.config['outlook']['links']['delisting'],
        )

    def build_email(self, recipient: dict, blocked_result: list):
        """Build a MIME Multipart email that has both alternatives html and plain-text."""
        sender = self.config['email']['sender']
        message = MIMEMultipart(_subtype='alternative')
        message['Subject'] = self.config['email']['subject']
        message['From'] = f"{sender['name']} <{sender['email']}>"
        message['To'] = f"{recipient['name']} <{recipient['email']}>"
        html = self._render_blocked_notification(self.BLOCKED_TEMPLATE['html'], recipient['name'], blocked_result)
        txt = self._render_blocked_notification(self.BLOCKED_TEMPLATE['txt'], recipient['name'], blocked_result)
        message.attach(MIMEText(html, 'html', _charset='utf-8' if not html.isascii() else None))
        message.attach(MIMEText(txt, 'plain', _charset='utf-8' if not html.isascii() else None))
        return message.as_string()

    def send(self, recipient_email: str, message: str):
        """Send an email message to a recipient."""
        try:
            connection = SMTP(
                host=self.config['email']['smtp']['server'],
                port=self.config['email']['smtp']['port']
            )
            connection.starttls()
            connection.login(
                user=self.config['email']['smtp']['user'],
                password=self.config['email']['smtp']['password']
            )
            connection.sendmail(
                from_addr=self.config['email']['sender']['email'],
                to_addrs=recipient_email,
                msg=message
            )
            connection.quit()
        except SMTPException as e:
            raise EmailException(e)
