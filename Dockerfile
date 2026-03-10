# Dockerfile for text_extractor project

# 1. Base image with Python
FROM python:3.11-slim

# 2. Work directory inside the container
WORKDIR /app

# 3. Install OS-level dependencies if needed (currently minimal)
# Uncomment and add packages if you ever need them.
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends <system-packages> && \
#     rm -rf /var/lib/apt/lists/*

# 4. Copy dependency file(s) and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the project into the image
# This brings in scripts/, data/, outputs/ (empty or precreated), tests/, docs/, etc.
COPY . .

# 6. Default command: run the full analysis pipeline
# Make sure you have a run_pipeline.py at the repo root that orchestrates
# scripts/count_figures.py, scripts/extract_links.py, scripts/generate_keyword_cloud.py
ENTRYPOINT ["python", "run_pipeline.py"]
