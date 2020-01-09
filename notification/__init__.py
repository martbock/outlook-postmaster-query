from jinja2 import FileSystemLoader, Environment, select_autoescape
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP


class EmailNotifier:
    BLOCKED_TEMPLATE = 'blocked_notification.html'

    def __init__(self, config):
        file_loader = FileSystemLoader('templates')
        self.jinja_env = Environment(loader=file_loader, autoescape=select_autoescape())
        self.config = config

    def render_blocked_notification(self, recipient_name, blocked_result):
        """Render the HTML template for the 'Blocked IP' notification."""
        template = self.jinja_env.get_template(self.BLOCKED_TEMPLATE)
        return template.render(
            recipient_name=recipient_name,
            table=blocked_result,
            homepage_url=self.config['outlook']['links']['homepage'],
            delisting_url=self.config['outlook']['links']['delisting'],
        )

    def build_email(self, recipient, sender, blocked_result):
        message = MIMEMultipart()
        message['Subject'] = ''
        message['From'] = f"{recipient['name']} <{recipient['email']}>"
        message['To'] = f"{sender['name']} <{sender['email']}>"
        html = self.render_blocked_notification(recipient['name'], blocked_result)
        message.attach(MIMEText(html, 'html'))
        text_only = message.as_string()
        return message, text_only
