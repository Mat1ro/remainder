import logging
import os
from abc import ABC, abstractmethod

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class BotConfig(ABC):
    """
    Abstract base class for bot configuration.

    This class defines the interface for obtaining the bot's token, which must
    be implemented by any subclass.
    """

    @abstractmethod
    def get_token(self) -> str:
        """
        Retrieve the bot token.

        Returns:
            str: The bot token.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        pass


class EnvBotConfig(BotConfig):
    """
    Bot configuration that retrieves the token from environment variables.

    This implementation uses the `python-dotenv` library to load environment
    variables from a `.env` file.
    """

    def get_token(self) -> str:
        load_dotenv()
        token = os.getenv("BOT_TOKEN")
        if not token:
            logger.error("BOT_TOKEN not found in environment variables.")
            raise ValueError("BOT_TOKEN not found in environment variables.")
        return token
