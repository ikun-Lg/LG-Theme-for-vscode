#!/usr/bin/env python3
"""Build the cute "Little Butter (小黄油)" theme by recoloring the Sunflower light theme.

Unified RGB-level hex remap (alpha preserved) recolors BOTH syntax tokens and the
UI chrome at once, because Sunflower reuses syntax hexes for semantic UI colors.
Cream -> buttercream, soft gold -> candy pink, warm syntax -> deep-candy pastels.
"""
import json
import re
import collections

SRC = "themes/lggbond-color-theme.json"
OUT = "themes/lggbond-butter-color-theme.json"

# old RRGGBB (upper) -> new RRGGBB. Alpha suffix is preserved automatically.
HEX_MAP = {
    # ---- backgrounds: warm cream -> buttercream ----
    "FBF7EC": "FCF4E2",  # editor bg
    "FAF5E6": "FBF2DD",  # inputs
    "F7F1E2": "FBF1DB",  # sidebar
    "F4EEDD": "F8EDD2",  # tabs inactive / group header
    "F2EBD9": "F6EAC B".replace(" ", ""),  # activity/status bar
    "FBF3DE": "FBEFDA",  # widgets / hover / suggest / peek / menu
    "FFFDF6": "FFFDF4",  # near-white fg-on-accent
    "EFE7D3": "F3E7CC",  # secondary button
    "F0E8D5": "F4E8CD",  # inactive selection
    "EDE6D5": "F0E5CC",  # indent guide / ruler
    "FBEFD8": "FDEBD0",  # warning bg
    # ---- borders / neutrals (warm) -> soft warm ----
    "E8E0CE": "EFE0C6",
    "E6DCC2": "EFE0C6",
    "D8CDB4": "E6D6B8",
    "DCD3BE": "E8DBBE",
    "C2B8A2": "D6C7AC",
    "A2937C": "BBA88C",
    # ---- selection/list highlight: pale gold -> soft pink ----
    "F5ECD7": "FBE2EC",
    # ---- soft-gold accent family -> candy pink ----
    "E0A526": "EC6CA4",  # primary accent: cursor, focus, borders, badge, button, active border
    "EBC056": "F296BE",  # hover / mid (selection tint becomes soft pink)
    "F0D596": "F8C9DE",  # light tint
    "D9C488": "EBB9CE",  # secondary border
    "EFE0B4": "FAE0EA",  # title bar slab -> soft pink (overridden below for fg too)
    # ---- warm UI text (cocoa/taupe) -> slightly softer warm ----
    "4A3F35": "6E6258",  # editor.foreground / variable
    "3A3026": "574A42",  # strong fg / text-on-accent
    "5A4F42": "7A6A60",
    "6E6150": "8A7468",
    "908462": "AC9678",
    "8A7E6E": "AC9A86",
    "7A6E5C": "9A8978",
    "7E7260": "9A8978",
    "847660": "9E8C7C",
    "908264": "AC9678",
    "847458": "9E8C7C",  # doc comment
    "82735C": "94807B",  # comment
    "7E7257": "9A8978",
    "968A74": "AC9A86",
    "A2937C2": "x",  # (noop guard)
    # ---- syntax hues -> deep candy ----
    "5F7320": "23824F",  # string / green added
    "AD4318": "C93A72",  # keyword / control / md bold
    "A8521F": "B05530",  # storage / md italic
    "94660C": "947014",  # function / md heading / ansi yellow
    "8C6800": "8C6A1C",  # builtin func / md link
    "7E5A12": "8C6A1C",  # css class selector
    "1E6F73": "8344C2",  # type / class / info / inlay type
    "257175": "8D55C6",  # inherited / type param
    "863A66": "B5551E",  # number / css color / md inline code
    "9C3A5A": "A33E8A",  # constant / language / enum / units
    "6E4A8C": "8743A6",  # decorator / pseudo / macro / ai-lightbulb
    "BF4A2E": "C84B34",  # tag / css tag selector
    "386580": "2A78B5",  # property / json/yaml key / shell var / blue
    "74604C": "7C6D5F",  # operator
    "756A58": "8C7D6D",  # punctuation
    "8A5C40": "B25468",  # parameter / this / attribute / label (dusty rose)
    "46735A": "1F7E5F",  # regex
    "C62828": "C93A36",  # error / invalid / deleted
    "B5481F": "B5551E",  # warning -> peach
    "A8740F": "B5551E",  # modified gutter -> peach
    "97660C": "947014",  # md changed
    "689F38": "23824F",
}
HEX_MAP = {k: v for k, v in HEX_MAP.items() if len(v) == 6 and re.fullmatch(r"[0-9A-Fa-f]{6}", v)}

HEX_RE = re.compile(r"^#([0-9A-Fa-f]{6})([0-9A-Fa-f]{2})?$")


def remap(v):
    if not isinstance(v, str):
        return v
    m = HEX_RE.match(v)
    if not m:
        return v
    rgb = m.group(1).upper()
    alpha = m.group(2) or ""
    if rgb in HEX_MAP:
        return "#" + HEX_MAP[rgb] + alpha
    return v


data = json.load(open(SRC, encoding="utf-8"), object_pairs_hook=collections.OrderedDict)
data["name"] = "Little Butter"

# recolor UI
for k, v in list(data["colors"].items()):
    data["colors"][k] = remap(v)

# recolor token foregrounds
for tc in data["tokenColors"]:
    s = tc.get("settings", {})
    if "foreground" in s:
        s["foreground"] = remap(s["foreground"])

# recolor semantic tokens
sem = data.get("semanticTokenColors", {})
for k, v in list(sem.items()):
    if isinstance(v, str):
        sem[k] = remap(v)
    elif isinstance(v, dict) and "foreground" in v:
        v["foreground"] = remap(v["foreground"])

# ---- cute-specific explicit overrides ----
ov = {
    "editor.background": "#FCF4E2",
    "editor.lineHighlightBackground": "#FCEEF2",   # soft pink current-line
    "editor.lineHighlightBorder": "#00000000",
    "editor.rangeHighlightBackground": "#FCEEF2",
    "editorCursor.foreground": "#EC6CA4",
    "titleBar.activeBackground": "#FAE0EA",
    "titleBar.activeForeground": "#A65C78",
    "titleBar.inactiveBackground": "#FBF1DB",
    "titleBar.inactiveForeground": "#BBA88C",
    "titleBar.border": "#F2D6DF",
    "statusBar.background": "#FAE0EA",
    "statusBar.foreground": "#A65C78",
    "statusBar.border": "#F2D6DF",
    "activityBar.background": "#FBE7C9",
    "activityBar.foreground": "#A65C78",
    "activityBarBadge.background": "#EC6CA4",
    "activityBarBadge.foreground": "#FFF6FA",
    "badge.background": "#EC6CA4",
    "badge.foreground": "#FFF6FA",
    "button.foreground": "#FFF6FA",
    "button.background": "#EC6CA4",
    "button.hoverBackground": "#F07FB1",
    "sideBar.background": "#FBF1DB",
}
for k, v in ov.items():
    if k in data["colors"]:
        data["colors"][k] = v
    else:
        data["colors"][k] = v

json.dump(data, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open(OUT, "a", encoding="utf-8").write("\n")
print("wrote", OUT)

# report any leftover saturated warm-gold (potential missed mapping)
import colorsys
def hsl(h):
    h = h.lstrip("#")[:6]
    r, g, b = (int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    return hh * 360, s * 100, l * 100
leftover = []
for k, v in data["colors"].items():
    m = HEX_RE.match(v) if isinstance(v, str) else None
    if not m:
        continue
    H, S, L = hsl(v)
    if 38 <= H <= 55 and S >= 55 and L <= 60:
        leftover.append((k, v))
print("leftover saturated golds:", len(leftover))
for k, v in leftover[:15]:
    print("  ", v, k)
