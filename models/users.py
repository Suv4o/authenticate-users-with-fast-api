from sqlalchemy import Column, Integer, String, Boolean
from models.base import TimeStampedModel


class Users(TimeStampedModel):
    __tablename__ = "users"

    uid = Column("id", Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(320), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    disabled = Column(Boolean, default=False)
    refresh_token = Column(String(150), nullable=True)

    def __init__(self, full_name, email, password, disabled=False, refresh_token=None):
        self.full_name = full_name
        self.email = email
        self.password = password
        self.disabled = disabled
        self.refresh_token = refresh_token

    def __repr__(self):
        return f"{self.__class__.__name__}, id: {self.uid}, email: {self.email}"
