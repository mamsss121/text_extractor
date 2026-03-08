import os
import sys
from pathlib import Path

# Add project root to sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from scripts.count_figures import count_figures_in_file

DATA_DIR = ROOT / "data" / "grobid"


def test_tei_files_exist():
    assert DATA_DIR.is_dir()
    xml_files = [f for f in DATA_DIR.iterdir() if f.name.endswith(".tei.xml")]
    assert len(xml_files) > 0


def test_figure_counts_are_non_negative():
    xml_files = [f for f in DATA_DIR.iterdir() if f.name.endswith(".tei.xml")]
    filepath = xml_files[0]

    n_figs =  count_figures_in_file(str(filepath))

    assert isinstance(n_figs, int)
    assert n_figs >= 0


def test_figures_known_paper_2506():
    filename = "2506.08872v2.pdf.tei.xml"
    expected_figures = 177  

    filepath = DATA_DIR / filename
    assert filepath.is_file()

    n_figs = count_figures_in_file(str(filepath))
    assert n_figs == expected_figures


def test_figures_known_paper_2503():
    filename = "2503.10225v2.pdf.tei.xml"
    expected_figures = 15 

    filepath = DATA_DIR / filename
    assert filepath.is_file()

    n_figs = count_figures_in_file(str(filepath))
    assert n_figs == expected_figures