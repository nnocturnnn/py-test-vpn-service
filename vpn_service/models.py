from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str
    email: str = None
    full_name: str = None
    phone: str = None

class UpdateUserData(BaseModel):
    email: str = None
    full_name: str = None
    phone: str = None

class Stats(BaseModel):
    site_name: str
    page_visits: int
    data_sent: int
    data_received: int