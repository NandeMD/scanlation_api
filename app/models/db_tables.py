from datetime import datetime
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
    id: int = Field(default=None, primary_key=True, unique=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    discord_id: str = Field(index=True, unique=True)
    role_in_website: RoleInWebsite = Field(default=RoleInWebsite.NORMAL)
    role_in_discord: list[RoleInDiscord] = Field(sa_column=Column(PickleType))
    is_active: bool = Field(default=True)
    
    
class UserInDB(User, table=True):
    __tablename__: str = "users" # type: ignore
    hashed_password: str
    

class Serie(SQLModel, table=True):
    __tablename__: str = "series" # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True, unique=True)
    image_url: str
    source_url: str = Field(unique=True)
    owned_url: str = Field(unique=True)
    source_last_chapter: float
    owned_last_chapter: float
    role_id: int = Field(unique=True)
    main_category_id: int
    translator_id: int | None = Field(default=None, foreign_key="users.id")
    proofreader_id: int | None = Field(default=None, foreign_key="users.id")
    cleaner_id: int | None = Field(default=None, foreign_key="users.id")
    typesetter_id: int | None = Field(default=None, foreign_key="users.id")
    quality_checker_id: int | None = Field(default=None, foreign_key="users.id")
    drive_url: str | None = Field(default=None)


class Chapter(SQLModel, table=True):
    __tablename__: str = "chapters" # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    serie_id: int = Field(foreign_key="series.id")
    chapter_number: float
    chapter_title: str | None = Field(default=None)
    creator_id: int = Field(foreign_key="users.id")
    
    translator_id: int | None = Field(default=None, foreign_key="users.id")
    translator_name: str | None = Field(default=None)
    translated_at: datetime | None = Field(default=None)
    should_proofread: bool = Field(default=False)

    proofreader_id: int | None = Field(default=None, foreign_key="users.id")
    proofreader_name: str | None = Field(default=None)
    proofreaded_at: datetime | None = Field(default=None)
    
    should_clean: bool = Field(default=False)

    cleaner_id: int | None = Field(default=None, foreign_key="users.id")
    cleaner_name: str | None = Field(default=None)
    cleaned_at: datetime | None = Field(default=None)
    
    typesetter_id: int | None = Field(default=None, foreign_key="users.id")
    typesetter_name: str | None = Field(default=None)
    typesetted_at: datetime | None = Field(default=None)

    should_quality_check: bool = Field(default=False)

    quality_checker_id: int | None = Field(default=None, foreign_key="users.id")
    quality_checker_name: str | None = Field(default=None)
    quality_checked_at: datetime | None = Field(default=None)

    closer_id: int | None = Field(default=None, foreign_key="users.id")

    notification_sent: bool = Field(default=False)
