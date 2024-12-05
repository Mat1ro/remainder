import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

logger = logging.getLogger(__name__)


class NotificationScheduler:
    """
    A class responsible for scheduling and sending notifications to users.

    This class uses the APScheduler library to schedule notifications based on a specific time.
    It allows adding tasks, sending notifications, and starting or stopping the scheduler.

    Attributes:
        scheduler (AsyncIOScheduler): An instance of APScheduler's AsyncIOScheduler to manage tasks.
        bot (Bot): An instance of the bot used to send notifications to users.
    """

    def __init__(self, bot):
        """
        Initializes the NotificationScheduler with a bot instance.

        Args:
            bot: An instance of the bot used to send messages to users.
        """
        self.scheduler = AsyncIOScheduler()
        self.bot = bot

    def add_task(self, note_id, remind_time, user_id, text):
        """
        Schedules a notification task for a specific note.

        This method adds a job to the scheduler that will send a notification to the user
        at the specified time (remind_time). The notification will include the note text.

        Args:
            note_id (str): The unique identifier for the note.
            remind_time (datetime): The time when the notification should be sent.
            user_id (int): The user to whom the notification will be sent.
            text (str): The content of the notification (note text).
        """
        self.scheduler.add_job(
            self.send_notification,
            trigger=DateTrigger(run_date=remind_time),
            args=(note_id, user_id, text)
        )
        logger.info(f"Task for note {note_id} scheduled at {remind_time}.")

    async def send_notification(self, note_id, user_id, text):
        """
        Sends a notification to the user at the scheduled time.

        This method is called when the scheduled time arrives. It sends a reminder message
        to the user with the content of the note.

        Args:
            note_id (str): The unique identifier for the note.
            user_id (int): The user to whom the notification will be sent.
            text (str): The content of the notification (note text).

        Logs an error if the notification fails to send.
        """
        try:
            await self.bot.send_message(user_id, f"🔔 Reminder:\n\n{text}")
            logger.info(f"Notification sent to user {user_id} for note {note_id}.")
        except Exception as e:
            logger.error(f"Error sending notification: {e}")

    def start(self):
        """
        Starts the scheduler to begin executing scheduled tasks.

        This method should be called to activate the scheduler and allow tasks to be executed at their specified times.
        """
        self.scheduler.start()

    def stop(self):
        """
        Stops the scheduler and shuts it down.

        This method can be used to stop the scheduler and prevent any further tasks from being executed.
        """
        self.scheduler.shutdown()
