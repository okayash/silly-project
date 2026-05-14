import requests
import json
import time
from pathlib import Path

# ── config ────────────────────────────────────────────────────────────────────

CDN_URL = "https://cdn-global.popmart.com/shop_productoncollection-4-1-1-us-en.json?t=1"

TARGET_IDS = {
    "5166": "Road Journal",
    "3944": "Monsters Carnival",
    "13":   "Little Mischief",
    "1604": "Le Petit Prince",
    "739":  "The Other One",
    "365":  "Mime",
    "2165": "Echo",
    "1385": "Shelter",
    "867":  "Reshape",
    "6071": "Tamed Wildgrass",
    "6070": "Little Hare",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "application/json",
    "Referer": "https://www.popmart.com/",
}

OUTPUT_DIR = Path("scraped")
OUTPUT_DIR.mkdir(exist_ok=True)

# ── fetch brand data ──────────────────────────────────────────────────────────

print("fetching hirono brand data...")
response = requests.get(CDN_URL, headers=HEADERS)
response.raise_for_status()
data = response.json()

products = data["productData"]
print(f"found {len(products)} total hirono products\n")

# ── filter + download ─────────────────────────────────────────────────────────

metadata = {}

for product in products:
    pid = str(product["id"])
    if pid not in TARGET_IDS:
        continue

    series_name = TARGET_IDS[pid]
    banner_images = product.get("bannerImages", [])

    print(f"── {series_name} (id: {pid})")
    print(f"   images: {len(banner_images)}")

    folder = OUTPUT_DIR / series_name.lower().replace(" ", "_")
    folder.mkdir(exist_ok=True)

    for i, img_url in enumerate(banner_images):
        ext = img_url.split(".")[-1].split("?")[0]
        dest = folder / f"{i+1:02d}.{ext}"
        if dest.exists():
            print(f"   skip: {dest.name}")
            continue
        try:
            r = requests.get(img_url, headers=HEADERS, timeout=15)
            r.raise_for_status()
            dest.write_bytes(r.content)
            print(f"   downloaded: {dest.name}")
            time.sleep(0.2)
        except Exception as e:
            print(f"   failed {dest.name}: {e}")

    metadata[series_name] = {
        "product_id": pid,
        "title": product["title"],
        "image_count": len(banner_images),
        "images": banner_images,
    }

# ── save metadata ─────────────────────────────────────────────────────────────

meta_path = OUTPUT_DIR / "metadata.json"
meta_path.write_text(json.dumps(metadata, indent=2))

print(f"\n✓ done! {len(metadata)} series scraped")
print(f"✓ metadata saved to {meta_path}")