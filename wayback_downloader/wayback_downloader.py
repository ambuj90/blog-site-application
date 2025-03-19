import os
import json
from bs4 import BeautifulSoup
import requests
import time


def get_snapshots(domain):
    """Fetch Wayback Machine snapshots for a domain."""
    url = f"https://web.archive.org/cdx/search/cdx?url={domain}&output=json"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data[1:] if len(data) > 1 else []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching snapshots: {e}")
        return []

def get_one_snapshot_per_year(snapshots):
    """Extracts the first available snapshot per year."""
    yearly_snapshots = {}
    for snapshot in snapshots:
        timestamp = snapshot[1]
        year = timestamp[:4]  # Extracting the year
        
        # ✅ Only add the first snapshot of each year
        if year not in yearly_snapshots:
            yearly_snapshots[year] = snapshot

    return yearly_snapshots

def download_html(snapshot, domain):
    """Downloads and saves the HTML content of a snapshot."""
    timestamp = snapshot[1]
    year = timestamp[:4]
    archive_url = f"https://web.archive.org/web/{timestamp}/{domain}"

    attempts = 3  # ✅ Number of retries

    for attempt in range(attempts):
        try:
            response = requests.get(archive_url, timeout=15)
            response.raise_for_status()
            
            domain_folder = os.path.join("archived_sites", domain.replace(".", "_"), year)
            os.makedirs(domain_folder, exist_ok=True)

            file_path = os.path.join(domain_folder, f"{domain.replace('.', '_')}_{year}.html")
            with open(file_path, "w", encoding="utf-8", errors="replace") as file:
                file.write(response.text)

            print(f"✅ Saved: {file_path}")
            time.sleep(2)  # Delay to prevent rate-limiting
            return  # ✅ Exit loop if successful

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Attempt {attempt + 1} failed: {e}")
            time.sleep(5)  # Wait before retrying

    print(f"❌ Failed to download after {attempts} attempts: {archive_url}")

def download_archived_site(domain):
    """Downloads historical snapshots from Wayback Machine."""
    snapshots = get_snapshots(domain)
    yearly_snapshots = get_one_snapshot_per_year(snapshots)

    if yearly_snapshots:
        for year, snapshot in yearly_snapshots.items():
            print(f"📅 Downloading {year} snapshot for {domain}...")
            download_html(snapshot, domain)

        print("\n🎉 Download complete.")
    else:
        print("❌ No snapshots found.")
# Function to extract visible text from an HTML file
def extract_text_content(html_file):
    """Extracts visible text from an HTML file."""
    try:
        with open(html_file, "r", encoding="utf-8", errors="replace") as file:  # ✅ Ensure correct encoding
            soup = BeautifulSoup(file, "html.parser")

        # Remove scripts, styles, and non-visible elements
        for script in soup(["script", "style", "noscript"]):
            script.extract()

        text = soup.get_text(separator=" ", strip=True)
        return text.lower() if text else "no_content"
    except Exception as e:
        print(f"Error reading {html_file}: {e}")
        return "error"

# Function to analyze domain changes (Content & SEO)
def analyze_domain_changes(domain, api_key):
    domain_folder = os.path.join("archived_sites", domain.replace(".", "_"))
    year_files = {}

    # Load HTML files by year
    for root, dirs, files in os.walk(domain_folder):
        for file in files:
            if file.endswith(".html"):
                year = file.split("_")[-1][:4]  # Extract year from filename
                year_files[year] = os.path.join(root, file)

    if not year_files:
        return {"niche_analysis": {}, "niche_changed": False}

    niche_analysis = {}
    for year, html_file in year_files.items():
        text_content = extract_text_content(html_file)

        if text_content == "no_content":
            niche_analysis[year] = "empty_page"
            continue

        # Classify website niche based on keywords in content
        if "buy" in text_content or "checkout" in text_content or "shop" in text_content:
            detected_niche = "ecommerce"
        elif "subscribe" in text_content or "membership" in text_content:
            detected_niche = "subscription"
        elif "review" in text_content or "best" in text_content:
            detected_niche = "affiliate"
        elif "ads" in text_content or "advertisement" in text_content:
            detected_niche = "advertising"
        else:
            detected_niche = "blog"

        niche_analysis[year] = detected_niche

    # Compare first and last year to detect niche change
    niche_years = list(niche_analysis.keys())
    niche_changed = niche_analysis[niche_years[0]] != niche_analysis[niche_years[-1]] if len(niche_years) > 1 else False

    return {
        "niche_analysis": niche_analysis,
        "niche_changed": niche_changed
    }
