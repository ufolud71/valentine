from browser import document, window
import random

scale = 1.0
no_clicks = 0
hover_enabled = False
forced_under_yes = False

# Interaction state
hovering = False
hover_timeout_id = None
pointer_down = False

yes = document["yes"]
no  = document["no"]
msg = document["msg"]
q   = document["q"]
buttonsArea = document["buttonsArea"]

app = document["app"]
final = document["final"]
finalTitle = document["finalTitle"]
finalText = document["finalText"]

# The boundary element (in which #no must stay)
boundary = document["no-boundary"]

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

# Mirror initial NO position across the center of the small buttons frame
def place_no_mirrored():
    # compute centers in viewport coordinates
    brect = buttonsArea.getBoundingClientRect()
    center_x = brect.left + brect.width / 2
    center_y = brect.top + brect.height / 2

    yesr = yes.getBoundingClientRect()
    yes_cx = yesr.left + yesr.width / 2
    yes_cy = yesr.top + yesr.height / 2

    dx = yes_cx - center_x
    # mirror across center: subtract dx
    no_cx = center_x - dx
    no_cy = yes_cy

    # ensure no is positioned absolute inside the boundary
    no.style.position = "absolute"
    no.style.left = f"{int(no_cx)}px"
    no.style.top = f"{int(no_cy)}px"
    no.style.transform = "translate(-50%, -50%)"

# Core placement: choose a position inside boundary avoiding YES
def move_no_anywhere_avoiding_yes():
    # Ensure the button is absolutely positioned inside the boundary container
    no.style.position = "absolute"

    # Boundary rectangle (fixed, covers viewport)
    brect = boundary.getBoundingClientRect()

    # Fresh element measurements after any text change
    _ = no.offsetWidth
    nor = no.getBoundingClientRect()
    yesr = yes.getBoundingClientRect()

    btn_w = nor.width
    btn_h = nor.height

    # Padding inside boundary (viewport-proportional)
    padding = max(8, int(min(brect.width, brect.height) * 0.06))

    # Allowed left/top edges inside boundary (absolute coordinates in viewport)
    allowed_left_min = brect.left + padding
    allowed_left_max = brect.right - padding - btn_w
    allowed_top_min = brect.top + padding
    allowed_top_max = brect.bottom - padding - btn_h

    # If not enough room, center inside boundary
    if allowed_left_min > allowed_left_max or allowed_top_min > allowed_top_max:
        cx = brect.left + brect.width / 2
        cy = brect.top + brect.height / 2
        no.style.left = f"{int(cx)}px"
        no.style.top = f"{int(cy)}px"
        no.style.transform = "translate(-50%, -50%)"
        return

    # Forbidden rectangle around YES (expand slightly)
    extra_pad = max(12, int(min(brect.width, brect.height) * 0.04))
    yes_forbid_left = yesr.left - extra_pad
    yes_forbid_right = yesr.right + extra_pad
    yes_forbid_top = yesr.top - extra_pad
    yes_forbid_bottom = yesr.bottom + extra_pad

    # Try many random positions
    for _ in range(600):
        left_edge = random.uniform(allowed_left_min, allowed_left_max)
        top_edge  = random.uniform(allowed_top_min, allowed_top_max)
        right_edge = left_edge + btn_w
        bottom_edge = top_edge + btn_h

        # Candidate does NOT intersect YES if one of the separation conditions holds
        no_intersect = (right_edge <= yes_forbid_left or left_edge >= yes_forbid_right or
                        bottom_edge <= yes_forbid_top or top_edge >= yes_forbid_bottom)

        if no_intersect:
            # Clamp (safety) and set center coords for translate(-50%)
            left_edge = max(allowed_left_min, min(left_edge, allowed_left_max))
            top_edge  = max(allowed_top_min,  min(top_edge,  allowed_top_max))

            cx = left_edge + btn_w / 2
            cy = top_edge + btn_h / 2

            no.style.left = f"{int(cx)}px"
            no.style.top = f"{int(cy)}px"
            no.style.transform = "translate(-50%, -50%)"
            return

    # Fallback: top-left allowed corner
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

    # Position absolute inside boundary (boundary is fixed covering viewport)
    no.style.position = "absolute"
    no.style.left = f"{int(cx)}px"
    no.style.top = f"{int(cy)}px"
    no.style.transform = "translate(-50%, -50%)"
    no.style.zIndex = "10001"
    yes.style.zIndex = "10002"

    msg.text = "Dumna z siebie jesteś?"

# --- Hover/click resilience helpers ---

def clear_hover_timeout():
    global hover_timeout_id
    if hover_timeout_id is not None:
        try:
            window.clearTimeout(hover_timeout_id)
        except Exception:
            pass
        hover_timeout_id = None

def on_no_hover(ev):
    global hovering, hover_timeout_id
    if not hover_enabled or forced_under_yes or pointer_down:
        return
    hovering = True
    # small delay so user can move pointer to click without immediate escape
    clear_hover_timeout()
    hover_timeout_id = window.setTimeout(_move_if_still_hover, 140)

def _move_if_still_hover():
    global hover_timeout_id, hovering
    hover_timeout_id = None
    if hovering and hover_enabled and not forced_under_yes and not pointer_down:
        move_no_anywhere_avoiding_yes()

def on_no_out(ev):
    global hovering
    hovering = False
    clear_hover_timeout()

def on_pointer_down(ev):
    global pointer_down
    pointer_down = True
    # cancel any pending hover move so it doesn't run during press
    clear_hover_timeout()
    # temporarily disable transition to avoid weird animation while pressing
    no.style.transition = "none"

def on_pointer_up(ev):
    global pointer_down
    pointer_down = False
    # small restore delay to avoid immediate escape on quick taps
    def restore_trans():
        no.style.transition = "left 0.12s ease, top 0.12s ease"
    window.setTimeout(restore_trans, 120)

def on_no(ev):
    global scale, no_clicks, hover_enabled

    bgm = document["bgm"]
    try:
        bgm.volume = 0.1
        bgm.play()
    except Exception:
        pass

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
        # Wait a frame for text to render, then attempt to move
        window.setTimeout(move_no_anywhere_avoiding_yes, 10)

def on_yes(ev):
    bgm = document["bgm"]
    try:
        bgm.volume = 0.1
        bgm.play()
    except Exception:
        pass

    app.style.display = "none"
    final.style.display = "block"

    finalTitle.text = "Less GOOOOO!! 💘💘💘"
    finalText.text = "To randka! Widzimy się po powrocie ❤️"

    window.party()

# Bind events (including pointer events so touch also works)
no.bind("click", on_no)
no.bind("mouseover", on_no_hover)
no.bind("mouseout", on_no_out)
# pointer events for both mouse and touch
no.bind("pointerdown", on_pointer_down)
no.bind("pointerup", on_pointer_up)
# fallback for older devices
no.bind("mousedown", on_pointer_down)
no.bind("mouseup", on_pointer_up)

yes.bind("click", on_yes)

# Re-position NO on resize so mirrored start remains correct
def on_resize(ev=None):
    # If user hasn't started interaction, place mirrored; otherwise keep current behavior
    place_no_mirrored()

window.bind("resize", on_resize)

# Initial placement
set_no_text()
apply_transform()
# place mirrored once DOM is ready (allow layout)
window.setTimeout(place_no_mirrored, 10)
