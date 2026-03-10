from scripts.count_figures import main as run_figures
from scripts.extract_links import main as run_links
from scripts.generate_keyword_cloud import main as run_keywords

def main():
    run_figures()
    run_links()
    run_keywords()

if __name__ == "__main__":
    main()
