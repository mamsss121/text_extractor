import sys
from pathlib import Path
import unittest

# Add project root to sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from scripts.count_figures import count_figures_in_file  # type: ignore

DATA_DIR = ROOT / "data" / "grobid"


class TestFigures(unittest.TestCase):
    def test_tei_files_exist(self):
        """Data directory should contain at least one .tei.xml file."""
        self.assertTrue(DATA_DIR.is_dir())
        xml_files = [f for f in DATA_DIR.iterdir() if f.name.endswith(".tei.xml")]
        self.assertGreater(len(xml_files), 0)

    def test_figure_counts_are_non_negative(self):
        """count_figures_in_file returns a non‑negative int for first file."""
        xml_files = [f for f in DATA_DIR.iterdir() if f.name.endswith(".tei.xml")]
        filepath = xml_files[0]

        n_figs = count_figures_in_file(str(filepath))

        self.assertIsInstance(n_figs, int)
        self.assertGreaterEqual(n_figs, 0)

    def test_figures_known_paper_2506(self):
        """Known paper 2506… has expected number of figures."""
        filename = "2506.08872v2.pdf.tei.xml"
        expected_figures = 177  # keep your checked value

        filepath = DATA_DIR / filename
        self.assertTrue(filepath.is_file())

        n_figs = count_figures_in_file(str(filepath))
        self.assertEqual(n_figs, expected_figures)

    def test_figures_known_paper_2503(self):
        """Known paper 2503… has expected number of figures."""
        filename = "2503.10225v2.pdf.tei.xml"
        expected_figures = 15  # keep your checked value

        filepath = DATA_DIR / filename
        self.assertTrue(filepath.is_file())

        n_figs = count_figures_in_file(str(filepath))
        self.assertEqual(n_figs, expected_figures)


if __name__ == "__main__":
    unittest.main()
