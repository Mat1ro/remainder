class NoteManager:
    """
    A class responsible for managing notes.

    This class allows creating and storing notes, each with a unique ID, associated user ID,
    text content, and reminder time.

    Attributes:
        notes (dict): A dictionary that stores notes by their unique ID.
    """

    def __init__(self):
        self.notes = {}

    def create_note(self, note_id, user_id, text, remind_time):
        """
        Creates a new note and stores it in the notes dictionary.

        This method adds a new note to the `notes` dictionary with the provided note ID,
        user ID, text content, and reminder time.

        Args:
            note_id (int): The unique identifier for the note.
            user_id (int): The ID of the user who created the note.
            text (str): The content of the note.
            remind_time (datetime): The time when the reminder for the note should be triggered.

        Returns:
            dict: The created note, represented as a dictionary with keys "user_id", "text", and "time".
        """
        self.notes[note_id] = {"user_id": user_id, "text": text, "time": remind_time}
        return self.notes[note_id]
