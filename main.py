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
    # Use fixed positioning context
    no.style.position = "fixed"

    # Fresh viewport and element measurements
    vw = document.documentElement.clientWidth
    vh = document.documentElement.clientHeight

    # Force layout/read to get current sizes after text change
    _ = no.offsetWidth
    nor = no.getBoundingClientRect()
    yesr = yes.getBoundingClientRect()

    btn_w = nor.width
    btn_h = nor.height

    # Viewport-proportional padding so small screens are handled
    padding = max(8, int(min(vw, vh) * 0.06))

    # Allowed left/top edges (we treat positions as edges here)
    allowed_left_min = padding
    allowed_left_max = max(padding, vw - padding - btn_w)
    allowed_top_min = padding
    allowed_top_max = max(padding, vh - padding - btn_h)

    # If not enough room, center the button (safe fallback)
    if allowed_left_min > allowed_left_max or allowed_top_min > allowed_top_max:
        cx = vw / 2
        cy = vh / 2
        no.style.left = f"{int(cx)}px"
        no.style.top = f"{int(cy)}px"
        no.style.transform = "translate(-50%, -50%)"
        return

    # Forbidden rectangle (yes button) expanded by a padding
    extra_pad = max(16, int(min(vw, vh) * 0.04))
    yes_forbid_left = yesr.left - extra_pad
    yes_forbid_right = yesr.right + extra_pad
    yes_forbid_top = yesr.top - extra_pad
    yes_forbid_bottom = yesr.bottom + extra_pad

    # Try many random candidates (edges), check for overlap, then clamp and place center
    attempts = 1000
    for _ in range(attempts):
        left_edge = random.uniform(allowed_left_min, allowed_left_max)
        top_edge  = random.uniform(allowed_top_min, allowed_top_max)
        right_edge = left_edge + btn_w
        bottom_edge = top_edge + btn_h

        # Check overlap between candidate rect and forbidden rect
        no_intersect = (right_edge <= yes_forbid_left or left_edge >= yes_forbid_right or
                        bottom_edge <= yes_forbid_top or top_edge >= yes_forbid_bottom)

        if no_intersect:
            # Clamp to allowed edges as safety net
            left_edge = max(allowed_left_min, min(left_edge, allowed_left_max))
            top_edge  = max(allowed_top_min,  min(top_edge,  allowed_top_max))

            # Convert to center coordinates because CSS uses translate(-50%, -50%)
            cx = left_edge + btn_w / 2
            cy = top_edge + btn_h / 2

            no.style.left = f"{int(cx)}px"
            no.style.top = f"{int(cy)}px"
            no.style.transform = "translate(-50%, -50%)"
            return

    # If nothing found, place at nearest allowed corner (top-left)
    left_edge = allowed_left_min
    top_edge = allowed_top_min
    cx = left_edge + btn_w / 2
    cy = top_edge + btn_h / 2
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
