class Series:
    def __init__(self, id:int, title:str, seasons:int, platform:str):
        self.id = id
        self.title = title
        self.seasons = seasons
        self.platform = platform

    def to_dict(self):
        # Devuelve una representación serializable a JSON
        return {
            "id": self.id,
            "title": self.title,
            "seasons": self.seasons,
            "platform": self.platform
        }
