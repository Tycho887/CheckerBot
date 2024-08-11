from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

scheduler = AsyncIOScheduler()

def schedule_daily_message(hour, minute, timezone_str, function):
    print(f"Scheduling daily message at {hour}:{minute} in timezone {timezone_str}")
    timezone = pytz.timezone(timezone_str)
    scheduler.add_job(function, CronTrigger(hour=hour, minute=minute, timezone=timezone))

def start_scheduler():
    scheduler.start()
