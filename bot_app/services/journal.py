from datetime import datetime


class Journal:
    journal_entries = {}

    @classmethod
    def add_entry(cls, user_id: int, entry: str):
        if user_id not in cls.journal_entries:
            cls.journal_entries[user_id] = []
        cls.journal_entries[user_id].append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'entry': entry
        })

    @classmethod
    def get_entries(cls, user_id: int):
        if user_id not in cls.journal_entries:
            return "У вас нет записей."
        return "\n\n".join(
            [f"<b>{entry['timestamp']}</b>:\n📝{entry['entry']}" for entry in cls.journal_entries[user_id]])

    @classmethod
    def get_entry_by_index(cls, user_id: int, index: int):
        if user_id not in cls.journal_entries or not cls.journal_entries[user_id]:
            return None
        entries = cls.journal_entries[user_id]
        if index < 0 or index >= len(entries):
            return None
        return entries[index]
