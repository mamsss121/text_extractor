import os
import csv
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

INPUT_DIR = "data/grobid"
OUTPUT_CSV="outputs/figures_per_paper.csv"
OUTPUT_FIG="outputs/figures_per_paper.png"

ns = {"tei": "http://www.tei-c.org/ns/1.0"}

def count_figures_in_file(filepath: str) -> int:
    # Counts the number of <figure> elements in the given XML file
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        figures = root.findall(".//tei:figure", ns)
        return len(figures)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return 0
    
def main():
    rows = [] # List to store filename and figure count for each paper

    # Ensure the output directory exists
    os.makedirs("outputs", exist_ok=True) 

    for filename in os.listdir(INPUT_DIR):
        if not filename.endswith(".xml"):
            continue
        file_path = os.path.join(INPUT_DIR, filename)
        figure_count = count_figures_in_file(file_path)
        rows.append([filename, figure_count])
        print(f"{filename}: {figure_count} figures")

    # Save the results to a CSV file
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "figure_count"])
        writer.writerows(rows)

    # Create a bar chart

    filenames = [row[0] for row in rows] 
    counts = [row[1] for row in rows]

    plt.figure(figsize=(10, 5))
    plt.bar(range(len(filenames)), counts)
    plt.xticks(range(len(filenames)), filenames, rotation=45, ha="right") # Rotate x-axis labels for better readability
    plt.ylabel("Number of figures")
    plt.xlabel("Paper")
    plt.title("Number of figures per paper")
    plt.tight_layout() # Adjust layout to prevent clipping of labels
    plt.savefig(OUTPUT_FIG) 
    plt.close() # Close the figure to free up memory

    print(f"Saved figures per article to {OUTPUT_CSV}")
    print(f"Saved bar chart to {OUTPUT_FIG}")

if __name__ == "__main__":
    main()