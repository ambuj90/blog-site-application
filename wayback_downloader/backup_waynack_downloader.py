import requests # type: ignore
import os
import time

# Function to get all available snapshots
def get_snapshots(domain):
    url = f"https://web.archive.org/cdx/search/cdx?url={domain}&output=json"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data[1:] if len(data) > 1 else []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching snapshots: {e}")
        return []

# Function to get one snapshot per year
def get_one_snapshot_per_year(snapshots):
    yearly_snapshots = {}
    for snapshot in snapshots:
        timestamp = snapshot[1]
        year = timestamp[:4]  # Extracting the year
        
        # ✅ Only add the first snapshot of each year
        if year not in yearly_snapshots:
            yearly_snapshots[year] = snapshot

    return yearly_snapshots


# Function to download and save HTML file with organized naming
def download_html(snapshot, domain):
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
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(response.text)

            print(f"✅ Saved: {file_path}")
            time.sleep(2)  # Delay to prevent rate-limiting
            return  # ✅ Exit loop if successful

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Attempt {attempt + 1} failed: {e}")
            time.sleep(5)  # Wait before retrying

    print(f"❌ Failed to download after {attempts} attempts: {archive_url}")

# Main function to call from other scripts
def download_archived_site(domain):
    snapshots = get_snapshots(domain)
    yearly_snapshots = get_one_snapshot_per_year(snapshots)

    if yearly_snapshots:
        for year, snapshot in yearly_snapshots.items():
            print(f"📅 Downloading {year} snapshot for {domain}...")
            download_html(snapshot, domain)

        print("\n🎉 Download complete.")
    else:
        print("❌ No snapshots found.")
