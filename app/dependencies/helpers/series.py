from sqlmodel import Session

from hoarder.sources import ChapterInfo, SourceResult

from ...models.db_tables import Chapter, Serie


def add_new_serie_chapters(db: Session, serie: Serie, owned_chapters: list[ChapterInfo], source_chapters: list[ChapterInfo]):
    owned_chs = owned_chapters
    src_chs = source_chapters

    own_ch_numbers = set([ch.chapter_number_float for ch in owned_chs])

    for src_ch in src_chs:
        src_ch_num = src_ch.chapter_number_float
        if src_ch_num is not None:
            chapter_in_db = Chapter(
                serie_id=serie.id if serie.id is not None else 0,
                chapter_number=src_ch_num,
                chapter_title=src_ch.title,
                creator_id=0,
                translator_id=serie.translator_id,
                proofreader_id=serie.proofreader_id,
                cleaner_id=serie.cleaner_id,
                typesetter_id=serie.typesetter_id,
                quality_checker_id=serie.quality_checker_id,
                closer_id=0 if src_ch_num in own_ch_numbers else None,
                notification_sent=True,
            )
            db.add(chapter_in_db)
    db.commit()


def add_new_manual_serie_chapters(start: int, end_owned: int, end_src: int, db: Session, serie: Serie):
    for i in range(start, end_src + 1):
        chapter_in_db = Chapter(
            serie_id=serie.id if serie.id is not None else 0,
            chapter_number=i,
            chapter_title=None,
            creator_id=0,
            translator_id=serie.translator_id,
            proofreader_id=serie.proofreader_id,
            cleaner_id=serie.cleaner_id,
            typesetter_id=serie.typesetter_id,
            quality_checker_id=serie.quality_checker_id,
            closer_id=0 if i <= end_owned else None,
            notification_sent=True,
        )
        db.add(chapter_in_db)
    db.commit()