from pydantic import BaseModel

class User(BaseModel):
    username: str
    hashed_password: str

    def get_user_data(self):
        return {
            "username": self.username,
            "hashed_password": self.hashed_password
        }