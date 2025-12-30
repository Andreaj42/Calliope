from html import unescape
from urllib.parse import parse_qs, unquote, urlparse

from bs4 import BeautifulSoup


def parse_mail(html: str):
    soup = BeautifulSoup(html, "html.parser")
    items = []

    for a in soup.select("a.gse_alrt_title[href]"):
        title = a.get_text(" ", strip=True)
        href = unescape(a["href"])
        qs = parse_qs(urlparse(href).query)
        container = a.find_parent(["h3", "div"])
        sni = container.find_next("div", class_="gse_alrt_sni")
        abstract = sni.get_text(" ", strip=True)
        items.append(
            {
                "title": title,
                 "url": unquote(qs["url"][0]),
                 "abstract": abstract,
            }
        )
    return items
