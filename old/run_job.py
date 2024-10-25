from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import logging


# Set up logging to monitor the scheduler
logging.basicConfig(level=logging.INFO)

# Create scheduler instance
scheduler = BlockingScheduler()

# Function to execute your Python script
def run_my_script():
    try:
        # Import and run your script
        # Or you can use exec() to run the script from file
        exec(open('bing.py').read())
        logging.info("Script executed successfully")
    except Exception as e:
        logging.error(f"Error executing script: {e}")

# Schedule the job to run at 4 AM every day
scheduler.add_job(
    run_my_script,
    trigger=CronTrigger(hour=4, minute=0),
    id='daily_task',
    name='Run script at 4 AM daily',
    misfire_grace_time=60  # Allow 60 seconds of delay if system is busy
)

if __name__ == '__main__':
    try:
        logging.info("Scheduler starting...")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()