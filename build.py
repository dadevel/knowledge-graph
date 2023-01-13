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
    def __init__(self, note: Note, notes: dict[str, Note], **kwargs) -> None:
        self.note = note
        self.notes = notes
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
        note = self.md.notes.get(path, None)

        if match.group(2):
            # use custom link title
            title = match.group(2).strip()
        elif note:
            # use default note title
            title = note.title.strip()
        else:
            # broken link
            title = path.replace('-', ' ').title().strip()

        if note and not note.draft:
            e = Element('a')
            e.text = title
            e.set('href', f'/{path}.html')
            e.set('class', 'wikilink')
        elif note and note.draft:
            e = Element('span')
            e.text = title
            e.set('class', 'wikilink broken')
        else:
            if not self.md.note.draft:
                print(f'warning: {self.md.note.path}: broken wikilink: {match.group()}', file=sys.stderr)
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
class Note:
    path: Path  # full path to source markdown file
    identifier: str  # relative path without file extension
    title: str  # tile from frontmatter
    template: str
    content: str  # markdown content
    modified_at: datetime  # last git commit
    authors: list[str]  # git authors
    draft: bool = True  # draft if not committed to git
    links: dict[str, Note] = dataclasses.field(default_factory=dict)  # outgoing wikilinks
    backlinks: dict[str, Note] = dataclasses.field(default_factory=dict)  # incoming wikilinks
    neighbors: dict[str, Note] = dataclasses.field(default_factory=dict)  # notes in same directory

    @classmethod
    def from_file(cls, path: Path) -> Note:
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


def preprocess_note(all_notes: dict[str, Note], public_notes: dict[str, Note], note: Note) -> None:
    file = MarkdownFile(
        note,
        all_notes,
        extensions=[
            'meta',
            'tables',
            WikiLinkExtension(),
            ImageCaptionExtension(),
            SuperFencesCodeExtension(disable_indented_code_blocks=True),
            HighlightExtension(guess_lang=False, noclasses=True),
            TabbedExtension(alternate_style=False),
        ],
        output_format='html',
    )
    note.content = file.convert(note.path.read_text())
    note.links = {identifier: public_notes[identifier] for identifier in file.links if identifier in public_notes}


def render_note(environment: Environment, opts: Namespace, public_notes: dict[str, Note], note: Note) -> None:
    template = note.template if note.template else 'note'
    final_html = environment.get_template(f'{template}.html').render(note=note, options=opts, notes=public_notes)
    output_file = OUTPUT_DIR/note.path.relative_to(GRAPH_DIR).with_suffix('.html')
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_bytes(final_html.encode('utf-8', errors='xmlcharrefreplace'))


def build_search_index(public_notes: dict[str, Note]) -> None:
    data = {identifier: dict(title=note.title, content=note.plaintext, url=f'/{identifier}.html', modified_at=note.modified_at.strftime('%d %b %Y')) for identifier, note in public_notes.items()}
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
    all_notes = {}
    for note in pool.map(Note.from_file, NODES):
        all_notes[note.identifier] = note
    public_notes = all_notes if opts.dev else {identifier: note for identifier, note in all_notes.items() if not note.draft}

    print(f'preprocessing', file=sys.stderr)
    for _ in pool.map(functools.partial(preprocess_note, all_notes, public_notes), public_notes.values()):
        continue

    print(f'backlinking', file=sys.stderr)
    for current_indentifier, current_note in public_notes.items():
        current_note.backlinks = {
            other_indentifier: other_note
            for other_indentifier, other_note in public_notes.items()
            if current_indentifier in other_note.links
        }
        parent_identifier = current_note.path.parent.relative_to(GRAPH_DIR).as_posix().lower()
        current_note.neighbors = {
            other_identifier: other_note
            for other_identifier, other_note in public_notes.items()
            if other_note.identifier != current_indentifier
            and other_note.path.parent.relative_to(GRAPH_DIR).as_posix().lower() == parent_identifier
            and other_identifier not in current_note.links
            and other_identifier not in current_note.backlinks
        }

    print(f'rendering notes', file=sys.stderr)
    environment = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=False)
    for _ in pool.map(functools.partial(render_note, environment, opts, public_notes), public_notes.values()):
        continue

    print('building search index', file=sys.stderr)
    build_search_index(public_notes)

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
