#!/usr/bin/env python3
"""Deterministic WCAG contrast checker for a VSCode color theme JSON.

Usage: python3 check_contrast.py themes/<theme>.json
Reports the WCAG 2.x contrast ratio of every tokenColors foreground against
editor.background, and a few key UI text pairs. Flags code text below 4.5:1.
"""
import json
import sys
import re


def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    r, g, b = rgb
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def parse_hex(h):
    h = h.strip().lstrip("#")
    if len(h) in (8,):  # RRGGBBAA -> ignore alpha for ratio (approx over bg later)
        h = h[:6]
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    if len(h) != 6 or not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        return None
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def blend(fg_hex, bg_rgb):
    """If fg has alpha, blend it over bg."""
    h = fg_hex.strip().lstrip("#")
    rgb = parse_hex(fg_hex)
    if rgb is None:
        return None
    if len(h) == 8:
        a = int(h[6:8], 16) / 255.0
        return tuple(round(rgb[i] * a + bg_rgb[i] * (1 - a)) for i in range(3))
    return rgb


def ratio(fg_hex, bg_rgb):
    fg = blend(fg_hex, bg_rgb)
    if fg is None:
        return None
    l1, l2 = luminance(fg), luminance(bg_rgb)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def main():
    path = sys.argv[1]
    with open(path) as f:
        theme = json.load(f)
    colors = theme.get("colors", {})
    bg_hex = colors.get("editor.background", "#FFFFFF")
    bg = parse_hex(bg_hex)
    fg_hex = colors.get("editor.foreground", "#000000")
    print(f"== {theme.get('name')} ({theme.get('type')}) ==")
    print(f"editor.background = {bg_hex}  editor.foreground = {fg_hex}")
    print(f"default fg ratio = {ratio(fg_hex, bg):.2f}\n")
    print(f"{'ratio':>6}  {'AA':<4} {'hex':<10} scope")
    print("-" * 70)
    rows = []
    for tc in theme.get("tokenColors", []):
        settings = tc.get("settings", {})
        fg = settings.get("foreground")
        if not fg:
            continue
        r = ratio(fg, bg)
        if r is None:
            continue
        name = tc.get("name") or (tc.get("scope") if isinstance(tc.get("scope"), str)
                                  else ", ".join(tc.get("scope", []))[:50])
        rows.append((r, fg, name))
    rows.sort()
    fails = 0
    for r, fg, name in rows:
        ok = "OK" if r >= 4.5 else ("~3" if r >= 3.0 else "FAIL")
        if r < 4.5:
            fails += 1
        print(f"{r:6.2f}  {ok:<4} {fg:<10} {name}")
    print("-" * 70)
    print(f"{fails} token color(s) below 4.5:1 AA threshold.")

    # Key UI text pairs
    print("\n== UI text pairs ==")
    pairs = [
        ("statusBar.foreground", "statusBar.background"),
        ("activityBar.foreground", "activityBar.background"),
        ("sideBar.foreground", "sideBar.background"),
        ("tab.activeForeground", "tab.activeBackground"),
        ("tab.inactiveForeground", "tab.inactiveBackground"),
        ("titleBar.activeForeground", "titleBar.activeBackground"),
        ("editorLineNumber.foreground", "editor.background"),
        ("editorLineNumber.activeForeground", "editor.background"),
        ("terminal.foreground", "terminal.background"),
        ("button.foreground", "button.background"),
    ]
    for fk, bk in pairs:
        fv, bv = colors.get(fk), colors.get(bk)
        if not fv:
            continue
        bvr = parse_hex(bv) if bv else bg
        if bvr is None:
            bvr = bg
        r = ratio(fv, bvr)
        if r is None:
            continue
        flag = "" if r >= 3.0 else "  <-- low"
        print(f"{r:6.2f}  {fk} on {bk or 'editor.bg'}{flag}")


if __name__ == "__main__":
    main()
