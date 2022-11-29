from pydantic import BaseModel

class AuthDetails(BaseModel):
    username: str
    password: str

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "password": self.password
        }