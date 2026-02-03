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

buttons = document["buttonsArea"]

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
    # a,b: (left, top, right, bottom)
    return not (a[2] <= b[0] or a[0] >= b[2] or a[3] <= b[1] or a[1] >= b[3])

def move_no_randomly_avoiding_yes():
    """
    Losujemy pozycję 'Nie' w obrębie kontenera przycisków tak,
    żeby NIE nachodziło na przycisk 'Tak' (nawet jak 'Tak' urośnie).
    """
    area = buttons.getBoundingClientRect()
    yesr = yes.getBoundingClientRect()

    # rozmiar "Nie" (po aktualnym tekście)
    nor = no.getBoundingClientRect()
    no_w = nor.width
    no_h = nor.height

    # margines bezpieczeństwa (żeby nie wchodziło w "Tak" i krawędzie)
    pad = 10

    # dopuszczalny zakres (w px, w obrębie kontenera)
    min_x = pad + no_w / 2
    max_x = max(min_x, area.width - pad - no_w / 2)
    min_y = pad + no_h / 2
    max_y = max(min_y, area.height - pad - no_h / 2)

    # jeśli kontener jest za mały (np. mega Tak), to i tak uciekamy w róg
    if area.width < no_w + 2*pad or area.height < no_h + 2*pad:
        no.style.left = "15%"
        no.style.top = "30%"
        no.style.transform = "translate(-50%, -50%)"
        return

    # próbujemy kilka razy znaleźć miejsce bez kolizji z "Tak"
    for _ in range(40):
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)

        # rect "Nie" w układzie strony (viewport)
        no_rect = (
            area.left + x - no_w/2,
            area.top  + y - no_h/2,
            area.left + x + no_w/2,
            area.top  + y + no_h/2,
        )

        # powiększamy trochę rect "Tak" (bufor), żeby nie “ocierało się”
        buf = 14
        yes_rect = (yesr.left - buf, yesr.top - buf, yesr.right + buf, yesr.bottom + buf)

        if not rects_intersect(no_rect, yes_rect):
            # ustawiamy left/top w px względem kontenera
            no.style.left = f"{x}px"
            no.style.top = f"{y}px"
            no.style.transform = "translate(-50%, -50%)"
            return

    # awaryjnie: jak nie znaleźliśmy miejsca, uciekaj w bezpieczny róg
    no.style.left = f"{min_x}px"
    no.style.top = f"{min_y}px"
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

    if no_clicks >= 3 and not hover_enabled:
        hover_enabled = True
        no.style.transition = "left 0.15s ease, top 0.15s ease"

def on_no_hover(ev):
    if hover_enabled:
        move_no_randomly_avoiding_yes()

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
