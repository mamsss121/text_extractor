# text_extractor

This project processes GROBID TEI XML files and generates:
- a CSV with extracted abstracts
- a keyword list
- a keyword cloud based on the abstracts

## Requirements
- Python 3.11+ recommended
- pip

## Installation

```bash
git clone https://github.com/mamsss121/text_extractor.git
cd text_extractor
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


## Usage

All scripts assume that GROBID TEI XML files are in `data/grobid`
and that the `outputs/` directory exists or can be created.

Extract abstracts and keywords:

```bash
python generate_keyword_cloud.py

Count figures per article: 

```bash
python extract_figures.py

Extract links per article:

```bash
python extract_links.py


```markdown
## Validation

To validate the results, I:

- Manually inspected 2–3 TEI files and checked that the extracted
  abstracts match the `<abstract>` section in the XML.
- Checked that the number of `<figure>` elements per TEI file matches
  the figure count in the original PDF.
- Verified that the links extracted from TEI files correspond to the
  URLs visible in the PDF or in the TEI attributes (e.g. `target`,
  `href`).

I added unit tests in `tests/` to automatically check some of these
cases (e.g. expected number of figures for a known paper).

## Project structure

- `extract_abstracts.py` – extract abstracts into a CSV.
- `make_keywords.py` – compute keyword frequencies.
- `make_wordcloud.py` – generate a word cloud image.
- `extract_figures.py` – count figures per article.
- `extract_links.py` – extract links per article.
- `tests/` – basic unit tests for the scripts.


## Limitations

- The scripts have been tested only on 10 GROBID TEI XML files.
- The URL extraction relies on a simple regex and may miss some edge
  cases or include non-scholarly links.
- The keyword extraction does not do lemmatization or phrase
  detection, so some terms may be duplicated (e.g. "model" vs
  "models").

