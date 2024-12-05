from aiogram.fsm.state import StatesGroup, State


class NoteCreationState(StatesGroup):
    """
    A state machine class representing the states during the note creation process.

    This class defines the states in the process of creating a note, where the bot waits
    for the user to input the text of the note and the time associated with it.

    States:
        waiting_for_note_text: State where the bot waits for the user to input the note's text.
        waiting_for_note_time: State where the bot waits for the user to input the time for the note.
    """

    waiting_for_note_text = State()
    waiting_for_note_time = State()
