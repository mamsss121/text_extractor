import sys
from pathlib import Path
import unittest

# Add project root to sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from scripts.extract_links import extract_links_from_file  # type: ignore

DATA_DIR = ROOT / "data" / "grobid"


class TestLinks(unittest.TestCase):
    def test_links_function_runs_on_first_file(self):
        """extract_links_from_file runs and returns list of strings."""
        xml_files = [f for f in DATA_DIR.iterdir() if f.name.endswith(".tei.xml")]
        self.assertGreater(len(xml_files), 0)

        filepath = xml_files[0]
        links = extract_links_from_file(str(filepath))

        self.assertIsInstance(links, list)
        for url in links:
            self.assertIsInstance(url, str)

    def test_extracted_links_look_like_urls(self):
        """Links from first file start with http:// or https://."""
        xml_files = [f for f in DATA_DIR.iterdir() if f.name.endswith(".tei.xml")]
        self.assertGreater(len(xml_files), 0)

        filepath = xml_files[0]
        links = extract_links_from_file(str(filepath))

        if links:
            for url in links:
                self.assertTrue(
                    url.startswith(("http://", "https://")),
                    msg=f"Invalid URL: {url}",
                )

    def test_links_known_paper_2506_contains_arxiv(self):
        """Known paper 2506… contains at least one arxiv.org link."""
        filename = "2506.08872v2.pdf.tei.xml"
        filepath = DATA_DIR / filename
        self.assertTrue(filepath.is_file())

        links = extract_links_from_file(str(filepath))

        self.assertGreater(len(links), 0)
        self.assertTrue(any("arxiv.org" in url for url in links))

    def test_links_known_paper_2503_unique_and_http(self):
        """Known paper 2503… links are unique and all http(s)."""
        filename = "2503.10225v2.pdf.tei.xml"
        filepath = DATA_DIR / filename
        self.assertTrue(filepath.is_file())

        links = extract_links_from_file(str(filepath))

        self.assertEqual(len(links), len(set(links)))
        for url in links:
            self.assertTrue(url.startswith(("http://", "https://")))


if __name__ == "__main__":
    unittest.main()
