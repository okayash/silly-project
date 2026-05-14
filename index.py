import torch
import json
from pathlib import Path
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

SERIES = {
       "The Other One": {
        "figures": ["Amnesia","Cuckoo","Staring","Nowhere Safe","Raving","Marionette",
                    "Vagrancy","Being Alive","The Ghost","The Crow","The Monster","The Fox"],
        "secret": "Dreaming",
    },
    "Little Mischief": {
        "figures": ["Rag Picker", "Destroyer", "Robot", "Boiling Frog", "Float", "The Aviator", "Birdman", 
                    "Loose Fish", "Pretender", "Persona", "Manacle", "Protector"],
        "secret": "Unknown Journey",
    },
    "Mime": {
        "figures": ["Blind","Destroy","Devilry","Drifter","Fool","Guardian",
                    "Patience","Poem","Prison","Secrecy","Seeker","Unspoken"],
        "secret": "Silent",
    },
    "Reshape": {
        "figures": ["Burst","Woodcarving","Fading","Healing","Paradise Lost",
                    "Drowning","Costume","Parasite","Voyage"],
        "secret": "Puppet",
    },
    "Shelter": {
        "figures": ["Mantel Clock","Candleholder","Poet","Alien","Birdy",
                    "Circus","Traffic Cone","Cabin","Warrior","Sunny Doll"],
        "secret": "Stuffed Bear",
    },
    "Echo": {
        "figures": ["Back Off", "Breakout Plan", "Caught You", "Daydreaming", "Eaten", "Get Lucky", "Hiding Behind You",
                    "Journey in the Rain", "Knight","Pieces of Memory", "Soul Connection", "Staying Up"],
        "secret": "Never Growing Up",
    },
    "Le Petit Prince": {
        "figures": ["The Switchman","The Geographer","The Lamplighter","The King","The Fox",
                    "The Conceited Man","The Tippler","The Rose","The Businessman",
                    "The Snake","The Little Prince","The Merchant"],
        "secret": ["The Pilot", "The Little Prince Special Edition"]
    },
    "Monsters' Carnival": {
        "figures": ["Grim Reaper","Doctor Beak","Killer Bunny","Zombie","Vampire","Creepy Clown"],
        "secret": "The Disembodied",
    },
    "Road Journal": {
        "figures": ["City Dust Afloat","Grey Gravel","Woven Woods",
                    "Lost in the Night","Into Fogwild","Frostfall Hour"],
        "secret": "Highway Imprint",
    },
        "Tamed Wildgrass": {
        "figures": ["Sisyphean Work","Live Under Receipts","Full-time","Canned Dreams","Fated",
                    "Camping","Digital Bind","Overload","Boiling Frog","Caged Bird",
                    "Self Anchored","City Escape"],
        "secret": "Boundary",
    },
            "Little Hare": {
        "figures": ["Pink Hare"],
        "secret": "Black Hare",
    },
}

def all_figures(series_name):
    s = SERIES[series_name]
    secret = s["secret"]
    if isinstance(secret, list):
        return s["figures"] + [sec + " ★" for sec in secret]
    return s["figures"] + [secret + " ★"]

def get_image_path(series_name, fig_name):
    folder = series_name.lower().replace(" ", "_").replace("'", "")
    filename = fig_name.lower().replace(" ★", "").replace(" ", "_") + ".png"
    return Path("images") / folder / filename

index = []

for series_name in SERIES:
    for fig in all_figures(series_name):
        path = get_image_path(series_name, fig)
        if not path.exists():
            print(f"missing: {path}")
            continue
        image = Image.open(path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")
        with torch.no_grad():
            outputs = model.vision_model(**inputs)
            embedding = outputs.pooler_output
            embedding = embedding / embedding.norm(dim=-1, keepdim=True)
        index.append({
            "series": series_name,
            "figure": fig,
            "embedding": embedding[0].tolist()
        })
        print(f"indexed: {series_name} - {fig}")

with open("hirono_index.json", "w") as f:
    json.dump(index, f)

print(f"\ndone! indexed {len(index)} figures")