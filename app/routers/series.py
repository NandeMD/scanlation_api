from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse
from sqlmodel import or_, select

from ..dependencies.auth import CurrentUserDep, DatabaseDep
from ..models.db_tables import RoleInWebsite, Serie

series_router = APIRouter(prefix="/series", tags=["series"])


@series_router.get("/", response_class=ORJSONResponse)
async def get_series(
    current_user: CurrentUserDep,
    db: DatabaseDep,
    limit: int = 100,
) -> list[Serie]:
    usr_role = current_user.role_in_website

    if usr_role == RoleInWebsite.ADMIN or usr_role == RoleInWebsite.SUPER:
        query = select(Serie).limit(limit)
    else:
        query = select(Serie).where(or_(
            Serie.translator_id == current_user.discord_id, 
            Serie.proofreader_id == current_user.discord_id,
            Serie.cleaner_id == current_user.discord_id,
            Serie.typesetter_id == current_user.discord_id,
            Serie.quality_checker_id == current_user.discord_id,
        )).limit(limit)

    series = db.exec(query)

    return list(series)

@series_router.get("/{serie_id}", response_class=ORJSONResponse)
async def get_serie(
    current_user: CurrentUserDep,
    db: DatabaseDep,
    serie_id: int,
) -> Serie:
    usr_role = current_user.role_in_website

    if usr_role == RoleInWebsite.ADMIN or usr_role == RoleInWebsite.SUPER:
        query = select(Serie).where(Serie.id == serie_id)
    else:
        query = select(Serie).where(
            Serie.id == serie_id,
            or_(
                Serie.translator_id == current_user.discord_id, 
                Serie.proofreader_id == current_user.discord_id,
                Serie.cleaner_id == current_user.discord_id,
                Serie.typesetter_id == current_user.discord_id,
                Serie.quality_checker_id == current_user.discord_id,
            )
        )

    serie = db.exec(query).first()

    if serie is None:
        raise HTTPException(status_code=404, detail="Serie not found")

    return serie