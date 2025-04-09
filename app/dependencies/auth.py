from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session

from ..helpers.auth import ALGORITHM, SECRET_KEY, get_database_session, get_user
from ..models.auth import TokenData
from ..models.user import UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

DatabaseDep = Annotated[Session, Depends(get_database_session)]


async def _get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: DatabaseDep
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


CurrentUserDep = Annotated[UserInDB, Depends(_get_current_user)]
