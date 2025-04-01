from datetime import datetime

class Commentaire:
    def __init__(self, content, post_id):
        self.content = content
        self.post_id = post_id
        self.created_at = datetime.now()