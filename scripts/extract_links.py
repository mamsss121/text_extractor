import os
import csv
import re
import xml.etree.ElementTree as ET

INPUT_DIR = "data/grobid"
OUTPUT_CSV = "outputs/links_per_article.csv"
URL_PATTERN = re.compile(r"https?://[^\s\"<>()]+")

ns = {"tei": "http://www.tei-c.org/ns/1.0"}

def extract_links_from_file(filepath: str) -> list:
    # Extract all links from the given XML file (without duplicates)
    links = set() # Use a set to avoid duplicate links

    try: 
        tree = ET.parse(filepath) # Parse the XML file and create an ElementTree object
        root = tree.getroot() # Get the root element of the XML tree

        # search in all text nodes
        for elem in root.iter(): 
            if elem.text:
                for link_match in URL_PATTERN.findall(elem.text):
                    links.add(link_match)

             # search in all attribute values (for example in href, target...) 
            for value in elem.attrib.values():
                for link_match in URL_PATTERN.findall(value):
                    links.add(link_match)

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

    return sorted(links) # Return the sorted list of unique links


def main():
    os.makedirs("outputs", exist_ok=True) # Ensure the output directory exists

    rows = [] # List to store filename and links for each paper (each row has: filename, link)

    for filename in os.listdir(INPUT_DIR):
        if not filename.endswith(".xml"):
            continue

        filepath = os.path.join(INPUT_DIR, filename)
        links = extract_links_from_file(filepath)
        if not links: # If there are no links, add a row with an empty string for the link
            rows.append([filename, ""])
        else: 
            for link in links: 
                rows.append([filename, link])
        
        print(f"{filename}: {len(links)} links")

        # Save the results to a CSV file
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "link"])
        writer.writerows(rows)

    print(f"Saved links per article to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()