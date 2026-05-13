import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_otp_email(to_email, otp):
    smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))
    smtp_user = os.environ.get('SMTP_USER', '')
    smtp_pass = os.environ.get('SMTP_PASS', '')
    from_email = os.environ.get('FROM_EMAIL', smtp_user)

    if not smtp_user or not smtp_pass:
        return False

    subject = 'Your LearnFun Password Reset Code'
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <div style="max-width: 480px; margin: 0 auto; background: #f0f9ff; border-radius: 16px; padding: 24px; border: 2px solid #60a5fa;">
            <h2 style="color: #1e40af; margin-top: 0;">Password Reset</h2>
            <p style="font-size: 16px; color: #333;">Use this code to reset your LearnFun password:</p>
            <div style="background: white; border-radius: 12px; padding: 20px; text-align: center; margin: 16px 0;">
                <span style="font-size: 36px; font-weight: 900; letter-spacing: 8px; color: #1e40af;">{otp}</span>
            </div>
            <p style="font-size: 14px; color: #666;">This code expires in <strong>10 minutes</strong>.</p>
            <p style="font-size: 14px; color: #666;">If you didn't request this, you can ignore this email.</p>
        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
        return True
    except smtplib.SMTPAuthenticationError:
        return False
    except Exception:
        return False
