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
    """Ucieka po ekranie, ale twardo zostaje w viewport i nie ląduje pod 'Tak'."""
    vw = window.innerWidth
    vh = window.innerHeight
    edge = 20      # margines od krawędzi
    buf = 20       # bufor wokół "Tak"

    yesr = yes.getBoundingClientRect()
    nor = no.getBoundingClientRect()
    no_width = nor.width
    no_height = nor.height

    def rects_intersect_check(a, b):
        return not (a["right"] <= b["left"] or a["left"] >= b["right"] or 
                    a["bottom"] <= b["top"] or a["top"] >= b["bottom"])

    # "strefa zakazana" wokół TAK
    yes_box = {
        "left": yesr.left - buf,
        "top": yesr.top - buf,
        "right": yesr.right + buf,
        "bottom": yesr.bottom + buf,
    }

    # próbujemy kilka razy znaleźć miejsce
    for _ in range(100):
        # z transform translate(-50%, -50%), pozycja to środek elementu
        # więc losujemy z uwzględnieniem połowy szerokości/wysokości
        x = random.uniform(edge + no_width/2, vw - edge - no_width/2)
        y = random.uniform(edge + no_height/2, vh - edge - no_height/2)

        # symulujemy gdzie będzie przycisk
        test_box = {
            "left": x - no_width/2,
            "top": y - no_height/2,
            "right": x + no_width/2,
            "bottom": y + no_height/2,
        }

        # sprawdź czy nie nachodzi na TAK
        if not rects_intersect_check(test_box, yes_box):
            no.style.left = f"{x}px"
            no.style.top = f"{y}px"
            no.style.transform = "translate(-50%, -50%)"
            return

    # awaryjnie: górny lewy róg (bezpieczna pozycja)
    safe_x = edge + no_width/2 + 10
    safe_y = edge + no_height/2 + 10
    no.style.left = f"{safe_x}px"
    no.style.top = f"{safe_y}px"
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
