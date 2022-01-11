import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from sql.methods import delete_old_urls


scheduler = BackgroundScheduler(timezone="Europe/Warsaw")

scheduler.add_job(delete_old_urls, 'cron', hour=0)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())
