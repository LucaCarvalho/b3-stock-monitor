from email.mime import base
import logging
from pprint import pformat

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from tunnel_monitor.utils.ticker import log_quotes
from os import getenv

logger = logging.getLogger(__name__)

# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way. 
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.
    
    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

# Lambdas apparently don't work, so... no simple way to automate this :(
def every_1():
    log_quotes(1)
def every_5():
    log_quotes(5)
def every_15():
    log_quotes(15)
def every_60():
    log_quotes(60)
def every_1440():
    log_quotes(1440)

class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        start_hour = getenv("START_HOUR", 10)
        end_hour = getenv("END_HOUR", 17)

        # Schedule jobs for every interval < 60 min
        intervals = {1: every_1, 5: every_5, 15:every_15}
        for interval, func in intervals.items():
            scheduler.add_job(
                func,
                trigger=CronTrigger(
                    day_of_week="0-4",
                    hour=f"{start_hour}-{end_hour}",
                    minute=f"*/{interval}"
                ),
                id=f"check_every_{interval}",  # The `id` assigned to each job MUST be unique
                max_instances=1,
                replace_existing=True,
            )
            self.stdout.write(f"Added job 'check_every_{interval}'.")

        # Schedule job for every 1h
        interval = "1h"
        scheduler.add_job(
            every_60,
            trigger=CronTrigger(
                day_of_week="0-4",
                hour=f"{start_hour}-{end_hour}/1",
            ),
            id=f"check_every_{interval}",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        self.stdout.write(f"Added job 'check_every_{interval}'.")

        # Schedule job for every 1d
        interval  ="1d"
        scheduler.add_job(
            every_1440,
            trigger=CronTrigger(
                day_of_week="0-4",
                hour=f"{start_hour}-{end_hour}",
            ),
            id=f"check_every_{interval}",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        self.stdout.write(f"Added job 'check_every_{interval}'.")

        self.stderr.write(pformat(scheduler.get_jobs()))
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
              day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        self.stdout.write(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            self.stdout.write("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            self.stderr.write("Stopping scheduler...")
            scheduler.shutdown()
            self.stderr.write("Scheduler shut down successfully!")
