import uuid
class Users:
    def __init__(self,user_id=None,name=None,email=None):
        self.user_id = user_id if user_id else str(uuid.uuid4())
        self.name=name
        self.email=email
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email
        }
    
    def __str__(self):
        return f"{self.user_id},{self.name},{self.email}"