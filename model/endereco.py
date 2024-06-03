import uuid
class Endereco:
    def __init__(self, endereco_id=None, logradouro=None, bairro=None, user_id=None):
        self.endereco_id = endereco_id if endereco_id else str(uuid.uuid4())
        self.logradouro = logradouro
        self.bairro = bairro
        self.user_id = user_id
    
    def to_dict(self):
        return {
            "endereco_id": self.endereco_id,
            "logradouro": self.logradouro,
            "bairro": self.bairro,
            "user_id": self.user_id
        }
    
    def __str__(self):
        return f"{self.endereco_id},{self.logradouro},{self.bairro },{self.user_id}"