import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from flask import render_template
from weasyprint import HTML


def generate_pdf(user_data):
    html = render_template('parent_user_report.html', **user_data)
    pdf = HTML(string=html).write_pdf()
    return pdf


def send_report_email(parent_email, child_name, pdf_data):
    smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))
    smtp_user = os.environ.get('SMTP_USER', '')
    smtp_pass = os.environ.get('SMTP_PASS', '')
    from_email = os.environ.get('FROM_EMAIL', smtp_user)

    if not smtp_user or not smtp_pass:
        raise ValueError("SMTP not configured. Set SMTP_USER and SMTP_PASS environment variables.")

    msg = MIMEMultipart('mixed')
    msg['Subject'] = f"{child_name}'s Progress Report - LEARNFUN"
    msg['From'] = from_email
    msg['To'] = parent_email

    body = MIMEText(f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px; color: #333;">
        <div style="max-width: 600px; margin: 0 auto;">
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #4F46E5, #7C3AED); border-radius: 12px; color: white;">
                <h1 style="margin: 0;">&#128218; Progress Report</h1>
                <p style="margin: 5px 0 0; opacity: 0.9;">{child_name}</p>
            </div>
            <div style="padding: 20px;">
                <p>Hi Parent,</p>
                <p>Please find attached <strong>{child_name}'s</strong> latest learning progress report from <strong>LEARNFUN Children Learning Web</strong>.</p>
                <p>The report includes quiz scores, subject progress, badges earned, and recent activity.</p>
                <p style="background: #F3F4F6; padding: 12px; border-radius: 8px; font-size: 0.9rem;">
                    &#128161; You can also view live reports anytime by logging into your Parent Dashboard.
                </p>
                <p>Happy Learning! &#127881;</p>
                <p style="color: #666; font-size: 0.85rem;">- LEARNFUN Team</p>
            </div>
            <div style="text-align: center; padding: 15px; font-size: 0.75rem; color: #999; border-top: 1px solid #eee;">
                LEARNFUN Children Learning Web &bull; Learn, Play, Grow!
            </div>
        </div>
    </body>
    </html>
    """, 'html')
    msg.attach(body)

    attachment = MIMEApplication(pdf_data, _subtype='pdf')
    safe_name = child_name.replace(' ', '_')
    attachment.add_header('Content-Disposition', 'attachment', filename=f'{safe_name}_report.pdf')
    msg.attach(attachment)

    with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
