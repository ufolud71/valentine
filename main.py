from browser import document
from browser import document, window

scale = 1.0

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

def on_no(ev):
    global scale
    bgm = document["bgm"]
    bgm.volume = 0.35
    bgm.play()
    set_no_text()

    scale *= 1.35
    apply_transform()

def on_yes(ev):
    bgm = document["bgm"]
    bgm.volume = 0.35
    bgm.play()
    # ukryj ekran 1
    app.style.display = "none"

    # pokaż ekran 2
    final.style.display = "block"

    # ustaw treści finału (możesz tu wpisać co chcesz)
    finalTitle.text = "Less GOOOOO!! 💘💘💘"
    finalText.text = "To randka! Widzimy się po powrocie ❤️"
    window.party() 

no.bind("click", on_no)
yes.bind("click", on_yes)

set_no_text()
apply_transform()
