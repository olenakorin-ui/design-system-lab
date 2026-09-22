#!/usr/bin/env python3
"""Assemble migrator-facing curated export from live Figma MCP snapshot.

Reads live schema (collections + variables) and produces the curated
figma-export.json shape expected by migrate-tokens.py.

Does not invent values — only resolves aliases and normalizes float32 alpha.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "tokens" / "_raw" / "figma-export.live.json"
OUT = ROOT / "tokens" / "_raw" / "figma-export.json"


def round_alpha(a: float | None) -> float | None:
    if a is None:
        return None
    return round(float(a), 3)


def norm_hex(h: str) -> str:
    return h.upper() if h.startswith("#") else h


def is_alias(val: dict | None) -> bool:
    if not isinstance(val, dict):
        return False
    if val.get("alias") is True:
        return True
    vid = val.get("id")
    return isinstance(vid, str) and vid.startswith("VariableID:")


def color_literal(val: dict) -> dict:
    out = {"hex": norm_hex(val["hex"])}
    if "alpha" in val and val["alpha"] is not None:
        a = round_alpha(val["alpha"])
        if a is not None and a < 0.999:
            out["alpha"] = a
    return out


# Tailwind color families — keep family on both sides of dark: recipes (blue-500-dark-blue-600).
# Other repeated stems collapse (destructive dark:destructive\70 → destructive-dark-70).
_COLOR_FAMILIES = {
    "slate",
    "gray",
    "zinc",
    "neutral",
    "stone",
    "red",
    "orange",
    "amber",
    "yellow",
    "lime",
    "green",
    "emerald",
    "teal",
    "cyan",
    "sky",
    "blue",
    "indigo",
    "violet",
    "purple",
    "fuchsia",
    "pink",
    "rose",
}


def sanitize_custom_key(figma_name: str) -> str:
    """Normalize Mode custom/* Figma names to stable short v0.4 code keys.

    Exact Figma strings stay in modeCustomFigmaNames / mappings[].figma.
    Collapses repeated semantic stems across ` dark:` (Decision custom-keys=A).
    """
    key = figma_name[7:] if figma_name.startswith("custom/") else figma_name
    key = key.replace("\\", "")
    if key.startswith("dark:"):
        return "dark-" + key[5:]
    if " dark:" not in key:
        key = key.replace(":", "-")
        return re.sub(r"([A-Za-z])(\d)", r"\1-\2", key)

    left, right = [p.strip() for p in key.split(" dark:", 1)]

    def tokenize(s: str) -> str:
        return re.sub(r"([A-Za-z])(\d)", r"\1-\2", s)

    left_t, right_t = tokenize(left), tokenize(right)
    # border dark:input-dark → border-dark-input
    if right_t.endswith("-dark") and left_t in ("border", "ring"):
        return f"{left_t}-dark-{right_t[:-5]}"
    left_parts, right_parts = left_t.split("-"), right_t.split("-")
    if left_parts[0] in _COLOR_FAMILIES and right_parts[0] in _COLOR_FAMILIES:
        return f"{left_t}-dark-{right_t}"
    if right_parts and left_parts and right_parts[0] == left_parts[0]:
        return "-".join(left_parts + ["dark"] + right_parts[1:])
    return f"{left_t}-dark-{right_t}"


def build_mode_theme_targets(idx: "LiveIndex") -> dict[str, str]:
    """Mode base/* → Theme color stem when not 1:1 (e.g. ring-offset → background)."""
    targets: dict[str, str] = {}
    for v in idx.by_col_name["3. Mode"]["variables"]:
        if not v["name"].startswith("base/"):
            continue
        name = v["name"][len("base/") :]
        light = v["valuesByMode"]["Light"]
        if not is_alias(light):
            continue
        theme_var = idx.get(light["id"])
        m = re.match(r"^colors/(.+)-light$", theme_var["name"])
        if not m:
            continue
        theme_stem = m.group(1)
        if theme_stem != name:
            targets[name] = theme_stem
    return targets


class LiveIndex:
    def __init__(self, live: dict):
        self.live = live
        self.by_id: dict[str, dict] = {}
        self.by_col_name: dict[str, dict] = {}
        for col_name, col in live["collections"].items():
            self.by_col_name[col_name] = col
            for v in col["variables"]:
                self.by_id[v["id"]] = {**v, "_collection": col_name}

    def get(self, var_id: str) -> dict:
        return self.by_id[var_id]

    def resolve(self, val: dict, mode: str | None = None, stack: tuple[str, ...] = ()) -> dict:
        """Resolve to a literal color/number/string or raise."""
        if not is_alias(val):
            if "hex" in val:
                return color_literal(val)
            if "number" in val:
                return {"number": val["number"]}
            if "string" in val:
                return {"string": val["string"]}
            raise TypeError(f"Unknown value: {val!r}")
        target = self.get(val["id"])
        if target["id"] in stack:
            raise RuntimeError(f"Alias cycle: {stack + (target['id'],)}")
        # Pick mode: prefer requested; else first mode key
        vbm = target["valuesByMode"]
        if mode and mode in vbm:
            next_val = vbm[mode]
        elif len(vbm) == 1:
            next_val = next(iter(vbm.values()))
        else:
            # Cross-collection alias into Mode: keep Light/Dark when resolving Mode customs
            if mode is None and "Default" in vbm:
                next_val = vbm["Default"]
            elif mode is None and "Light" in vbm:
                # should not happen without mode
                next_val = vbm["Light"]
            else:
                next_val = vbm.get(mode) or next(iter(vbm.values()))
        return self.resolve(next_val, mode=mode, stack=stack + (target["id"],))

    def resolve_to_primitive_ref(self, val: dict, mode: str | None = None) -> list | dict:
        """Resolve color alias chain to [family, step] or {hex,alpha}."""
        lit = self.resolve(val, mode=mode)
        if "hex" in lit:
            # Try match against known primitive by walking alias chain endpoints
            # Prefer structured ref when terminal is a tailwind color var
            terminal = self._terminal_color_var(val, mode=mode)
            if terminal and terminal["name"].startswith("tailwind colors/"):
                return self._tailwind_name_to_ref(terminal["name"])
            return lit
        raise TypeError(f"Expected color, got {lit!r}")

    def _terminal_color_var(self, val: dict, mode: str | None = None, stack: tuple[str, ...] = ()) -> dict | None:
        if not is_alias(val):
            return None
        target = self.get(val["id"])
        if target["id"] in stack:
            return None
        vbm = target["valuesByMode"]
        if mode and mode in vbm:
            next_val = vbm[mode]
        elif "Default" in vbm:
            next_val = vbm["Default"]
        else:
            next_val = next(iter(vbm.values()))
        if not is_alias(next_val):
            return target
        return self._terminal_color_var(next_val, mode=mode, stack=stack + (target["id"],))

    @staticmethod
    def _tailwind_name_to_ref(name: str) -> list:
        # tailwind colors/base/white | tailwind colors/blue/600
        path = name[len("tailwind colors/") :]
        parts = path.split("/")
        if parts[0] == "base":
            return [parts[1], None]
        return [parts[0], parts[1]]


def build_primitive_colors(idx: LiveIndex) -> dict:
    colors: dict = {}
    tw = idx.by_col_name["1. TailwindCSS"]
    for v in tw["variables"]:
        if not v["name"].startswith("tailwind colors/"):
            continue
        lit = color_literal(v["valuesByMode"]["Default"])
        path = v["name"][len("tailwind colors/") :]
        parts = path.split("/")
        if parts[0] == "base":
            colors[parts[1]] = lit
        else:
            family, step = parts[0], parts[1]
            colors.setdefault(family, {})[step] = lit
    return colors


def build_theme_colors(idx: LiveIndex) -> dict:
    out = {}
    theme = idx.by_col_name["2. Theme"]
    for v in theme["variables"]:
        if not v["name"].startswith("colors/"):
            continue
        key = v["name"][len("colors/") :]
        out[key] = idx.resolve_to_primitive_ref(v["valuesByMode"]["Default"], mode="Default")
    return out


def build_mode_base(idx: LiveIndex) -> dict:
    """Document Mode→Theme→primitive resolved refs; keys drive migrate."""
    out = {}
    mode = idx.by_col_name["3. Mode"]
    for v in mode["variables"]:
        if not v["name"].startswith("base/"):
            continue
        name = v["name"][len("base/") :]
        out[name] = {
            "Light": idx.resolve_to_primitive_ref(v["valuesByMode"]["Light"], mode="Light"),
            "Dark": idx.resolve_to_primitive_ref(v["valuesByMode"]["Dark"], mode="Dark"),
        }
    return out


def build_mode_alpha(idx: LiveIndex) -> dict:
    out = {}
    mode = idx.by_col_name["3. Mode"]
    for v in mode["variables"]:
        if not v["name"].startswith("alpha/"):
            continue
        step = v["name"][len("alpha/") :]
        out[step] = {
            "Light": color_literal(v["valuesByMode"]["Light"]),
            "Dark": color_literal(v["valuesByMode"]["Dark"]),
        }
    return out


def build_mode_custom(idx: LiveIndex) -> tuple[dict, dict]:
    recipes = {}
    names = {}
    mode = idx.by_col_name["3. Mode"]
    for v in mode["variables"]:
        if not v["name"].startswith("custom/"):
            continue
        key = sanitize_custom_key(v["name"])
        names[key] = v["name"]
        recipes[key] = {
            "Light": idx.resolve_to_primitive_ref(v["valuesByMode"]["Light"], mode="Light"),
            "Dark": idx.resolve_to_primitive_ref(v["valuesByMode"]["Dark"], mode="Dark"),
        }
    return recipes, names


def num_of(idx: LiveIndex, col: str, name: str, mode: str = "Default") -> float | int:
    v = next(x for x in idx.by_col_name[col]["variables"] if x["name"] == name)
    lit = idx.resolve(v["valuesByMode"][mode], mode=mode)
    n = lit["number"]
    return int(n) if float(n).is_integer() else n


def str_of(idx: LiveIndex, col: str, name: str, mode: str = "Default") -> str:
    v = next(x for x in idx.by_col_name[col]["variables"] if x["name"] == name)
    lit = idx.resolve(v["valuesByMode"][mode], mode=mode)
    return lit["string"]


def build_spacing(idx: LiveIndex) -> dict:
    out = {}
    for v in idx.by_col_name["1. TailwindCSS"]["variables"]:
        if not v["name"].startswith("spacing/"):
            continue
        key = v["name"][len("spacing/") :]
        n = idx.resolve(v["valuesByMode"]["Default"])["number"]
        out[key] = f"{int(n) if float(n).is_integer() else n}px"
    return out


def build_radius(idx: LiveIndex) -> dict:
    # Prefer Theme radius/* plus Tailwind none/full
    out = {"none": "0px", "full": "9999px"}
    for v in idx.by_col_name["2. Theme"]["variables"]:
        if not v["name"].startswith("radius/"):
            continue
        key = v["name"][len("radius/") :]
        n = idx.resolve(v["valuesByMode"]["Default"])["number"]
        out[key] = f"{int(n)}px"
    return out


def build_breakpoints_containers(idx: LiveIndex) -> tuple[dict, dict]:
    bp, ct = {}, {}
    for v in idx.by_col_name["2. Theme"]["variables"]:
        if v["name"].startswith("breakpoint/"):
            key = v["name"][len("breakpoint/") :]
            n = idx.resolve(v["valuesByMode"]["Default"])["number"]
            bp[key] = f"{int(n)}px"
        elif v["name"].startswith("container/"):
            key = v["name"][len("container/") :]
            n = idx.resolve(v["valuesByMode"]["Default"])["number"]
            ct[key] = f"{int(n)}px"
    return bp, ct


def build_typography(idx: LiveIndex) -> dict:
    font = {
        "sans": {"$type": "fontFamily", "$value": str_of(idx, "2. Theme", "font/font-sans")},
        "serif": {"$type": "fontFamily", "$value": str_of(idx, "2. Theme", "font/font-serif")},
        "mono": {"$type": "fontFamily", "$value": str_of(idx, "2. Theme", "font/font-mono")},
    }
    weights = {}
    for v in idx.by_col_name["2. Theme"]["variables"]:
        if v["name"].startswith("font-weight/"):
            key = v["name"][len("font-weight/") :]
            n = idx.resolve(v["valuesByMode"]["Default"])["number"]
            weights[key] = {"$type": "fontWeight", "$value": int(n)}
    text: dict = {}
    for v in idx.by_col_name["2. Theme"]["variables"]:
        m = re.match(r"^text/([^/]+)/(font-size|line-height)$", v["name"])
        if not m:
            continue
        size, prop = m.group(1), m.group(2)
        n = idx.resolve(v["valuesByMode"]["Default"])["number"]
        text.setdefault(size, {})
        key = "font-size" if prop == "font-size" else "line-height"
        text[size][key] = {"$type": "dimension", "$value": f"{int(n)}px"}

    # Custom headings — resolve aliases to concrete values
    heading: dict = {}
    custom = idx.by_col_name["4. Custom"]
    for v in custom["variables"]:
        m = re.match(r"^heading-([^/]+)/(.+)$", v["name"])
        if not m:
            continue
        size, prop = m.group(1), m.group(2)
        for mode_name, mode_key in [("Desktop", "desktop"), ("Mobile", "mobile")]:
            lit = idx.resolve(v["valuesByMode"][mode_name], mode=mode_name)
            bucket = heading.setdefault(size, {}).setdefault(mode_key, {})
            if prop == "font-family":
                bucket[prop] = {"$type": "fontFamily", "$value": lit["string"]}
            elif prop == "font-weight":
                bucket[prop] = {"$type": "fontWeight", "$value": int(lit["number"])}
            else:
                n = lit["number"]
                bucket[prop] = {"$type": "dimension", "$value": f"{int(n) if float(n).is_integer() else n}px"}

    return {
        "meta": {
            "name": "Design System V2 Typography Tokens",
            "version": "0.4.0",
            "source": "live Figma MCP export",
            "collection": "2. Theme / font + text, 4. Custom headings",
        },
        "font": font,
        "font-weight": weights,
        "text": text,
        "heading": heading,
    }


def build_shadow(idx: LiveIndex) -> dict:
    def rgba(lit: dict) -> str:
        h = lit["hex"].lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        a = lit.get("alpha", 1)
        if a is None or a >= 0.999:
            return f"rgb({r},{g},{b})"
        return f"rgba({r},{g},{b},{a})"

    def layer(prefix: str) -> dict:
        ox = num_of(idx, "2. Theme", f"{prefix}/offset-x")
        oy = num_of(idx, "2. Theme", f"{prefix}/offset-y")
        blur = num_of(idx, "2. Theme", f"{prefix}/blur-radius")
        spread = num_of(idx, "2. Theme", f"{prefix}/spread-radius")
        color_v = next(
            x for x in idx.by_col_name["2. Theme"]["variables"] if x["name"] == f"{prefix}/color"
        )
        color = rgba(color_literal(color_v["valuesByMode"]["Default"]))
        return {
            "$type": "shadow",
            "$value": {
                "offsetX": ox,
                "offsetY": oy,
                "blur": blur,
                "spread": spread,
                "color": color,
            },
        }

    # Discover shadow names from Theme vars
    names: set[str] = set()
    layered: dict[str, set[str]] = {}
    for v in idx.by_col_name["2. Theme"]["variables"]:
        m = re.match(r"^shadow/([^/]+)/(\d+)/", v["name"])
        if m:
            layered.setdefault(m.group(1), set()).add(m.group(2))
            continue
        m = re.match(r"^shadow/([^/]+)/", v["name"])
        if m:
            names.add(m.group(1))

    shadow = {}
    for name in sorted(names | set(layered)):
        if name in layered:
            shadow[name] = [layer(f"shadow/{name}/{i}") for i in sorted(layered[name], key=int)]
        else:
            shadow[name] = [layer(f"shadow/{name}")]

    blur = {}
    for v in idx.by_col_name["2. Theme"]["variables"]:
        if v["name"].startswith("blur/"):
            key = v["name"][len("blur/") :]
            n = idx.resolve(v["valuesByMode"]["Default"])["number"]
            blur[key] = {"$type": "dimension", "$value": f"{int(n)}px"}

    return {
        "meta": {
            "name": "Design System V2 Shadow Tokens",
            "version": "0.4.0",
            "source": "live Figma MCP export",
            "collection": "2. Theme / shadow",
        },
        "shadow": shadow,
        "blur": blur,
    }


def build_layout(idx: LiveIndex) -> dict:
    out = {}
    custom = idx.by_col_name["4. Custom"]
    for v in custom["variables"]:
        if v["name"].startswith("heading-"):
            continue
        key = v["name"]
        modes = {}
        for mode_name, mode_key in [("Desktop", "desktop"), ("Mobile", "mobile")]:
            lit = idx.resolve(v["valuesByMode"][mode_name], mode=mode_name)
            n = lit["number"]
            modes[mode_key] = {"$type": "dimension", "$value": f"{int(n)}px"}
        out[key] = modes
    return out


def assemble(live: dict) -> dict:
    idx = LiveIndex(live)
    theme_colors = build_theme_colors(idx)
    mode_base = build_mode_base(idx)
    mode_theme_targets = build_mode_theme_targets(idx)
    mode_custom, mode_custom_names = build_mode_custom(idx)
    mode_alpha = build_mode_alpha(idx)
    bp, containers = build_breakpoints_containers(idx)
    primitives = build_primitive_colors(idx)
    # Convenience alias retained for CSS consumers (not a Figma variable).
    if "white" in primitives and "neutral" in primitives and "0" not in primitives["neutral"]:
        primitives["neutral"]["0"] = dict(primitives["white"])

    collections_meta = {}
    for key, figma_name in [
        ("tailwind", "1. TailwindCSS"),
        ("theme", "2. Theme"),
        ("mode", "3. Mode"),
        ("custom", "4. Custom"),
    ]:
        col = live["collections"][figma_name]
        collections_meta[key] = {
            "name": figma_name,
            "id": col["id"],
            "modes": [m["name"] for m in col["modes"]],
            "variableCount": col["variableCount"],
        }

    return {
        "meta": {
            "fileKey": live["fileKey"],
            "source": f"https://www.figma.com/design/{live['fileKey']}/Design-System-V2",
            "extractedAt": live["extractedAt"],
            "assembledFrom": "live Figma MCP read-only export (figma-export.live.json)",
            "textStyleCount": live["textStyleCount"],
            "effectStyleCount": live["effectStyleCount"],
            "totalVariables": live["totalVariables"],
            "decisions": {
                "1": "A",
                "2": "B",
                "3": "B",
                "4": "A",
                "ringOffset": "A",
                "customKeys": "A",
            },
        },
        "collections": collections_meta,
        "primitiveColors": primitives,
        "modeBase": mode_base,
        "modeBaseThemeTargets": mode_theme_targets,
        "modeCustom": mode_custom,
        "modeCustomFigmaNames": mode_custom_names,
        "modeAlpha": mode_alpha,
        "spacing": build_spacing(idx),
        "breakpoints": bp,
        "containers": containers,
        "layout": build_layout(idx),
        "radius": build_radius(idx),
        "typography": build_typography(idx),
        "shadow": build_shadow(idx),
        "themeColors": theme_colors,
        "live": {
            "note": "Canonical full variable inventory is tokens/_raw/figma-export.live.json",
            "variableCounts": {k: v["variableCount"] for k, v in collections_meta.items()},
        },
    }


def main() -> None:
    live = json.loads(LIVE.read_text(encoding="utf-8"))
    assert live["totalVariables"] == 760, live["totalVariables"]
    curated = assemble(live)
    OUT.write_text(json.dumps(curated, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "wrote": str(OUT.relative_to(ROOT)),
                "extractedAt": curated["meta"]["extractedAt"],
                "themeColors": len(curated["themeColors"]),
                "modeBase": len(curated["modeBase"]),
                "modeCustom": len(curated["modeCustom"]),
                "primitiveFamilies": len(curated["primitiveColors"]),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
