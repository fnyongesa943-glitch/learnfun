import os
import smtplib
from email.mime.text import MIMEText


def _build_email_html(data):
    user = data['user']
    badge_defs = {
        'First Steps': '🌟', 'Perfect Score': '💯', 'Math Star': '🔢',
        'Reading Pro': '📚', 'Science Wizard': '🔬', 'Geo Explorer': '🌍',
        'Quiz Master': '🎯', 'Champion': '🏆', 'Rocket Learner': '🚀',
        'On Fire': '🔥', 'Dedicated': '💎',
    }
    badges_html = ''
    for b in data['badges']:
        icon = badge_defs.get(b.badge_name, '🏅')
        badges_html += f'<span style="display:inline-block;padding:8px 12px;margin:4px;background:#F3F4F6;border-radius:8px;">{icon} {b.badge_name}</span>'

    subject_rows = ''
    for s in data['subject_progress']:
        subject_rows += f'''
        <tr>
            <td style="padding:8px 12px;border-bottom:1px solid #eee;">{s['icon']} {s['name']}</td>
            <td style="padding:8px 12px;border-bottom:1px solid #eee;text-align:center;">{s['percentage']}%</td>
            <td style="padding:8px 12px;border-bottom:1px solid #eee;text-align:center;">{s['completed']}/{s['total']}</td>
            <td style="padding:8px 12px;border-bottom:1px solid #eee;text-align:center;">{s['best_score']}%</td>
        </tr>'''

    activity_html = ''
    for a in data['recent_activity'][:5]:
        emoji = '🟢' if a['score'] >= 70 else ('🟡' if a['score'] >= 50 else '🔴')
        activity_html += f'<tr><td style="padding:6px 12px;border-bottom:1px solid #f0f0f0;">{a["subject_icon"]} {a["quiz_title"]}</td><td style="padding:6px 12px;border-bottom:1px solid #f0f0f0;text-align:center;">{emoji} {a["score"]}%</td><td style="padding:6px 12px;border-bottom:1px solid #f0f0f0;color:#999;font-size:0.85rem;">{a["completed_at"].strftime("%b %d, %Y") if a["completed_at"] else ""}</td></tr>'

    return f"""<html>
<body style="font-family:Arial,sans-serif;margin:0;padding:0;background:#f5f5f5;">
<div style="max-width:600px;margin:0 auto;background:white;">
    <div style="text-align:center;padding:30px 20px;background:linear-gradient(135deg,#4F46E5,#7C3AED);border-radius:0 0 20px 20px;color:white;">
        <h1 style="margin:0;font-size:1.5rem;">📚 {user.username}'s Progress Report</h1>
        <p style="margin:5px 0 0;opacity:0.9;">Level {user.level} • {user.total_points} pts • {user.streak_days} day streak</p>
    </div>
    <div style="padding:20px;">
        <h2 style="font-size:1.1rem;color:#333;margin:0 0 15px;">📊 Overview</h2>
        <table style="width:100%;border-collapse:collapse;margin-bottom:20px;">
            <tr>
                <td style="padding:15px;text-align:center;background:#EEF2FF;border-radius:12px;width:50%;">
                    <div style="font-size:1.8rem;font-weight:800;color:#4F46E5;">{data['total_quizzes']}</div>
                    <div style="font-size:0.8rem;color:#666;">Quizzes Done</div>
                </td>
                <td style="width:10px;"></td>
                <td style="padding:15px;text-align:center;background:#F0FDF4;border-radius:12px;width:50%;">
                    <div style="font-size:1.8rem;font-weight:800;color:#059669;">{data['avg_score']}%</div>
                    <div style="font-size:0.8rem;color:#666;">Average Score</div>
                </td>
            </tr>
        </table>

        <h2 style="font-size:1.1rem;color:#333;margin:20px 0 15px;">📖 Subject Progress</h2>
        <table style="width:100%;border-collapse:collapse;margin-bottom:20px;">
            <thead><tr style="background:#F9FAFB;"><th style="padding:8px 12px;text-align:left;font-size:0.8rem;color:#666;">Subject</th><th style="padding:8px 12px;text-align:center;font-size:0.8rem;color:#666;">Progress</th><th style="padding:8px 12px;text-align:center;font-size:0.8rem;color:#666;">Done</th><th style="padding:8px 12px;text-align:center;font-size:0.8rem;color:#666;">Best</th></tr></thead>
            <tbody>{subject_rows}</tbody>
        </table>

        <h2 style="font-size:1.1rem;color:#333;margin:20px 0 15px;">🏅 Badges ({data['badges']|length})</h2>
        <div style="margin-bottom:20px;">{badges_html if badges_html else '<p style="color:#999;">No badges earned yet.</p>'}</div>

        <h2 style="font-size:1.1rem;color:#333;margin:20px 0 15px;">📈 Recent Quiz Activity</h2>
        <table style="width:100%;border-collapse:collapse;margin-bottom:20px;">
            <thead><tr style="background:#F9FAFB;"><th style="padding:6px 12px;text-align:left;font-size:0.8rem;color:#666;">Quiz</th><th style="padding:6px 12px;text-align:center;font-size:0.8rem;color:#666;">Score</th><th style="padding:6px 12px;text-align:center;font-size:0.8rem;color:#666;">Date</th></tr></thead>
            <tbody>{activity_html if activity_html else '<tr><td colspan="3" style="padding:12px;text-align:center;color:#999;">No quizzes taken yet.</td></tr>'}</tbody>
        </table>

        <p style="text-align:center;margin:20px 0 0;">
            <a href="https://learnfun.onrender.com/parent/" style="display:inline-block;padding:12px 24px;background:#4F46E5;color:white;text-decoration:none;border-radius:8px;font-weight:700;">View Live Dashboard →</a>
        </p>
    </div>
    <div style="text-align:center;padding:15px;font-size:0.75rem;color:#999;border-top:1px solid #eee;">
        LEARNFUN Children Learning Web • Learn, Play, Grow!
    </div>
</div>
</body>
</html>"""


def send_report_email(parent_email, child_name, user_data):
    smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))
    smtp_user = os.environ.get('SMTP_USER', '')
    smtp_pass = os.environ.get('SMTP_PASS', '')
    from_email = os.environ.get('FROM_EMAIL', smtp_user)

    if not smtp_user or not smtp_pass:
        raise ValueError("SMTP not configured. Set SMTP_USER and SMTP_PASS environment variables.")

    html = _build_email_html(user_data)

    msg = MIMEText(html, 'html')
    msg['Subject'] = f"{child_name}'s Progress Report - LEARNFUN"
    msg['From'] = from_email
    msg['To'] = parent_email

    with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
