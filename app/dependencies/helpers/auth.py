from datetime import UTC, datetime, timedelta

import jwt
from passlib.context import CryptContext
from sqlmodel import Session, SQLModel, create_engine, select

from app.models.db_tables import RoleInDiscord, RoleInWebsite, UserInDB  # noqa

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

ADMIN = ["NandeMD", "$2b$12$xMZc.TBbYffA5YyLdjUIZe82tk1RokF9D4Rbx3dDE6j6XLrR5Gvf."]
BOT = ["DiscordBot", "$2b$12$LIKBcEIJ6fnCf3Yl7PNuuOzGO.GSWf1WQlZbzBe/rH3gW7a.9Rmsm"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

_sqlite_file_name = "database.db"
_sqlite_url = f"sqlite:///{_sqlite_file_name}"
_connect_args = {"check_same_thread": False}

sql_engine = create_engine(_sqlite_url, connect_args=_connect_args)


def get_database_session():
    with Session(sql_engine) as session:
        yield session


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_database():
    SQLModel.metadata.create_all(sql_engine)

    db_session = next(get_database_session())

    admin_query = db_session.exec(select(UserInDB).where(UserInDB.username == ADMIN[0]))
    admin = admin_query.first()
    if not admin:
        admin_user = UserInDB(
            username=ADMIN[0],
            email="msthmmu@gmail.com",
            discord_id="NandeMD",
            role_in_website=RoleInWebsite.SUPER,
            role_in_discord=[RoleInDiscord.ADMIN],
            hashed_password=ADMIN[1],
        )
        db_session.add(admin_user)
        db_session.commit()
        db_session.refresh(admin_user)

    bot_query = db_session.exec(select(UserInDB).where(UserInDB.username == BOT[0]))
    bot = bot_query.first()
    if not bot:
        bot_user = UserInDB(
            username=BOT[0],
            email="bottan@gmail.com",
            discord_id="nobot",
            role_in_website=RoleInWebsite.SUPER,
            role_in_discord=[RoleInDiscord.ADMIN],
            hashed_password=BOT[1],
        )
        db_session.add(bot_user)
        db_session.commit()
        db_session.refresh(bot_user)
    db_session.close()


def get_user(db: Session, username: str | None):
    return db.exec(select(UserInDB).where(UserInDB.username == username)).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(days=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
