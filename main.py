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
    # Get fresh measurements
    vw = document.documentElement.clientWidth
    vh = document.documentElement.clientHeight
    
    # Force browser to recalculate
    _ = no.offsetWidth
    
    nor = no.getBoundingClientRect()
    yesr = yes.getBoundingClientRect()
    
    btn_w = nor.width
    btn_h = nor.height
    
    # Huge safety margin
    margin = 100
    
    # Calculate safe zone (where button CENTER can be)
    safe_x_min = margin + btn_w/2
    safe_x_max = vw - margin - btn_w/2
    safe_y_min = margin + btn_h/2
    safe_y_max = vh - margin - btn_h/2
    
    # Safety check
    if safe_x_min >= safe_x_max or safe_y_min >= safe_y_max:
        no.style.left = "150px"
        no.style.top = "150px"
        no.style.transform = "translate(-50%, -50%)"
        return
    
    # Yes button forbidden zone
    pad = 40
    yes_l = yesr.left - pad
    yes_r = yesr.right + pad
    yes_t = yesr.top - pad
    yes_b = yesr.bottom + pad
    
    # Try to find valid position
    for attempt in range(300):
        cx = random.uniform(safe_x_min, safe_x_max)
        cy = random.uniform(safe_y_min, safe_y_max)
        
        # Calculate where button edges would be
        btn_l = cx - btn_w/2
        btn_r = cx + btn_w/2
        btn_t = cy - btn_h/2
        btn_b = cy + btn_h/2
        
        # Check if overlaps with YES button
        overlaps = not (btn_r < yes_l or btn_l > yes_r or btn_b < yes_t or btn_t > yes_b)
        
        if not overlaps:
            no.style.left = f"{int(cx)}px"
            no.style.top = f"{int(cy)}px"
            no.style.transform = "translate(-50%, -50%)"
            return
    
    # Fallback: top left corner
    no.style.left = "150px"
    no.style.top = "150px"
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
