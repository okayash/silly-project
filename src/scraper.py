
import requests
import os
import json
import time

''' 

CURRENTLY NOT WORKING

'''

# ── series config ─────────────────────────────────────────────────────────────

SERIES = {
    "Road Journal":       5166,
    "Monsters Carnival":  3944,
    "Little Mischief":    13,
    "Le Petit Prince":    1604,
    "The Other One":      739,
    "Mime":               365,
    "Echo":               2165,
    "Shelter":            1385,
    "Reshape":            867,
    "Tamed Wildgrass":    6071,
    "Little Hare":        6070,
}

API_BASE = "https://www.popmart.com/api/us/v2/product"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://www.popmart.com/",
}

# ── output dirs ───────────────────────────────────────────────────────────────

OUTPUT_DIR = Path("scraped")
OUTPUT_DIR.mkdir(exist_ok=True)

# ── helpers ───────────────────────────────────────────────────────────────────

def folder_name(series_name: str) -> str:
    return series_name.lower().replace(" ", "_").replace("'", "")

def fetch_series(product_id: int) -> dict:
    url = f"{API_BASE}/{product_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def download_image(url: str, dest: Path):
    if dest.exists():
        print(f"  skip (exists): {dest.name}")
        return
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        dest.write_bytes(r.content)
        print(f"  downloaded: {dest.name}")
    except Exception as e:
        print(f"  failed {dest.name}: {e}")

# ── main ──────────────────────────────────────────────────────────────────────

all_metadata = {}

for series_name, product_id in SERIES.items():
    print(f"\n── {series_name} (id: {product_id})")

    try:
        data = fetch_series(product_id)
    except Exception as e:
        print(f"  ERROR fetching: {e}")
        continue

    if data.get("code") != "OK":
        print(f"  API error: {data.get('message')}")
        continue

    product = data["data"]

    # pull banner images
    banner_images = product.get("bannerImages", [])
    desc = product.get("desc", "")

    print(f"  title: {product['title']}")
    print(f"  images found: {len(banner_images)}")

    # save images
    folder = OUTPUT_DIR / folder_name(series_name)
    folder.mkdir(exist_ok=True)

    for i, img_url in enumerate(banner_images):
        ext = img_url.split(".")[-1].split("?")[0]
        filename = f"{i+1:02d}.{ext}"
        download_image(img_url, folder / filename)
        time.sleep(0.3)  # be polite, don't hammer the server

    # save metadata
    all_metadata[series_name] = {
        "product_id": product_id,
        "title": product["title"],
        "desc": desc,
        "image_count": len(banner_images),
        "images": banner_images,
    }

    time.sleep(0.5)

# save full metadata to json
meta_path = OUTPUT_DIR / "metadata.json"
meta_path.write_text(json.dumps(all_metadata, indent=2))
print(f"\n✓ done! metadata saved to {meta_path}")
print(f"✓ images saved to {OUTPUT_DIR}/")