#!/usr/bin/env python3
from __future__ import annotations
from argparse import ArgumentParser, BooleanOptionalAction, Namespace
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from re import Match
from xml.etree.ElementTree import Element, SubElement
import dataclasses
import functools
import json
import os
import shutil
import subprocess
import sys

from jinja2 import Environment, FileSystemLoader
from markdown.core import Markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor, ImageInlineProcessor, IMAGE_LINK_RE
from pymdownx.highlight import HighlightExtension
from pymdownx.superfences import SuperFencesCodeExtension
from pymdownx.tabbed import TabbedExtension
import yaml

TEMPLATE_DIR = Path('./templates')
OUTPUT_DIR = Path('./public')
GRAPH_DIR = Path('./graph')
NODES = (p for p in GRAPH_DIR.glob('**/*.md') if p.is_file() and not p.parent.name.startswith('.'))
ATTACHMENTS = (p for p in GRAPH_DIR.glob('**/*') if p.is_file() and not p.parent.name.startswith('.') and not p.name.endswith('.md'))
COMITTED_FILES = {Path(path.rstrip()) for path in subprocess.check_output(['git', 'ls-files'], text=True).splitlines()}
WIKILINK_REGEX = r'\[\[([a-zA-Z0-9-/#]+)(?:\|(.+?))?\]\]'


class MarkdownFile(Markdown):
    def __init__(self, page: Page, pages: dict[str, Page], **kwargs) -> None:
        self.page = page
        self.pages = pages
        self.links = set()
        super().__init__(**kwargs)


class WikiLinkExtension(Extension):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def extendMarkdown(self, md: MarkdownFile) -> None:
        self.md = md
        pattern = WikiLinksInlineProcessor()
        pattern.md = md
        md.inlinePatterns.register(pattern, 'wikilink', 75)


class WikiLinksInlineProcessor(InlineProcessor):
    def __init__(self) -> None:
        super().__init__(WIKILINK_REGEX)
        self.md: MarkdownFile

    def handleMatch(self, match: Match, input: str) -> tuple[Element|str, int, int]:
        path = match.group(1)
        if not path:
            return '', match.start(0), match.end(0)

        self.md.links.add(path)
        page = self.md.pages.get(path, None)

        if match.group(2):
            # use custom link title
            title = match.group(2).strip()
        elif page:
            # use default page title
            title = page.title.strip()
        else:
            # broken link
            title = path.replace('-', ' ').title().strip()

        if page and not page.draft:
            e = Element('a')
            e.text = title
            e.set('href', f'/{path}.html')
            e.set('class', 'wikilink')
        elif page and page.draft:
            e = Element('span')
            e.text = title
            e.set('class', 'wikilink broken')
        else:
            if not self.md.page.draft:
                print(f'warning: {self.md.page.path}: broken wikilink: {match.group()}', file=sys.stderr)
            e = Element('a')
            e.text = title
            e.set('href', f'/{path}.html')
            e.set('class', 'wikilink broken')

        return e, match.start(0), match.end(0)


# based on https://github.com/Evidlo/markdown_captions/blob/fe7dcb63050930ad25b786fe1ae2524400f5de56/markdown_captions/markdown_captions.py
class ImageCaptionInlineProcessor(ImageInlineProcessor):
    def __init__(self, pattern: str) -> None:
        super().__init__(pattern)
        self.md: MarkdownFile

    def handleMatch(self, match: Match, input: str) -> tuple[Element|str|None, int|None, int|None]:
        text, index, handled = self.getText(input, match.end(0))
        if not handled:
            return None, None, None

        src, title, index, handled = self.getLink(input, index)
        if not handled:
            return None, None, None

        fig = Element('figure')
        img = SubElement(fig, 'img')
        cap = SubElement(fig, 'figcaption')

        img.set('src', src)
        if title is not None:
            img.set('title', title)
        cap.text = text

        return fig, match.start(0), index


class ImageCaptionExtension(Extension):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def extendMarkdown(self, md: MarkdownFile) -> None:
        self.md = md
        pattern = ImageCaptionInlineProcessor(IMAGE_LINK_RE)
        pattern.md = md
        md.inlinePatterns.register(pattern, 'imagecaption', 151)


@dataclasses.dataclass
class Page:
    path: Path  # full path to source markdown file
    identifier: str  # relative path without file extension
    title: str  # tile from frontmatter
    template: str
    content: str  # markdown content
    modified_at: datetime  # last git commit
    authors: list[str]  # git authors
    draft: bool = True  # draft if not committed to git
    links: dict[str, Page] = dataclasses.field(default_factory=dict)  # outgoing wikilinks
    backlinks: dict[str, Page] = dataclasses.field(default_factory=dict)  # incoming wikilinks
    neighbors: dict[str, Page] = dataclasses.field(default_factory=dict)  # pages in same directory

    @classmethod
    def from_file(cls, path: Path) -> Page:
        with open(path) as file:
            try:
                frontmatter = next(yaml.safe_load_all(file))
            except Exception:
                frontmatter = None

        identifier = path.relative_to(GRAPH_DIR).as_posix().lower().removesuffix('.md')

        draft = path not in COMITTED_FILES

        if isinstance(frontmatter, dict):
            title = frontmatter.get('title', '')
            template = frontmatter.get('template', '')
            if not title and not draft:
                print(f'warning: {path}: title missing')
        else:
            #if not identifier.startswith('private/'):
            #    print(f'warning: {path}: frontmatter missing')
            title, template = '', ''

        process = subprocess.run(['git', 'log', '-1', '--pretty=format:%cI', '--', path], capture_output=True, text=True)
        if process.returncode == 0 and process.stdout:
            modified_at = datetime.fromisoformat(process.stdout)
        else:
            modified_at = datetime.utcnow().replace(tzinfo=timezone.utc)

        process = subprocess.run(['git', 'log', '--format=%an', '--', path], capture_output=True, text=True)
        if process.returncode == 0 and process.stdout:
            authors = list(sorted(set(process.stdout.splitlines())))
        else:
            authors = []

        return cls(path=path, identifier=identifier, title=title, template=template, modified_at=modified_at, authors=authors, draft=draft, content='')

    @property
    def plaintext(self) -> str:
        return HTMLFilter.to_text(self.content)


class HTMLFilter(HTMLParser):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.text = ''

    def handle_data(self, data: str) -> None:
        self.text += data

    @classmethod
    def to_text(cls, html: str) -> str:
        f = cls()
        f.feed(html)
        return f.text.strip()


def preprocess_page(all_pages: dict[str, Page], public_pages: dict[str, Page], page: Page) -> None:
    file = MarkdownFile(
        page,
        all_pages,
        extensions=[
            'meta',
            'tables',
            WikiLinkExtension(),
            ImageCaptionExtension(),
            SuperFencesCodeExtension(disable_indented_code_blocks=True),
            HighlightExtension(guess_lang=False, noclasses=False),
            TabbedExtension(alternate_style=False),
        ],
        output_format='html',
    )
    page.content = file.convert(page.path.read_text())
    page.links = {identifier: public_pages[identifier] for identifier in file.links if identifier in public_pages}


def render_page(environment: Environment, opts: Namespace, public_pages: dict[str, Page], page: Page) -> None:
    if page.template:
        template = page.template
    elif page.identifier.startswith('posts/'):
        template = 'post'
    elif page.identifier.startswith('notes/'):
        template = 'note'
    else:
        raise RuntimeError('failed to determine page template')
    public_notes = list(sorted((other for other in public_pages.values() if page.identifier != other.identifier and other.identifier != 'notes/index' and other.identifier.startswith('notes/')), key=lambda p: (-p.modified_at.timestamp(), p.title)))
    public_posts = list(sorted((other for other in public_pages.values() if page.identifier != other.identifier and other.identifier != 'posts/index' and other.identifier.startswith('posts/')), key=lambda p: (-p.modified_at.timestamp(), p.title)))
    final_html = environment.get_template(f'{template}.html').render(page=page, options=opts, pages=public_pages, notes=public_notes, posts=public_posts)
    output_file = OUTPUT_DIR/page.path.relative_to(GRAPH_DIR).with_suffix('.html')
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_bytes(final_html.encode('utf-8', errors='xmlcharrefreplace'))


def build_search_index(public_pages: dict[str, Page]) -> None:
    data = {identifier: dict(title=page.title, content=page.plaintext, url=f'/{identifier}.html', modified_at=page.modified_at.strftime('%d.%m.%Y')) for identifier, page in public_pages.items()}
    index_file = OUTPUT_DIR/'index.json'
    with open(index_file, 'w') as file:
        json.dump(data, file)


def copy_attachment(input_file: Path) -> None:
    comitted = input_file in COMITTED_FILES
    if not comitted:
        return
    output_file = OUTPUT_DIR/input_file.relative_to(GRAPH_DIR)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_bytes(input_file.read_bytes())


def do_work(opts: Namespace, pool: ThreadPoolExecutor) -> None:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()

    print(f'parsing', file=sys.stderr)
    all_pages = {}
    for page in pool.map(Page.from_file, NODES):
        all_pages[page.identifier] = page
    public_pages = all_pages if opts.dev else {identifier: page for identifier, page in all_pages.items() if not page.draft}

    print(f'preprocessing', file=sys.stderr)
    for _ in pool.map(functools.partial(preprocess_page, all_pages, public_pages), public_pages.values()):
        continue

    print(f'backlinking', file=sys.stderr)
    for current_indentifier, current_page in public_pages.items():
        current_page.backlinks = {
            other_indentifier: other_page
            for other_indentifier, other_page in public_pages.items()
            if current_indentifier in other_page.links
        }
        parent_identifier = current_page.path.parent.relative_to(GRAPH_DIR).as_posix().lower()
        current_page.neighbors = {
            other_identifier: other_page
            for other_identifier, other_page in public_pages.items()
            if other_page.identifier != current_indentifier
            and other_page.path.parent.relative_to(GRAPH_DIR).as_posix().lower() == parent_identifier
            and other_identifier not in current_page.links
            and other_identifier not in current_page.backlinks
        }

    print(f'rendering pages', file=sys.stderr)
    environment = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=False)
    for _ in pool.map(functools.partial(render_page, environment, opts, public_pages), public_pages.values()):
        continue

    print('building search index', file=sys.stderr)
    build_search_index(public_pages)

    print(f'copying attachments', file=sys.stderr)
    for _ in pool.map(copy_attachment, ATTACHMENTS):
        continue

    print(f'copying static files', file=sys.stderr)
    shutil.copytree('./static', OUTPUT_DIR/'static')


def main() -> None:
    entrypoint = ArgumentParser()
    entrypoint.add_argument('-d', '--dev', action=BooleanOptionalAction)
    opts = entrypoint.parse_args()
    cores = os.cpu_count() or 1
    with ThreadPoolExecutor(max_workers=max(64, cores * 4)) as pool:
        do_work(opts, pool)


if __name__ == '__main__':
    main()
