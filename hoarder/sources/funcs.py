import re

from cloudscraper import create_scraper
from lxml import html

from . import ChapterInfo, SourceResult, XPaths

html_parser = html.HTMLParser(collect_ids=False)
CHAPTER_NUM_RE = re.compile(r"(\d+(\.\d+)?)")


def __fetch_url(url) -> str:
    scraper = create_scraper()
    with scraper.get(url) as response:
        site = response.text

    del scraper
    del response

    return site


def default(url: str, xpaths: XPaths) -> SourceResult:
    """
    Default function to fetch the source.
    :param url: URL to fetch the source from.
    :param xpaths: XPaths object containing the xpaths to be used.
    :return: SourceResult object containing the name and chapters.
    """
    site = __fetch_url(url)
    tree = html.fromstring(site, parser=html_parser)

    title = tree.xpath(xpaths.title)[0]
    image_url = tree.xpath(xpaths.image_url)
    image_url = image_url[0] if len(image_url) > 0 else "None"
    last_chapter = tree.xpath(xpaths.last_chapter)
    last_chapter = last_chapter[0] if len(last_chapter) > 0 else "inf"
    try:
        last_chapter = float(last_chapter)
    except ValueError:
        match = CHAPTER_NUM_RE.search(last_chapter)
        if match:
            last_chapter = float(match.group(0))
        else:
            last_chapter = 0.0

    chapters = [
        ChapterInfo(
            title=chapter_title,
            url=chapter_url,
        )
        for chapter_title, chapter_url in zip(
            tree.xpath(xpaths.chapter_title),
            tree.xpath(xpaths.chapter_url),
        )
    ]

    return SourceResult(
        title=title,
        image_url=image_url,
        last_chapter=last_chapter,
        chapters=chapters,
    )


def asura_source(url: str, xpaths: XPaths) -> SourceResult:
    site = __fetch_url(url)
    tree = html.fromstring(site, parser=html_parser)

    title = tree.xpath(xpaths.title)[0]
    image_url = tree.xpath(xpaths.image_url)
    image_url = image_url[0] if len(image_url) > 0 else "None"
    chapters_separated = tree.xpath(xpaths.chapter_title)
    chapter_titles = [
        " ".join(chapters_separated[i : i + 2])
        for i in range(0, len(chapters_separated), 2)
    ]
    chapter_urls = [
        f"https://asuracomic.net/series/{uri}" for uri in tree.xpath(xpaths.chapter_url)
    ]
    chapters = [
        ChapterInfo(
            title=chapter_title,
            url=chapter_url,
        )
        for chapter_title, chapter_url in zip(
            chapter_titles,
            chapter_urls,
        )
    ]
    if chapters:
        last_chapter = chapters[0].chapter_number_float
        if last_chapter is None:
            last_chapter = 0.0
    else:
        last_chapter = 0.0

    return SourceResult(
        title=title,
        image_url=image_url,
        last_chapter=last_chapter,
        chapters=chapters,
    )
