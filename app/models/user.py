from enum import Enum

from sqlmodel import Column, Field, PickleType, SQLModel


class RoleInWebsite(str, Enum):
    NORMAL = "normal"
    ADMIN = "admin"
    SUPER = "super"
    
class RoleInDiscord(str, Enum):
    TRANSLATOR = "translator"
    PROOFREADER = "proofreader"
    TYPESETTER = "typesetter"
    QUALITY_CHECKER = "qualitychecker"
    ADMIN = "admin"
    SIDE_ADMIN = "sideadmin"

class User(SQLModel):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    discord_id: str = Field(index=True, unique=True)
    role_in_website: RoleInWebsite = Field(default=RoleInWebsite.NORMAL)
    role_in_discord: list[RoleInDiscord] = Field(sa_column=Column(PickleType))
    is_active: bool = Field(default=True)
    
class UserInDB(User, table=True):
    __tablename__: str = "users" # type: ignore
    
    hashed_password: str
    
    