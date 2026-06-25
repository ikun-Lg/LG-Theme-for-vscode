#!/usr/bin/env python3
"""Generate the "Little Butter" File Icon Themes — two styles from one mapping:

  - tile : cute rounded color-coded tiles with white/cocoa labels
  - min  : minimalist, NO background — just the family-colored glyph/label,
           flat butter folders, thin-outline default file & image.

Deterministic so each set stays visually consistent. Validates every mapping.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _lum(hex_):
    h = hex_.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def _ratio(a, b):
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def label_color(fill):
    return "#FFFDF7" if _ratio("#FFFDF7", fill) >= _ratio("#4A3526", fill) else "#4A3526"


FAMILY = {
    "js": "#C9972B", "ts": "#2A78B5", "web": "#C84B34", "style": "#C93A72",
    "data": "#8344C2", "doc": "#6B5544", "python": "#2D80C0", "shell": "#1F8A52",
    "systems": "#B5551E", "jvm": "#C8503A", "config": "#9A7418", "image": "#2E9E6A",
    "data2": "#1F7E5F", "gray": "#8C7D6D", "archive": "#8743A6",
}

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif"


# ---------- TILE style ----------
def tile_svg(label, fill):
    fs, y = (18, 22) if len(label) == 1 else (14.5, 21) if len(label) == 2 else (10.5, 20)
    tc = label_color(fill)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">'
            f'<rect x="3" y="4" width="26" height="24" rx="6.5" fill="{fill}"/>'
            f'<text x="16" y="{y}" text-anchor="middle" font-family="{FONT}" font-weight="700" '
            f'font-size="{fs}" letter-spacing="-0.4" fill="{tc}">{label}</text></svg>')


TILE_SHAPES = {
    "folder": ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">'
               '<path d="M3.5 8.5a2 2 0 0 1 2-2h6.2a2 2 0 0 1 1.5.7l1.5 1.8H26.5a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-21a2 2 0 0 1-2-2z" fill="#EFC152"/>'
               '<path d="M3.5 12.5h25v9.5a2 2 0 0 1-2 2h-21a2 2 0 0 1-2-2z" fill="#F6D277"/>'
               '<circle cx="24" cy="11.5" r="1.4" fill="#FBE9B0"/></svg>'),
    "folder_open": ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">'
                    '<path d="M3.5 8.5a2 2 0 0 1 2-2h6.2a2 2 0 0 1 1.5.7l1.5 1.8H26.5a2 2 0 0 1 2 2v3H3.5z" fill="#EFC152"/>'
                    '<path d="M6 13h24.5l-3 9.4a2 2 0 0 1-1.9 1.4H4.4a1.4 1.4 0 0 1-1.35-1.8l2.6-8a1.4 1.4 0 0 1 1.35-1z" fill="#FBE2A8"/>'
                    '<path d="M6 13h22l-.6 1.8H5.4z" fill="#F7D070"/><circle cx="25" cy="10.5" r="1.4" fill="#FBE9B0"/></svg>'),
    "file": ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">'
             '<path d="M8 4.5h10.5L25 11v15.5a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V6.5a2 2 0 0 1 2-2z" fill="#FBEFCE" stroke="#E2CFA0" stroke-width="1.1"/>'
             '<path d="M18.3 4.7v5a1.2 1.2 0 0 0 1.2 1.2h4.8z" fill="#EAD9A0"/>'
             '<rect x="10.5" y="15" width="10" height="1.7" rx="0.85" fill="#CBB68A"/>'
             '<rect x="10.5" y="18.8" width="8" height="1.7" rx="0.85" fill="#CBB68A"/>'
             '<rect x="10.5" y="22.6" width="6" height="1.7" rx="0.85" fill="#CBB68A"/></svg>'),
    "img": ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">'
            f'<rect x="3" y="4" width="26" height="24" rx="6.5" fill="{FAMILY["image"]}"/>'
            '<circle cx="12" cy="12" r="2.6" fill="#FFFDF7"/>'
            '<path d="M6.5 24l5.5-7 3.3 4 3.7-5.5L25.5 24z" fill="#FFFDF7"/></svg>'),
}


# ---------- MINIMAL style (no background) ----------
def min_svg(label, fill):
    fs, y = (21, 23) if len(label) == 1 else (17, 22) if len(label) == 2 else (12.5, 21)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">'
            f'<text x="16" y="{y}" text-anchor="middle" font-family="{FONT}" font-weight="700" '
            f'font-size="{fs}" letter-spacing="-0.5" fill="{fill}">{label}</text></svg>')


MIN_SHAPES = {
    "folder": ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">'
               '<path d="M3.5 8.5a2 2 0 0 1 2-2h6.2a2 2 0 0 1 1.5.7l1.5 1.8H26.5a2 2 0 0 1 2 2v11.5a2 2 0 0 1-2 2h-21a2 2 0 0 1-2-2z" fill="#EFC152"/></svg>'),
    "folder_open": ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">'
                    '<path d="M3.5 8.5a2 2 0 0 1 2-2h6.2a2 2 0 0 1 1.5.7l1.5 1.8H26.5a2 2 0 0 1 2 2v2H3.5z" fill="#E8B84A"/>'
                    '<path d="M3.5 12.2h25l-2.5 9.4a2 2 0 0 1-1.93 1.48H5.5a2 2 0 0 1-2-2z" fill="#F4CF6B"/></svg>'),
    "file": ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">'
             '<path d="M8 4.8h10.2L24.5 11v15.2a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V6.8a2 2 0 0 1 2-2z" fill="none" stroke="#AC9A82" stroke-width="1.7"/>'
             '<path d="M18 5.2v5a1.2 1.2 0 0 0 1.2 1.2h4.6" fill="none" stroke="#AC9A82" stroke-width="1.7" stroke-linejoin="round"/></svg>'),
    "img": ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">'
            f'<rect x="4.5" y="6.5" width="23" height="19" rx="3" fill="none" stroke="{FAMILY["image"]}" stroke-width="1.8"/>'
            f'<circle cx="11.5" cy="13" r="2" fill="{FAMILY["image"]}"/>'
            f'<path d="M6 24.5l6.5-7 3.5 4 4-5.5L27 24.5" fill="none" stroke="{FAMILY["image"]}" stroke-width="1.8" stroke-linejoin="round"/></svg>'),
}

# (family, label, [extensions], [filenames], [languageIds])
DEFS = [
    ("js", "JS", ["js", "mjs", "cjs"], [], ["javascript"]),
    ("web", "JSX", ["jsx"], [], ["javascriptreact"]),
    ("ts", "TS", ["ts", "mts", "cts"], ["tsconfig.json"], ["typescript"]),
    ("web", "TSX", ["tsx"], [], ["typescriptreact"]),
    ("data", "{}", ["json", "jsonc", "json5"], [], ["json", "jsonc"]),
    ("web", "<>", ["html", "htm", "xhtml"], [], ["html"]),
    ("web", "V", ["vue"], [], ["vue"]),
    ("web", "SV", ["svelte"], [], []),
    ("web", "AS", ["astro"], [], []),
    ("style", "#", ["css"], [], ["css"]),
    ("style", "S", ["scss", "sass"], [], ["scss", "sass"]),
    ("style", "L", ["less"], [], ["less"]),
    ("style", "TW", [], ["tailwind.config.js", "tailwind.config.ts"], []),
    ("style", "GQL", ["graphql", "gql"], [], []),
    ("doc", "md", ["md", "markdown", "mdx"], ["README.md", "README"], ["markdown"]),
    ("gray", "TXT", ["txt", "text", "log"], [], ["plaintext"]),
    ("doc", "DOC", ["pdf", "rst", "adoc", "doc", "docx"], [], []),
    ("doc", "©", [], ["LICENSE", "LICENSE.md", "LICENCE", "COPYING"], []),
    ("python", "PY", ["py", "pyw", "pyi"], [], ["python"]),
    ("python", "IPY", ["ipynb"], [], []),
    ("systems", "GO", ["go"], [], ["go"]),
    ("systems", "RS", ["rs"], [], ["rust"]),
    ("systems", "C", ["c", "h"], [], ["c"]),
    ("systems", "C+", ["cpp", "cc", "cxx", "hpp", "hh"], [], ["cpp"]),
    ("archive", "C#", ["cs"], [], ["csharp"]),
    ("jvm", "JV", ["java"], [], ["java"]),
    ("jvm", "KT", ["kt", "kts"], [], ["kotlin"]),
    ("jvm", "SC", ["scala"], [], []),
    ("jvm", "RB", ["rb"], ["Gemfile", "Rakefile"], ["ruby"]),
    ("archive", "PHP", ["php"], [], ["php"]),
    ("systems", "SW", ["swift"], [], ["swift"]),
    ("ts", "DT", ["dart"], [], ["dart"]),
    ("data", "LUA", ["lua"], [], ["lua"]),
    ("ts", "R", ["r"], [], []),
    ("archive", "EX", ["ex", "exs"], [], []),
    ("shell", "CLJ", ["clj", "cljs", "cljc"], [], []),
    ("config", "PL", ["pl", "pm"], [], ["perl"]),
    ("data2", "SQL", ["sql"], [], ["sql"]),
    ("data2", "DB", ["db", "sqlite", "sqlite3"], [], []),
    ("data", "PB", ["proto"], [], []),
    ("config", "Y", ["yaml", "yml"], [], ["yaml"]),
    ("config", "TM", ["toml"], [], ["toml"]),
    ("config", "CF", ["ini", "cfg", "conf", "properties"], [".npmrc", ".nvmrc", ".editorconfig"], []),
    ("web", "XML", ["xml", "plist", "xaml"], [], ["xml"]),
    ("data2", "CSV", ["csv", "tsv"], [], []),
    ("shell", ">_", ["sh", "bash", "zsh", "fish"], [], ["shellscript"]),
    ("shell", "PS", ["ps1", "psm1"], [], ["powershell"]),
    ("shell", "BAT", ["bat", "cmd"], [], ["bat"]),
    ("config", "DK", ["dockerfile"], ["Dockerfile", "dockerfile", ".dockerignore", "docker-compose.yml", "docker-compose.yaml"], ["dockerfile"]),
    ("config", "MK", ["mk", "mak"], ["Makefile", "makefile", "GNUmakefile"], ["makefile"]),
    ("config", "ENV", ["env"], [".env", ".env.local", ".env.development", ".env.production", ".env.test"], []),
    ("config", "ES", [], [".eslintrc", ".eslintrc.json", ".eslintrc.js", ".eslintrc.cjs", "eslint.config.js", "eslint.config.mjs"], []),
    ("config", "PR", [], [".prettierrc", ".prettierrc.json", ".prettierrc.js", "prettier.config.js"], []),
    ("config", "BB", [], [".babelrc", "babel.config.js", "babel.config.json"], []),
    ("config", "VT", [], ["vite.config.js", "vite.config.ts", "vite.config.mjs"], []),
    ("config", "RU", [], ["rollup.config.js", "rollup.config.mjs", "rollup.config.ts"], []),
    ("config", "WP", [], ["webpack.config.js", "webpack.config.ts"], []),
    ("style", "npm", [], ["package.json"], []),
    ("gray", "LK", ["lock"], ["package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb", "composer.lock", "Cargo.lock", "poetry.lock"], []),
    ("web", "git", ["gitignore", "gitattributes", "gitmodules"], [".gitignore", ".gitattributes", ".gitmodules", ".gitkeep", ".vscodeignore"], []),
    ("image", "_img", ["png", "jpg", "jpeg", "gif", "webp", "bmp", "ico", "avif", "tiff"], [], []),
    ("image", "SVG", ["svg"], [], []),
    ("archive", "VID", ["mp4", "mov", "webm", "avi", "mkv"], [], []),
    ("archive", "AUD", ["mp3", "wav", "flac", "ogg", "m4a"], [], []),
    ("gray", "FNT", ["ttf", "otf", "woff", "woff2", "eot"], [], []),
    ("archive", "ZIP", ["zip", "tar", "gz", "tgz", "rar", "7z", "bz2", "xz"], [], []),
    ("archive", "VSX", ["vsix"], [], []),
    ("gray", "BIN", ["exe", "dll", "bin", "so", "dylib", "o", "a"], [], []),
]


def key_for(family, label):
    safe = re.sub(r"[^a-zA-Z0-9]", "_", label).strip("_") or "sym"
    return f"_{family}_{safe}"


def build(subdir, theme_path, svg_fn, shapes):
    icondir = os.path.join(ROOT, "fileicons", subdir)
    os.makedirs(icondir, exist_ok=True)
    # clear stale svgs
    for fn in os.listdir(icondir):
        if fn.endswith(".svg"):
            os.remove(os.path.join(icondir, fn))

    icon_defs, file_exts, file_names, lang_ids = {}, {}, {}, {}
    for k, svg in shapes.items():
        fn = {"folder": "folder", "folder_open": "folder-open", "file": "file", "img": "img"}[k]
        open(os.path.join(icondir, fn + ".svg"), "w").write(svg)
        icon_defs["_" + ({"folder": "folder", "folder_open": "folder_open", "file": "file", "img": "img"}[k])] = {"iconPath": f"./{subdir}/{fn}.svg"}

    generated = set()
    for family, label, exts, names, langs in DEFS:
        if label == "_img":
            ikey = "_img"
        else:
            ikey = key_for(family, label)
            if ikey not in generated:
                open(os.path.join(icondir, ikey.lstrip("_") + ".svg"), "w").write(svg_fn(label, FAMILY[family]))
                icon_defs[ikey] = {"iconPath": f"./{subdir}/{ikey.lstrip('_')}.svg"}
                generated.add(ikey)
        for e in exts:
            file_exts[e] = ikey
        for n in names:
            file_names[n] = ikey
        for lg in langs:
            lang_ids[lg] = ikey

    theme = {
        "hidesExplorerArrows": False,
        "iconDefinitions": icon_defs,
        "file": "_file", "folder": "_folder", "folderExpanded": "_folder_open",
        "rootFolder": "_folder", "rootFolderExpanded": "_folder_open",
        "fileExtensions": file_exts, "fileNames": file_names, "languageIds": lang_ids,
    }
    json.dump(theme, open(theme_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    open(theme_path, "a").write("\n")

    errors = []
    for key, d in icon_defs.items():
        if not os.path.exists(os.path.join(ROOT, "fileicons", d["iconPath"].lstrip("./"))):
            errors.append(f"missing icon for {key}")
    for mp in (file_exts, file_names, lang_ids):
        for k, v in mp.items():
            if v not in icon_defs:
                errors.append(f"{k} -> {v} unmapped")
    print(f"[{subdir}] {len(os.listdir(icondir))} svgs | defs {len(icon_defs)} | ext {len(file_exts)} | names {len(file_names)} | langs {len(lang_ids)} | errors: {errors or 'none'}")


build("icons", os.path.join(ROOT, "fileicons", "lggbond-icon-theme.json"), tile_svg, TILE_SHAPES)
build("icons-min", os.path.join(ROOT, "fileicons", "lggbond-icon-theme-min.json"), min_svg, MIN_SHAPES)
print("done.")
