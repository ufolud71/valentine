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

def rects_intersect(a, b):
    return not (a[2] <= b[0] or a[0] >= b[2] or a[3] <= b[1] or a[1] >= b[3])

def move_no_anywhere_avoiding_yes():
    """Ucieka po całym ekranie (viewport) i nie ląduje pod 'Tak'."""
    yesr = yes.getBoundingClientRect()
    nor = no.getBoundingClientRect()
    no_w = nor.width
    no_h = nor.height

    pad = 12
    buf = 16

    vw = window.innerWidth
    vh = window.innerHeight

    min_x = pad + no_w / 2
    max_x = max(min_x, vw - pad - no_w / 2)
    min_y = pad + no_h / 2
    max_y = max(min_y, vh - pad - no_h / 2)

    yes_rect = (yesr.left - buf, yesr.top - buf, yesr.right + buf, yesr.bottom + buf)

    for _ in range(60):
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)
        no_rect = (x - no_w/2, y - no_h/2, x + no_w/2, y + no_h/2)

        if not rects_intersect(no_rect, yes_rect):
            no.style.left = f"{x}px"
            no.style.top = f"{y}px"
            no.style.transform = "translate(-50%, -50%)"
            return

    # awaryjnie róg
    no.style.left = f"{min_x}px"
    no.style.top = f"{min_y}px"
    no.style.transform = "translate(-50%, -50%)"

def put_no_under_yes():
    """Ustaw 'Nie' dokładnie pod 'Tak' + niższy z-index, żeby zostało zasłonięte."""
    global forced_under_yes, hover_enabled
    forced_under_yes = True
    hover_enabled = False

    r = yes.getBoundingClientRect()
    cx = r.left + r.width / 2
    cy = r.top + r.height / 2

    # No musi być fixed, żeby trzymało się ekranu (jeśli masz fixed w CSS, super)
    no.style.position = "fixed"
    no.style.left = f"{cx}px"
    no.style.top = f"{cy}px"
    no.style.transform = "translate(-50%, -50%)"

    # Upewniamy się, że jest POD "Tak"
    no.style.zIndex = "10001"
    yes.style.zIndex = "10002"

    msg.text = "Dumna z siebie jesteś?"

def on_no(ev):
    global scale, no_clicks, hover_enabled

    # muzyka
    bgm = document["bgm"]
    bgm.volume = 0.1
    bgm.play()

    no_clicks += 1
    set_no_text()

    scale *= 1.35
    apply_transform()

    # po 7 kliknięciach: MUSI wylądować pod TAK i koniec uciekania
    if no_clicks >= 7 and not forced_under_yes:
        put_no_under_yes()
        return

    # po 3 kliknięciach: włącz uciekanie na hover
    if no_clicks >= 3 and not hover_enabled:
        hover_enabled = True
        no.style.transition = "left 0.12s ease, top 0.12s ease"

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
