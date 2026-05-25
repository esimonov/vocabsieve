import ebooklib
from typing import Dict, Optional
from ebooklib import epub
from charset_normalizer import from_bytes
from lxml import etree
from markdownify import markdownify
from markdown import markdown
import os


def remove_ns(s: str) -> str:
    return str(s).split("}")[-1]


def fix_hyphen(s: str) -> str:
    """This replaces first hyphen in a paragraph
    (which should not be there) with an en dash.
    """
    return s.replace('>-', '>–')


def tostr(s):
    return str(
        from_bytes(
            etree.tostring(
                s,
                encoding='utf8',
                method='text')).best()).strip()


def tohtml(s):
    return str(
        from_bytes(
            etree.tostring(
                s,
                encoding='utf8')).best()).strip()

def parseFb2(path: str) -> dict:
    with open(path, 'rb') as f:
        data = f.read()
        tree = etree.fromstring(data)
    chapters = []
    already_seen = False
    authors = []
    title = ""
    for el in tree:
        tag_nons = remove_ns(el.tag)
        if tag_nons == "description":
            for item in el:
                if remove_ns(item.tag) == "title-info":
                    for subitem in item:
                        if remove_ns(subitem.tag) == "author":
                            authors.append(" ".join(tostr(subitem).split()))
                        if remove_ns(subitem.tag) == "book-title":
                            title = tostr(subitem)
        if tag_nons == "body" and not already_seen:
            already_seen = True
            for section in el:
                current_chapter = ""
                for item in section:
                    if remove_ns(item.tag) == "title":
                        current_chapter = "## " + tostr(item) + "\n\n"
                    else:
                        current_chapter += markdownify(fix_hyphen(tohtml(item)))
                chapters.append(current_chapter)
    return {
        "author": ", ".join(authors),
        "title": title,
        "chapters": [markdown(chapter) for chapter in chapters]
    }

def getEpubMetadata(path: str) -> Dict[str, str]:
    book = epub.read_epub(path)
    title = book.get_metadata('DC', 'title') or ["no title", "no title"]
    author = book.get_metadata('DC', 'creator') or ["no author", "no author"]
    return {
        "title": title[0][0],
        "author": author[0][0]
    }


ALLOWED_EXTENSIONS = {'epub', 'fb2'}


def allowed_file(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
