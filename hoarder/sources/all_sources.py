from typing import Type

from . import BaseSource, XPaths
from .funcs import asura_source, default


class MerlinScans(BaseSource):
    identifiers = ["merlinscans.com"]
    xpaths = XPaths(
        title="//div[@class='seriestuhead']/h1[@class='entry-title']/text()",
        image_url="//div[@class='seriestucont']/div[@class='seriestucontl']/div[@class='thumb']/img/@src",
        last_chapter="//span[@class='epcur epcurlast']/text()",
        chapter_title="//div[@class='eplister']/ul/li/div/div/a/span[@class='chapternum']/text()",
        chapter_url="//div[@class='eplister']/ul/li/div/div/a/@href",
    )
    fetch_source_fn = default


class AsuraComics(BaseSource):
    identifiers = ["asuracomic.net"]
    xpaths = XPaths(
        title="//title/text()",
        image_url="//img[@class='rounded mx-auto md:mx-0']/@src",
        last_chapter="",
        chapter_title="//h3[@class='text-sm text-white font-medium flex flex-row' and not(span/svg)]//text()",
        chapter_url="//h3[@class='text-sm text-white font-medium flex flex-row' and not(span/svg)]/parent::a/@href",
    )
    fetch_source_fn = asura_source


ALL_SOURCES: list[Type[BaseSource]] = [MerlinScans, AsuraComics]
