from celery import Celery
from dotenv import load_dotenv
import os
from celery.schedules import crontab
from app import app
from model.models import *
from mail_sender import send_email
load_dotenv()
import csv
from datetime import datetime

cel = Celery("intelliquest", broker="redis://127.0.0.1:6379/0")

# cel.conf.broker_url = os.environ.get("BROKER_URL")
cel.conf.result_backend = os.environ.get("RESULT_BACKEND")
cel.conf.broker_connection_retry_on_startup = True
cel.conf.timezone = 'Asia/Kolkata'

@cel.task()
def send_daily_reminder():
    with app.app_context():

        today = datetime.now().date()
        users = User.query.all()

        for user in users:
            # Check if user has any scores today
            attempted_today = Score.query.filter(
                Score.user_id == user.user_id,
                Score.time_stamp_of_attempt >= datetime.combine(today, datetime.min.time()),
                Score.time_stamp_of_attempt <= datetime.combine(today, datetime.max.time())
            ).first()

            if not attempted_today:
                html = f"""
                    <h3>Reminder to Attempt Quizzes!</h3>
                    <p>Hi {user.username}, you haven't visited today. There might be new quizzes waiting for you.</p>
                """
                send_email(
                    to=user.email,
                    subject="📝 IntelliQuest Daily Reminder",
                    html_content=html
                )
print("mail_sent")


@cel.task()
def send_monthly_report():
    with app.app_context():
        start_of_month = datetime.now().replace(day=1)

        for user in User.query.all():
            scores = Score.query.filter(
                Score.user_id == user.user_id,
                Score.time_stamp_of_attempt >= start_of_month
            ).all()

            total = len(scores)
            avg_score = round(sum([s.score for s in scores]) / total, 2) if total else 0

            html = f"""
                <h3>📊 Monthly Quiz Report for {user.username}</h3>
                <p>Quizzes Attempted: {total}</p>
                <p>Average Score: {avg_score}</p>
            """
            send_email(to=user.email, subject="📅 Your Monthly Quiz Summary", html_content=html)

@cel.task()
def export_user_quiz_csv(user_id, email):
    with app.app_context():
        user = User.query.get(user_id)
        scores = Score.query.filter_by(user_id=user_id).all()

        filename = f"user_export_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        filepath = os.path.join("static/exports", filename)

        with open(filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Quiz ID", "Chapter ID", "Date of Quiz", "Attempted at", "Total Score"])
            for s in scores:
                writer.writerow([s.quiz_id, s.quiz.chapter.chapter_id, s.quiz.start_time, s.time_stamp_of_attempt, s.total_scored])

        # Email Notification
        html = f"""
        <h3>Your quiz CSV export is ready!</h3>
        <p><a href="http://127.0.0.1:4001/static/exports/{filename}">Download CSV</a></p>
        """
        send_email(to=email, subject="📄 Your Quiz Export is Ready", html_content=html)



cel.conf.beat_schedule = {
    'send-daily-reminder': {
        'task': 'celery_app.send_daily_reminder',
        'schedule': crontab(hour=18, minute=48),  # Every 24 hours
    },
    'send-monthly-report': {
        'task': 'celery_app.send_monthly_report',
        'schedule': crontab(hour=8, minute=0, day_of_month='1'),
    },
}

