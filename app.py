import streamlit as st
import json
from pathlib import Path

# ── data ────────────────────────────────────────────────────────────────────

SERIES = {
    "The Other One": {
        "figures": ["Amnesia","Cuckoo","Staring","Nowhere Safe","Raving","Marionette",
                    "Vagrancy","Being Alive","The Ghost","The Crow","The Monster","The Fox"],
        "secret": "Dreaming",
    },
    "Little Mischief": {
        "figures": ["Loose Fish","The Aviator","Persona","Boiling Frog","Protector",
                    "Cardboard Box","Hot Spring","Mechanic","Slingshot","Tied Up","Airplane","Chained"],
        "secret": "Hidden Edition",
    },
    "Mime": {
        "figures": ["Guardian","Blind","Devilry","Unspoken","Patience","Prison",
                    "Destroy","Drift","Fool","Seemer","Poem","Idol"],
        "secret": "Secret",
    },
    "Reshape": {
        "figures": ["Burst","Woodcarving","Fading","Healing","Paradise Lost",
                    "Drowning","Costume","Parasite","Voyage"],
        "secret": "Secret",
    },
    "Shelter": {
        "figures": ["Sneak Mantel","Candleholder","Poet","Alien","Birdy",
                    "Circus Strong","Traffic Cone","Cabin","Warrior","Sunny Doll"],
        "secret": "Secret",
    },
    "Echo": {
        "figures": ["Piece of Memory","Back Off","Caught You","Staying Up","Daydreaming Knight",
                    "Journey in the Rain","Soul Connection","Eaten","Get Lucky",
                    "Breakout Plan","Hiding Behind You","Remember"],
        "secret": "Secret",
    },
    "Le Petit Prince": {
        "figures": ["The Switchman","The Geographer","The Lamplighter","The King","The Fox",
                    "The Conceited Man","The Tippler","The Rose","The Businessman",
                    "The Snake","The Little Prince","The Merchant"],
        "secret": "The Pilot",
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
}

SAVE_FILE = Path("my_collection.json")

# ── persistence ──────────────────────────────────────────────────────────────

def load_collection():
    if SAVE_FILE.exists():
        try:
            return json.loads(SAVE_FILE.read_text())
        except Exception:
            pass
    return {}

def save_collection(data: dict):
    SAVE_FILE.write_text(json.dumps(data, indent=2))

# ── helpers ──────────────────────────────────────────────────────────────────

def all_figures(series_name: str) -> list[str]:
    s = SERIES[series_name]
    return s["figures"] + [s["secret"] + " ★"]

def fig_key(series: str, fig: str) -> str:
    return f"{series}||{fig}"

def get_status(collection: dict, series: str, fig: str) -> str:
    return collection.get(fig_key(series, fig), "none")

def set_status(collection: dict, series: str, fig: str, status: str):
    k = fig_key(series, fig)
    if collection.get(k) == status:
        collection[k] = "none"
    else:
        collection[k] = status
    save_collection(collection)


# --images --------------------------------------------------------------------

def get_image(series_name, fig_name):
    folder = series_name.lower().replace(" ", "_").replace("'", "").replace("_wild_", "_wild")
    filename = "_".join(w.capitalize() for w in fig_name.replace(" ★", "").split()) + ".png"
    path = Path("images") / folder / filename
    if path.exists():
        return path
    return None

# ── page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="hirono collection",
    page_icon="🪆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700&family=DM+Sans:wght@400;500&display=swap');

  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

  .main-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #e0a3c0;
    margin-bottom: 0;
    line-height: 1.1;
  }
  .main-sub {
    font-size: 0.82rem;
    color: #9d96b0;
    margin-top: 2px;
    margin-bottom: 1.2rem;
  }
  .series-header {
    font-family: 'Syne', sans-serif;
    font-size: 0.78rem;
    font-weight: 700;
    color: #e0a3c0;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    border-bottom: 1px solid #3d3950;
    padding-bottom: 0.3rem;
    margin-bottom: 0.5rem;
    display: flex;
    justify-content: space-between;
  }
  .secret-badge {
    background: #3d2840;
    color: #e8b4d8;
    font-size: 0.65rem;
    font-weight: 600;
    padding: 1px 6px;
    border-radius: 4px;
    vertical-align: middle;
    margin-left: 4px;
  }

  /* card colors */
  div[data-testid="stButton"] > button {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem;
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
  }
  .stat-box {
    background: #221f2b;
    border: 0.5px solid #3d3950;
    border-radius: 10px;
    padding: 0.6rem 1rem;
    text-align: center;
  }
  .stat-val { font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 700; }
  .stat-lbl { font-size: 0.7rem; color: #9d96b0; text-transform: uppercase; letter-spacing: 0.05em; }

  /* owned / want row highlight */
  .fig-owned { color: #b3e5c8 !important; }
  .fig-want  { color: #f5d0a0 !important; }
  .fig-none  { color: #e8e2f0; }

  /* hide streamlit branding */
  #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── state ────────────────────────────────────────────────────────────────────

if "collection" not in st.session_state:
    st.session_state.collection = load_collection()

col = st.session_state.collection

# ── header ───────────────────────────────────────────────────────────────────

st.markdown('<div class="main-title">hirono collection</div>', unsafe_allow_html=True)
st.markdown('<div class="main-sub">blind box tracker · pop mart</div>', unsafe_allow_html=True)

# ── stats ─────────────────────────────────────────────────────────────────────

total = sum(len(all_figures(s)) for s in SERIES)
owned = sum(1 for s in SERIES for f in all_figures(s) if get_status(col, s, f) == "owned")
want  = sum(1 for s in SERIES for f in all_figures(s) if get_status(col, s, f) == "want")
unchecked = total - owned - want

s1, s2, s3, s4, _ = st.columns([1, 1, 1, 1, 4])
with s1:
    st.markdown(f'<div class="stat-box"><div class="stat-val" style="color:#e0a3c0">{total}</div><div class="stat-lbl">figures</div></div>', unsafe_allow_html=True)
with s2:
    st.markdown(f'<div class="stat-box"><div class="stat-val" style="color:#b3e5c8">{owned}</div><div class="stat-lbl">owned</div></div>', unsafe_allow_html=True)
with s3:
    st.markdown(f'<div class="stat-box"><div class="stat-val" style="color:#f5d0a0">{want}</div><div class="stat-lbl">wishlist</div></div>', unsafe_allow_html=True)
with s4:
    st.markdown(f'<div class="stat-box"><div class="stat-val" style="color:#9d96b0">{unchecked}</div><div class="stat-lbl">unchecked</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── filters ───────────────────────────────────────────────────────────────────

fc1, fc2, fc3 = st.columns([2, 2, 1])
with fc1:
    status_filter = st.selectbox(
        "show", ["all", "owned", "wishlist", "unchecked"],
        label_visibility="collapsed"
    )
with fc2:
    series_filter = st.selectbox(
        "series", ["all series"] + list(SERIES.keys()),
        label_visibility="collapsed"
    )
with fc3:
    if st.button("🗑 clear all", use_container_width=True):
        st.session_state.collection = {}
        save_collection({})
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ── figure grid ───────────────────────────────────────────────────────────────

series_to_show = [series_filter] if series_filter != "all series" else list(SERIES.keys())

COLS = 4

for series_name in series_to_show:
    figs = all_figures(series_name)

    # apply status filter
    if status_filter == "owned":
        figs = [f for f in figs if get_status(col, series_name, f) == "owned"]
    elif status_filter == "wishlist":
        figs = [f for f in figs if get_status(col, series_name, f) == "want"]
    elif status_filter == "unchecked":
        figs = [f for f in figs if get_status(col, series_name, f) == "none"]

    if not figs:
        continue

    owned_in_series = sum(1 for f in all_figures(series_name) if get_status(col, series_name, f) == "owned")
    total_in_series = len(all_figures(series_name))

    st.markdown(
        f'<div class="series-header"><span>{series_name}</span>'
        f'<span style="color:#9d96b0;font-weight:400;font-size:0.75rem;text-transform:none;letter-spacing:0">'
        f'{owned_in_series}/{total_in_series} owned</span></div>',
        unsafe_allow_html=True
    )

    for row_start in range(0, len(figs), COLS):
        row_figs = figs[row_start : row_start + COLS]
        cols = st.columns(COLS)
        for i, fig in enumerate(row_figs):
            with cols[i]:
                is_secret = fig.endswith("★")
                display = fig.replace(" ★", "") if is_secret else fig
                status = get_status(col, series_name, fig)


                # name + secret badge
                badge = ' <span class="secret-badge">secret</span>' if is_secret else ""
                color = {"owned": "#b3e5c8", "want": "#f5d0a0"}.get(status, "#e8e2f0")
                st.markdown(
                    f'<div style="font-size:0.8rem;font-weight:500;color:{color};'
                    f'min-height:2.4em;line-height:1.3;margin-bottom:4px">'
                    f'{display}{badge}</div>',
                    unsafe_allow_html=True
                )

                img = get_image(series_name, display)

                if img:
                    st.image(str(img), use_container_width=True)

                b1, b2 = st.columns(2)

                with b1:
                    own_label = "✓ owned" if status == "owned" else "✓ own"
                    if st.button(own_label, key=f"own_{series_name}_{fig}", use_container_width=True):
                        set_status(col, series_name, fig, "owned")
                        st.rerun()
                with b2:
                    want_label = "♡ wanted" if status == "want" else "♡ want"
                    if st.button(want_label, key=f"want_{series_name}_{fig}", use_container_width=True):
                        set_status(col, series_name, fig, "want")
                        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)