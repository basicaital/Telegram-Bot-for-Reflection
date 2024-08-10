class MoodTracker:
    mood_data = {}

    @classmethod
    def save_mood(cls, user_id: int, mood: int):
        cls.mood_data[user_id] = mood
