from browser import document, window
import random

scale = 1.0
no_clicks = 0
hover_enabled = False
forced_under_yes = False

yes = document["yes"]
no  = document["no"]
msg = document["msg"]
q   = document["q"]

app = document["app"]
final = document["final"]
finalTitle = document["finalTitle"]
finalText = document["finalText"]

NO_TEXTS = [
    "Nie",
    "Co za harpia...",
    "No weeeeź Iza",
    "Budzik, obudź się",
    "Iza plis 🙏",
    "Jak możesz ;__;",
    "Na pewno nie?",
    "Szkoda strzępić ryja",
]

idx = 0

def set_no_text():
    global idx
    no.text = NO_TEXTS[idx]
    if idx < len(NO_TEXTS) - 1:
        idx += 1

def apply_transform():
    yes.style.transform = f"translate(70px, -50%) scale({scale})"

def move_no_anywhere_avoiding_yes():
    # Ensure button uses fixed positioning context
    no.style.position = "fixed"

    # Get fresh measurements
    vw = document.documentElement.clientWidth
    vh = document.documentElement.clientHeight

    # Force browser to recalculate sizes
    _ = no.offsetWidth

    nor = no.getBoundingClientRect()
    yesr = yes.getBoundingClientRect()

    btn_w = nor.width
    btn_h = nor.height

    # Use a smaller, viewport-proportional safety margin (so it works on small screens)
    margin = max(12, int(vw * 0.06))

    # Calculate safe zone (where button CENTER can be)
    safe_x_min = margin + btn_w / 2
    safe_x_max = vw - margin - btn_w / 2
    safe_y_min = margin + btn_h / 2
    safe_y_max = vh - margin - btn_h / 2

    # If there is no room, center the button as a fallback
    if safe_x_min > safe_x_max or safe_y_min > safe_y_max:
        cx = vw / 2
        cy = vh / 2
        no.style.left = f"{int(cx)}px"
        no.style.top = f"{int(cy)}px"
        no.style.transform = "translate(-50%, -50%)"
        return

    # Yes button forbidden zone (padding expands the forbidden area)
    pad = 40
    yes_l = yesr.left - pad
    yes_r = yesr.right + pad
    yes_t = yesr.top - pad
    yes_b = yesr.bottom + pad

    # Try to find a valid position
    for attempt in range(500):
        cx = random.uniform(safe_x_min, safe_x_max)
        cy = random.uniform(safe_y_min, safe_y_max)

        # Button edges based on center
        btn_l = cx - btn_w / 2
        btn_r = cx + btn_w / 2
        btn_t = cy - btn_h / 2
        btn_b = cy + btn_h / 2

        # Check overlap with YES button
        overlaps = not (btn_r <= yes_l or btn_l >= yes_r or btn_b <= yes_t or btn_t >= yes_b)

        if not overlaps:
            # Clamp final coordinates as a safety net
            cx = max(safe_x_min, min(cx, safe_x_max))
            cy = max(safe_y_min, min(cy, safe_y_max))

            no.style.left = f"{int(cx)}px"
            no.style.top = f"{int(cy)}px"
            no.style.transform = "translate(-50%, -50%)"
            return

    # Final fallback: put button at the nearest safe corner
    cx = safe_x_min
    cy = safe_y_min
    no.style.left = f"{int(cx)}px"
    no.style.top = f"{int(cy)}px"
    no.style.transform = "translate(-50%, -50%)"

def put_no_under_yes():
    global forced_under_yes, hover_enabled
    forced_under_yes = True
    hover_enabled = False

    r = yes.getBoundingClientRect()
    cx = r.left + r.width / 2
    cy = r.top + r.height / 2

    no.style.position = "fixed"
    no.style.left = f"{cx}px"
    no.style.top = f"{cy}px"
    no.style.transform = "translate(-50%, -50%)"
    no.style.zIndex = "10001"
    yes.style.zIndex = "10002"

    msg.text = "Dumna z siebie jesteś?"

def on_no(ev):
    global scale, no_clicks, hover_enabled

    bgm = document["bgm"]
    bgm.volume = 0.1
    bgm.play()

    no_clicks += 1
    set_no_text()

    scale *= 1.35
    apply_transform()

    if no_clicks >= 7 and not forced_under_yes:
        put_no_under_yes()
        return

    if no_clicks >= 3 and not hover_enabled:
        hover_enabled = True
        no.style.transition = "left 0.12s ease, top 0.12s ease"
        # Wait a frame for text to render
        window.setTimeout(move_no_anywhere_avoiding_yes, 10)

def on_no_hover(ev):
    if hover_enabled and not forced_under_yes:
        move_no_anywhere_avoiding_yes()

def on_yes(ev):
    bgm = document["bgm"]
    bgm.volume = 0.1
    bgm.play()

    app.style.display = "none"
    final.style.display = "block"

    finalTitle.text = "Less GOOOOO!! 💘💘💘"
    finalText.text = "To randka! Widzimy się po powrocie ❤️"

    window.party()

no.bind("click", on_no)
no.bind("mouseover", on_no_hover)
yes.bind("click", on_yes)

set_no_text()
apply_transform()
