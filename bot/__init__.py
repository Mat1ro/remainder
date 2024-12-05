from functools import partial
from aiogram import Dispatcher
from aiogram.filters import Command
from bot.handlers import start_command, create_note_command, handle_note_text, handle_note_time
from bot.scheduler import NotificationScheduler
from bot.states import NoteCreationState
from services.note_manager import NoteManager

note_manager = NoteManager()
scheduler: NotificationScheduler = None

def register_handlers(dp: Dispatcher, scheduler_instance: NotificationScheduler):
    """
    Registers the bot's command and state handlers with the given dispatcher.

    This function registers the handlers for the `/start`, `/note`, and state-based
    commands. It also passes the scheduler instance to the `handle_note_time` handler.

    Args:
        dp (Dispatcher): The dispatcher instance responsible for handling incoming messages.
        scheduler_instance (NotificationScheduler): The scheduler instance used for scheduling notifications.
    """
    global scheduler
    scheduler = scheduler_instance

    # Registering handlers for specific commands and states
    dp.message.register(start_command, Command("start"))
    dp.message.register(create_note_command, Command("note"))
    dp.message.register(
        handle_note_text,
        NoteCreationState.waiting_for_note_text
    )
    dp.message.register(
        partial(handle_note_time, note_manager=note_manager, scheduler=scheduler),
        NoteCreationState.waiting_for_note_time
    )


def create_dispatcher() -> Dispatcher:
    """
    Creates and returns a new instance of the Dispatcher with memory storage.

    This function initializes the Dispatcher used by the bot, with in-memory storage
    for managing states across different handlers.

    Returns:
        Dispatcher: A new instance of the Dispatcher with MemoryStorage.
    """
    from aiogram.fsm.storage.memory import MemoryStorage
    return Dispatcher(storage=MemoryStorage())
