#!/usr/bin/env python3
"""Build the flat, unified "Little Butter Flat" color theme from the base butter theme.

Strong cohesion: every UI surface shares ONE buttercream background and all
divider borders are removed, so the whole window reads as a single flat sheet.
Overlays (popups) get a barely-elevated tone + soft shadow so they stay legible.
Syntax candy colors and the pink interaction accents are kept unchanged.
"""
import json
import re
import collections

SRC = "themes/lggbond-butter-color-theme.json"
OUT = "themes/lggbond-flat-color-theme.json"

U = "#FCF4E2"        # the single unified surface
E = "#F7EDD3"        # barely-elevated overlay surface (popups/inputs)
PINK = "#EC6CA4"     # interaction accent

data = json.load(open(SRC, encoding="utf-8"), object_pairs_hook=collections.OrderedDict)
c = data["colors"]
data["name"] = "Little Butter Flat"

# borders to KEEP as accents (everything else *border* -> transparent)
KEEP_BORDER = {
    "focusBorder", "tab.activeBorderTop", "activityBar.activeBorder",
    "panelTitle.activeBorder", "list.focusOutline", "list.focusAndSelectionOutline",
    "inputOption.activeBorder", "checkbox.selectBorder", "menu.selectionBorder",
    "menubar.selectionBorder", "editorBracketMatch.border", "list.dropBorder",
}

# all surface backgrounds -> one unified color
SURF = [
    "editor.background", "editor.foregroundBackground", "editorGutter.background",
    "editorStickyScroll.background", "minimap.background", "breadcrumb.background",
    "panel.background", "panelSectionHeader.background", "panelSection.background",
    "terminal.background", "sideBar.background", "sideBarSectionHeader.background",
    "sideBarStickyScroll.background", "sideBarTitle.background", "activityBar.background",
    "activityBarTop.background", "statusBar.background", "titleBar.activeBackground",
    "titleBar.inactiveBackground", "editorGroupHeader.tabsBackground",
    "editorGroupHeader.noTabsBackground", "editorGroup.emptyBackground",
    "tab.activeBackground", "tab.inactiveBackground", "tab.unfocusedActiveBackground",
    "tab.unfocusedInactiveBackground", "editorPane.background", "welcomePage.background",
    "walkThrough.embeddedEditorBackground", "debugToolBar.background", "banner.background",
    "commandCenter.background", "commandCenter.activeBackground",
]
# overlay/popup/input surfaces -> barely elevated
OVER = [
    "editorWidget.background", "editorSuggestWidget.background", "editorHoverWidget.background",
    "editorStickyScrollHover.background", "peekViewEditor.background", "peekViewResult.background",
    "peekViewTitle.background", "editorMarkerNavigation.background", "quickInput.background",
    "quickInputTitle.background", "menu.background", "notifications.background",
    "notificationCenterHeader.background", "notificationToast.background", "dropdown.background",
    "dropdown.listBackground", "input.background", "checkbox.background", "keybindingTable.headerBackground",
    "settings.textInputBackground", "settings.numberInputBackground", "settings.dropdownBackground",
    "settings.checkboxBackground", "settings.focusedRowBackground", "breadcrumbPicker.background",
    "debugExceptionWidget.background", "editorActionList.background",
]

# 1) flatten divider borders
for k in list(c.keys()):
    if re.search("border", k, re.I) and k not in KEEP_BORDER:
        c[k] = "#00000000"

# 2) unify surfaces
for k in SURF:
    c[k] = U
for k in OVER:
    c[k] = E

# 3) keep pink accents crisp + uniform calm chrome text
c["tab.activeBorderTop"] = PINK
c["activityBar.activeBorder"] = PINK
c["panelTitle.activeBorder"] = PINK
c["focusBorder"] = PINK
c["tab.activeBorder"] = "#00000000"   # no underline divider
c["editorGroupHeader.border"] = "#00000000"
c["statusBar.foreground"] = "#6E5A48"
c["statusBar.border"] = "#00000000"
c["titleBar.activeForeground"] = "#6E5A48"
c["activityBar.foreground"] = "#9A3F6B"        # active icon = rose accent
c["activityBar.inactiveForeground"] = "#B29A80"
c["sideBarSectionHeader.foreground"] = "#7A6450"
# tabs/gutter share the editor bg now -> lift faint foregrounds for legibility
c["tab.inactiveForeground"] = "#8E7B60"
c["editorLineNumber.foreground"] = "#9A8666"

# 4) overlays float with a soft shadow instead of borders
c["widget.shadow"] = "#5A463626"
c["scrollbar.shadow"] = "#5A463618"
c["widget.border"] = "#00000000"

json.dump(data, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open(OUT, "a").write("\n")

# report
n_borders = sum(1 for k in c if re.search("border", k, re.I) and c[k] == "#00000000")
print(f"wrote {OUT}")
print(f"unified surface {U}; elevated overlay {E}; {n_borders} borders flattened")
print("editor.background =", c["editor.background"], "| sideBar =", c["sideBar.background"],
      "| activityBar =", c["activityBar.background"], "| statusBar =", c["statusBar.background"],
      "| titleBar =", c["titleBar.activeBackground"])
