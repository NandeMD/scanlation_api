from pydantic import BaseModel


class NewSerieRequest(BaseModel):
    source_url: str
    owned_url: str
    role_id: int
    main_category_id: int

    translator_id: int | None = None
    proofreader_id: int | None = None
    cleaner_id: int | None = None
    typesetter_id: int | None = None
    quality_checker_id: int | None = None
    drive_url: str | None = None


class NewSeriesManualRequest(BaseModel):
    title: str
    image_url: str
    source_url: str
    owned_url: str
    source_last_chapter: int
    owned_last_chapter: int
    role_id: int
    main_category_id: int

    translator_id: int | None = None
    proofreader_id: int | None = None
    cleaner_id: int | None = None
    typesetter_id: int | None = None
    quality_checker_id: int | None = None
    drive_url: str | None = None


class UpdateSerieRequest(BaseModel):
    serie_id: int
    title: str | None = None
    image_url: str | None = None
    source_url: str | None = None
    owned_url: str | None = None
    source_last_chapter: int | None = None
    owned_last_chapter: int | None = None
    role_id: int | None = None
    main_category_id: int | None = None

    translator_id: int | None = None
    proofreader_id: int | None = None
    cleaner_id: int | None = None
    typesetter_id: int | None = None
    quality_checker_id: int | None = None
    drive_url: str | None = None
