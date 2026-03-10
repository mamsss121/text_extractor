import csv
import os
import xml.etree.ElementTree as ET
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

INPUT_DIR = "data/grobid"
OUTPUT_FILE = "outputs/abstracts.csv"
OUTPUT_KEYWORDS = "outputs/keywords.txt"

ns = {"tei": "http://www.tei-c.org/ns/1.0"}

STOPWORDS = set([
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
    'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these',
    'those', 'it', 'its', 'which', 'who', 'when', 'where', 'why', 'how',
    'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other',
    'some', 'such', 'than', 'too', 'very', 'we', 'us', 'our', 'their',
    'them', 'they', 'his', 'her'
])


def main():
    rows = []
    all_abstracts_text = []

    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".xml"):
            file_path = os.path.join(INPUT_DIR, filename)
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()

                abstract_texts = []
                for abstract in root.findall(".//tei:abstract", ns):
                    for elem in abstract.iter():
                        if elem.text:
                            abstract_texts.append(elem.text.strip())

                abstract_text = " ".join(t for t in abstract_texts if t)
                all_abstracts_text.append(abstract_text)
                rows.append([filename, abstract_text])

            except Exception as e:
                rows.append([filename, f"ERROR: {e}"])

    combined_text = " ".join(all_abstracts_text).lower()
    combined_text = re.sub(r'[^a-z\s]', ' ', combined_text)

    words = combined_text.split()
    filtered_words = [
        word for word in words
        if word and len(word) > 2 and word not in STOPWORDS
    ]

    word_freq = Counter(filtered_words)

    os.makedirs("outputs", exist_ok=True)

    with open(OUTPUT_KEYWORDS, "w", encoding="utf-8") as f:
        f.write(" ".join(filtered_words))

    with open("outputs/top_keywords.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["keyword", "frequency"])
        writer.writerows(word_freq.most_common(100))

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "abstract"])
        writer.writerows(rows)

    wordcloud = WordCloud(width=800, height=400,
                          background_color='white').generate(
        " ".join(filtered_words)
    )

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title("Keyword Cloud")
    plt.tight_layout()
    plt.savefig("outputs/keyword_cloud.png", dpi=300)
    plt.close()

    print(f"Saved {len(rows)} abstracts to {OUTPUT_FILE}")
    print(f"Saved processed keywords to {OUTPUT_KEYWORDS}")
    print(f"Top 5 keywords: {word_freq.most_common(5)}")


if __name__ == "__main__":
    main()
