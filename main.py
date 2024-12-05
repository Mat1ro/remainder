import logging

from bot import create_dispatcher, register_handlers
from bot.config import EnvBotConfig
from bot.factory import BotFactory
from bot.scheduler import NotificationScheduler

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def main():
    """
    The main entry point of the bot application.

    This function initializes the bot, sets up the dispatcher, creates a scheduler for notifications,
    and registers the necessary handlers. It then starts polling to listen for incoming messages.

    It performs the following tasks:
        1. Loads the bot configuration from the environment.
        2. Creates a bot instance using the `BotFactory`.
        3. Initializes the dispatcher.
        4. Sets up the notification scheduler.
        5. Registers handlers for different bot commands and states.
        6. Starts polling for updates and handling incoming messages.

    """
    config = EnvBotConfig()  # Load the bot configuration
    bot_factory = BotFactory(config)  # Create a bot factory
    bot = bot_factory.create_bot()  # Create a bot instance

    dp = create_dispatcher()  # Create the dispatcher for handling messages

    scheduler = NotificationScheduler(bot)  # Initialize the scheduler for notifications
    scheduler.start()  # Start the scheduler

    register_handlers(dp, scheduler)  # Register command and state handlers

    await dp.start_polling(bot)  # Start polling for updates


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
