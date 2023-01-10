class MemoryDB:
    def __init__(self) -> None:
        self.db = {}

    def update_kv(self, key, value):
        self.db[key] = value

    def get_value(self, key):
        return self.db[key] if key in self.db else None
