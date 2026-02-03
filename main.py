from browser import document, window
import random

scale = 1.0
no_clicks = 0
hover_enabled = False

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

def move_no_randomly():
    # losowe miejsce w obrębie kontenera przycisków
    x = random.randint(10, 90)
    y = random.randint(20, 80)

    no.style.left = f"{x}%"
    no.style.top = f"{y}%"
    no.style.transform = "translate(-50%, -50%)"

def on_no(ev):
    global scale, no_clicks, hover_enabled

    no_clicks += 1

    bgm = document["bgm"]
    bgm.volume = 0.1
    bgm.play()

    set_no_text()

    scale *= 1.35
    apply_transform()

    # po 3 kliknięciach aktywujemy uciekanie na hover
    if no_clicks >= 3 and not hover_enabled:
        hover_enabled = True
        no.style.transition = "left 0.15s ease, top 0.15s ease"

def on_no_hover(ev):
    if hover_enabled:
        move_no_randomly()

def on_yes(ev):
    bgm = document["bgm"]
    bgm.volume = 0.1
    bgm.play()

    app.style.display = "none"
    final.style.display = "block"

    finalTitle.text = "Less GOOOOO!! 💘💘💘"
    finalText.text = "To randka! Widzimy się po powrocie ❤️"

    window.party()

# eventy
no.bind("click", on_no)
no.bind("mouseover", on_no_hover)
yes.bind("click", on_yes)

# start
set_no_text()
apply_transform()
