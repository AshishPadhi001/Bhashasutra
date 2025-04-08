import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from jinja2 import Template

from BackEnd.src.core.config import settings
from BackEnd.src.utils.logger import logger


class EmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.sender_email = settings.SENDER_EMAIL
        self.templates_dir = Path(__file__).parent.parent / "templates" / "emails"

    def _get_template(self, template_name):
        """Load email template from file"""
        template_path = self.templates_dir / template_name
        with open(template_path, "r", encoding="utf-8") as f:  # ✅ specify encoding
            template_content = f.read()
        return Template(template_content)

    def send_welcome_email(self, user_email, user_name):
        """Send welcome email to newly registered users"""
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = "Welcome to Bhashasutra!"
            message["From"] = self.sender_email
            message["To"] = user_email

            # Render template
            template = self._get_template("welcome.html")
            html = template.render(user_name=user_name)

            # Attach HTML part
            html_part = MIMEText(html, "html")
            message.attach(html_part)

            # Connect to server and send
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(self.sender_email, user_email, message.as_string())

            logger.info(f"Welcome email sent to {user_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send welcome email to {user_email}: {str(e)}")
            return False
