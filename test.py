from cloudscraper import create_scraper
from lxml import html

URL = "https://asuracomic.net/series/the-extras-academy-survival-guide-118c145c"
XP = "//img[@class='rounded mx-auto md:mx-0']/@src"

scraper = create_scraper()

response = scraper.get(URL)
site = response.text
tree = html.fromstring(site)
image_url = tree.xpath(XP)

print(image_url)
