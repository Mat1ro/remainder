import logging
from aiogram import Bot

logger = logging.getLogger(__name__)


class BotFactory:
    """
    A factory class responsible for creating and initializing a Telegram bot.

    Attributes:
        config: The configuration object that provides the bot's token.
    """

    def __init__(self, config):
        self.config = config

    def create_bot(self) -> Bot:
        """
        Creates an instance of the Bot using the token from the configuration.

        This method attempts to retrieve the token from the configuration, initializes the Bot,
        and returns it. In case of any errors during initialization, an error is logged.

        Returns:
            Bot: An initialized Bot instance.

        Raises:
            Exception: If there is an error during bot initialization, the exception is logged and re-raised.
        """
        try:
            token = self.config.get_token()
            bot = Bot(token=token)
            logger.info("Bot initialized successfully.")
            return bot
        except Exception as e:
            logger.error(f"Error initializing bot: {e}")
            raise
