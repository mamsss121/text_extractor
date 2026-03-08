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

