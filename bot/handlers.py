from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.scheduler import NotificationScheduler
from bot.states import NoteCreationState
from services.note_manager import NoteManager


async def start_command(message: Message):
    """
    Handles the `/start` command.

    This method sends a greeting message to the user when they start the bot,
    informing them about the bot's functionality and how to create a reminder.

    Args:
        message (Message): The message object containing information about the incoming command.
    """
    await message.answer("Hello! I'm a notification bot. Use /note to create a reminder.")


async def create_note_command(message: Message, state: FSMContext):
    """
    Handles the `/note` command to initiate the note creation process.

    This method prompts the user to enter the text of the note they wish to save.
    The bot expects the user to provide the note text first.

    Args:
        message (Message): The message object containing information about the incoming command.
        state (FSMContext): The Finite State Machine context that keeps track of the user's progress.
    """
    await message.answer(
        "Enter the note text you want to save.\n\nExample: `Call mom`",
        parse_mode="Markdown"
    )
    await state.set_state(NoteCreationState.waiting_for_note_text)


async def handle_note_text(message: Message, state: FSMContext):
    """
    Handles the user's input for the note text.

    This method updates the state with the note text provided by the user and prompts
    the user to enter the reminder time.

    Args:
        message (Message): The message object containing the user's note text.
        state (FSMContext): The Finite State Machine context that keeps track of the user's input state.
    """
    await state.update_data(note_text=message.text)
    await message.answer(
        "Now, enter the reminder time in the format: `YYYY-MM-DD HH:MM`\n\nExample: `2024-12-05 18:30`",
        parse_mode="Markdown"
    )
    await state.set_state(NoteCreationState.waiting_for_note_time)


async def handle_note_time(
        message: Message,
        state: FSMContext,
        note_manager: NoteManager,
        scheduler: NotificationScheduler
):
    """
    Handles the user's input for the reminder time and schedules the notification.

    This method processes the reminder time provided by the user, validates it, and creates
    a new note. It then schedules a notification for the user at the specified time using
    the NotificationScheduler.

    Args:
        message (Message): The message object containing the user's reminder time input.
        state (FSMContext): The Finite State Machine context that holds the user's note text.
        note_manager (NoteManager): The NoteManager instance used to create and manage notes.
        scheduler (NotificationScheduler): The NotificationScheduler instance used to schedule notifications.

    Raises:
        ValueError: If the user input for the reminder time is in an invalid format.
    """
    try:
        remind_time = datetime.strptime(message.text.strip(), "%Y-%m-%d %H:%M")

        if remind_time < datetime.now():
            await message.reply("You specified a past time. Please enter a valid date and time.")
            return

        data = await state.get_data()
        note_text = data["note_text"]
        note_id = len(note_manager.notes) + 1
        note = note_manager.create_note(note_id, message.from_user.id, note_text, remind_time)

        scheduler.add_task(note_id, remind_time, note["user_id"], note["text"])

        await message.reply(
            f"Note created successfully!\n\nText: {note_text}\nTime: {remind_time}"
        )
        await state.clear()
    except ValueError:
        await message.reply(
            "Invalid time format. Please use the format: `YYYY-MM-DD HH:MM`"
        )
