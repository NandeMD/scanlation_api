from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError
from sqlmodel import or_, select

from hoarder import match_manga_source

from ..dependencies.auth import CurrentUserDep, DatabaseDep
from ..dependencies.helpers.series import (add_new_manual_serie_chapters,
                                           add_new_serie_chapters)
from ..models.db_tables import RoleInWebsite, Serie
from ..models.series import (NewSerieRequest, NewSeriesManualRequest,
                             UpdateSerieRequest)

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
        query = (
            select(Serie)
            .where(
                or_(
                    Serie.translator_id == current_user.discord_id,
                    Serie.proofreader_id == current_user.discord_id,
                    Serie.cleaner_id == current_user.discord_id,
                    Serie.typesetter_id == current_user.discord_id,
                    Serie.quality_checker_id == current_user.discord_id,
                )
            )
            .limit(limit)
        )

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
            ),
        )

    serie = db.exec(query).first()

    if serie is None:
        raise HTTPException(status_code=404, detail="Serie not found")

    return serie


@series_router.post("/new", response_class=ORJSONResponse)
async def new_serie(
    current_user: CurrentUserDep,
    db: DatabaseDep,
    serie: NewSerieRequest,
) -> Serie:
    usr_role = current_user.role_in_website

    if usr_role != RoleInWebsite.ADMIN and usr_role != RoleInWebsite.SUPER:
        raise HTTPException(status_code=403, detail="Forbidden")

    source_source = match_manga_source(serie.source_url)
    if source_source is None:
        raise HTTPException(status_code=400, detail="Invalid source URL")
    owned_source = match_manga_source(serie.owned_url)
    if owned_source is None:
        raise HTTPException(status_code=400, detail="Invalid owned URL")

    source_result = source_source.fetch_source_fn(
        serie.source_url, source_source.xpaths
    )
    owned_result = owned_source.fetch_source_fn(serie.owned_url, owned_source.xpaths)

    new_serie = Serie(
        title=owned_result.title,
        image_url=owned_result.image_url,
        source_url=serie.source_url,
        owned_url=serie.owned_url,
        source_last_chapter=source_result.last_chapter,
        owned_last_chapter=owned_result.last_chapter,
        role_id=serie.role_id,
        main_category_id=serie.main_category_id,
        translator_id=serie.translator_id,
        proofreader_id=serie.proofreader_id,
        cleaner_id=serie.cleaner_id,
        typesetter_id=serie.typesetter_id,
        quality_checker_id=serie.quality_checker_id,
        drive_url=serie.drive_url,
    )
    try:
        db.add(new_serie)
        db.commit()
        db.refresh(new_serie)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Serie already exists!")

    add_new_serie_chapters(db, new_serie, owned_result.chapters, source_result.chapters)

    return new_serie


@series_router.post("/new/manual", response_class=ORJSONResponse)
async def new_manual_serie(
    current_user: CurrentUserDep, db: DatabaseDep, serie: NewSeriesManualRequest
):
    usr_role = current_user.role_in_website

    if usr_role != RoleInWebsite.ADMIN and usr_role != RoleInWebsite.SUPER:
        raise HTTPException(status_code=403, detail="Forbidden")

    new_serie = Serie(
        title=serie.title,
        image_url=serie.image_url,
        source_url=serie.source_url,
        owned_url=serie.owned_url,
        source_last_chapter=serie.source_last_chapter,
        owned_last_chapter=serie.owned_last_chapter,
        role_id=serie.role_id,
        main_category_id=serie.main_category_id,
        translator_id=serie.translator_id,
        proofreader_id=serie.proofreader_id,
        cleaner_id=serie.cleaner_id,
        typesetter_id=serie.typesetter_id,
        quality_checker_id=serie.quality_checker_id,
        drive_url=serie.drive_url,
    )
    try:
        db.add(new_serie)
        db.commit()
        db.refresh(new_serie)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Serie already exists!")

    add_new_manual_serie_chapters(
        1,
        serie.owned_last_chapter,
        serie.source_last_chapter,
        db,
        new_serie,
    )

    return new_serie


@series_router.delete("/delete/{serie_id}", response_class=ORJSONResponse)
async def delete_serie(
    current_user: CurrentUserDep,
    db: DatabaseDep,
    serie_id: int,
) -> dict:
    usr_role = current_user.role_in_website

    if usr_role != RoleInWebsite.ADMIN and usr_role != RoleInWebsite.SUPER:
        raise HTTPException(status_code=403, detail="Forbidden")

    serie = db.get(Serie, serie_id)

    if serie is None:
        raise HTTPException(status_code=404, detail="Serie not found")

    db.delete(serie)
    db.commit()

    return {"detail": "Serie deleted"}


@series_router.put("/update", response_class=ORJSONResponse)
async def update_serie(
    current_user: CurrentUserDep,
    db: DatabaseDep,
    serie: UpdateSerieRequest,
) -> Serie:
    usr_role = current_user.role_in_website

    if usr_role != RoleInWebsite.ADMIN and usr_role != RoleInWebsite.SUPER:
        raise HTTPException(status_code=403, detail="Forbidden")

    db_serie = db.get(Serie, serie.id)

    if db_serie is None:
        raise HTTPException(status_code=404, detail="Serie not found")

    for key, value in serie.model_dump(exclude_unset=True).items():
        setattr(db_serie, key, value)

    try:
        db.add(db_serie)
        db.commit()
        db.refresh(db_serie)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Serie already exists!")

    return db_serie
