import re
from dataclasses import dataclass
from typing import Callable

CHAPTER_NUM_RE = re.compile(r"(\d+(\.\d+)?)")


class ChapterInfo:
    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url

    @property
    def chapter_number(self):
        match = CHAPTER_NUM_RE.search(self.title)
        return match.group(0) if match else None

    @property
    def chapter_number_float(self):
        ch_num = self.chapter_number

        if ch_num:
            try:
                return float(ch_num)
            except ValueError:
                return None
        return None

    def __repr__(self):
        return f"ChapterInfo(title={self.title}, url={self.url})"

    def __str__(self):
        return f"Title: {self.title} --- URL: {self.url}\n"


class XPaths:
    def __init__(
        self,
        title: str,
        image_url: str,
        last_chapter: str,
        chapter_title: str,
        chapter_url: str,
    ):
        self.title = title
        self.image_url = image_url
        self.last_chapter = last_chapter
        self.chapter_title = chapter_title
        self.chapter_url = chapter_url


class SourceResult:
    def __init__(
        self,
        title: str,
        image_url: str,
        last_chapter: float,
        chapters: list[ChapterInfo],
    ):
        self.title = title
        self.image_url = image_url
        self.last_chapter = last_chapter
        self.chapters = chapters

    def __repr__(self):
        return f"SourceResult(name={self.title}, chapters={self.chapters})"

    def __str__(self):
        return f"Title: {self.title} --- Chapter Count: {len(self.chapters)}\n"


@dataclass
class BaseSource:
    identifiers: list[str]
    xpaths: XPaths
    fetch_source_fn: Callable[[str, XPaths], SourceResult]
