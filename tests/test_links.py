import os
import sys
from pathlib import Path

# Add project root to sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from scripts.extract_links import extract_links_from_file  # type: ignore

DATA_DIR = ROOT / "data" / "grobid"


def test_links_function_runs_on_first_file():
    xml_files = [f for f in DATA_DIR.iterdir() if f.name.endswith(".tei.xml")]
    assert xml_files

    filepath = xml_files[0]
    links = extract_links_from_file(str(filepath))

    assert isinstance(links, list)
    for url in links:
        assert isinstance(url, str)


def test_extracted_links_look_like_urls():
    xml_files = [f for f in DATA_DIR.iterdir() if f.name.endswith(".tei.xml")]
    assert xml_files

    filepath = xml_files[0]
    links = extract_links_from_file(str(filepath))

    if links:
        for url in links:
            assert url.startswith(("http://", "https://"))

def test_links_known_paper_2506_contains_arxiv():
    filename = "2506.08872v2.pdf.tei.xml"
    filepath = DATA_DIR / filename
    assert filepath.is_file()

    links = extract_links_from_file(str(filepath))

    assert links  # at least one link
    assert any("arxiv.org" in url for url in links)


def test_links_known_paper_2503_unique_and_http():
    filename = "2503.10225v2.pdf.tei.xml"
    filepath = DATA_DIR / filename
    assert filepath.is_file()

    links = extract_links_from_file(str(filepath))

    # unique
    assert len(links) == len(set(links))

    # all http(s)
    for url in links:
        assert url.startswith(("http://", "https://"))