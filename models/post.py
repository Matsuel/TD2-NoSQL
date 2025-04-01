from datetime import datetime

class Post:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.created_at = datetime.now()