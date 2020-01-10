from jinja2 import FileSystemLoader, Environment, select_autoescape
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP


class EmailNotifier:
    BLOCKED_TEMPLATE = {'html': 'blocked_notification.html', 'txt': 'blocked_notification.txt'}

    def __init__(self, config):
        file_loader = FileSystemLoader('templates')
        self.jinja_env = Environment(loader=file_loader, autoescape=select_autoescape())
        self.config = config

    def render_blocked_notification(self, template_uri, recipient_name, blocked_result):
        """Render the HTML template for the 'Blocked IP' notification."""
        template = self.jinja_env.get_template(template_uri)
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
        html = self.render_blocked_notification(self.BLOCKED_TEMPLATE['html'], recipient['name'], blocked_result)
        txt = self.render_blocked_notification(self.BLOCKED_TEMPLATE['txt'], recipient['name'], blocked_result)
        message.attach(MIMEText(html, 'html', _charset='utf-8' if not html.isascii() else None))
        message.attach(MIMEText(txt, 'txt', _charset='utf-8' if not html.isascii() else None))
        return message.as_string()
