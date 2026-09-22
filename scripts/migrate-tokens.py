#!/usr/bin/env python3
"""Migrate Design System V2 tokens into three-tier repo structure.

Reads:  tokens/_raw/figma-export.json
Writes: tokens/{meta,primitive,theme,semantic,custom,mappings}/...
        src/styles/tokens.css (GENERATED)
        tokens/_validation-report.json

Decisions: 1=A (Figma blue/neutral), 2=B (no lab-only semantics),
           3=B (normalize + mappings), 4=A (Tailwind → Theme → Mode).
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "tokens" / "_raw" / "figma-export.json"
TOKENS = ROOT / "tokens"
CSS_OUT = ROOT / "src" / "styles" / "tokens.css"

# Lab-only names that must NOT appear in production semantic set (Decision 2=B)
LAB_ONLY_FORBIDDEN = {
    "success",
    "success-foreground",
    "success-subtle",
    "success-subtle-foreground",
    "warning",
    "warning-foreground",
    "warning-subtle",
    "warning-subtle-foreground",
    "info",
    "info-foreground",
    "info-subtle",
    "info-subtle-foreground",
    "error-subtle",
    "error-subtle-foreground",
    "border-strong",
    "surface-raised",
    "surface-sunken",
    "focus-ring",
    "brand",
}


def dump(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def dim(px_str: str) -> dict:
    """Convert '16px' or number-like string to DTCG dimension."""
    if isinstance(px_str, (int, float)):
        return {"$type": "dimension", "$value": f"{px_str}px"}
    return {"$type": "dimension", "$value": px_str}


def color_token(hex_value: str, alpha: float | None = None) -> dict:
    tok: dict = {"$type": "color", "$value": hex_value.upper() if hex_value.startswith("#") else hex_value}
    if alpha is not None:
        tok["alpha"] = alpha
    return tok


def alias(path: str, type_name: str = "color") -> dict:
    return {"$type": type_name, "$value": f"{{{path}}}"}


def ref_to_alias(ref, prefix: str = "primitive.color") -> dict:
    """Convert export ref tuple/list/dict to token alias or literal color."""
    if isinstance(ref, dict) and "hex" in ref:
        return color_token(ref["hex"], ref.get("alpha"))
    if isinstance(ref, (tuple, list)) and len(ref) == 2:
        family, step = ref
        if step is None:
            if family == "white":
                return alias(f"{prefix}.white")
            if family == "black":
                return alias(f"{prefix}.black")
            return alias(f"{prefix}.{family}")
        return alias(f"{prefix}.{family}.{step}")
    raise TypeError(f"Unknown ref: {ref!r}")


def css_name_from_path(path: str) -> str:
    """Normalize token path to CSS custom property name."""
    return "--" + path.replace(".", "-").replace("/", "-").replace(" ", "-").lower()


def sanitize_key(name: str) -> str:
    """Normalize Figma path segment for code keys."""
    name = name.replace("tailwind colors/", "")
    name = name.replace("border-radius/rounded-", "rounded.")
    name = name.replace("border-width/border", "border-width.")
    name = name.replace("max-width/max-w-", "max-width.")
    name = name.replace("opacity/opacity-", "opacity.")
    name = name.replace("\\", "-")
    name = re.sub(r"[^a-zA-Z0-9._-]+", "-", name)
    name = re.sub(r"-+", "-", name).strip("-")
    return name


def build_primitive_color(export: dict) -> tuple[dict, list[dict]]:
    mappings = []
    tree: dict = {
        "$description": "Figma collection 1. TailwindCSS — color primitives (normalized)",
    }
    colors = export["primitiveColors"]
    for family, scale in colors.items():
        figma_prefix = (
            f"tailwind colors/base/{family}"
            if family in ("white", "black", "transparent")
            else f"tailwind colors/{family}"
        )
        if family in ("white", "black", "transparent"):
            tree[family] = color_token(scale["hex"], scale.get("alpha"))
            mappings.append(
                {
                    "figma": figma_prefix if family != "transparent" else "tailwind colors/base/transparent",
                    "figmaCollection": "1. TailwindCSS",
                    "codePath": f"primitive.color.{family}",
                    "cssVar": css_name_from_path(f"color.{family}"),
                    "tier": "primitive",
                }
            )
            continue
        tree[family] = {}
        for step, entry in scale.items():
            if step == "0" and family == "neutral":
                # convenience mirror of white — map explicitly
                tree[family][step] = color_token(entry["hex"], entry.get("alpha"))
                mappings.append(
                    {
                        "figma": "tailwind colors/base/white",
                        "figmaCollection": "1. TailwindCSS",
                        "codePath": f"primitive.color.neutral.0",
                        "cssVar": css_name_from_path(f"color.neutral.0"),
                        "tier": "primitive",
                        "note": "normalized convenience alias of white",
                    }
                )
                continue
            tree[family][step] = color_token(entry["hex"], entry.get("alpha"))
            mappings.append(
                {
                    "figma": f"tailwind colors/{family}/{step}",
                    "figmaCollection": "1. TailwindCSS",
                    "codePath": f"primitive.color.{family}.{step}",
                    "cssVar": css_name_from_path(f"color.{family}.{step}"),
                    "tier": "primitive",
                }
            )
    return {"meta": {"tier": "primitive", "figmaCollection": "1. TailwindCSS"}, **tree}, mappings


def build_primitive_dimension(export: dict) -> tuple[dict, list[dict]]:
    mappings = []
    spacing = {k: dim(v if str(v).endswith("px") else f"{v}px" if v != 0 and not str(v).endswith("px") else ("0px" if v == 0 or v == "0px" else v)) for k, v in export["spacing"].items()}
    # normalize spacing values
    space_out = {}
    for k, v in export["spacing"].items():
        num = int(str(v).replace("px", "")) if not isinstance(v, int) else v
        space_out[k] = {"$type": "dimension", "$value": f"{num}px"}
        mappings.append(
            {
                "figma": f"spacing/{k}",
                "figmaCollection": "1. TailwindCSS",
                "codePath": f"primitive.dimension.spacing.{k}",
                "cssVar": css_name_from_path(f"spacing.{k}"),
                "tier": "primitive",
            }
        )

    # Known Tailwind utility scales from discovery (not all in old JSON)
    opacity = {str(n): {"$type": "number", "$value": n} for n in [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]}
    for k in opacity:
        mappings.append(
            {
                "figma": f"opacity/opacity-{k}",
                "figmaCollection": "1. TailwindCSS",
                "codePath": f"primitive.dimension.opacity.{k}",
                "cssVar": css_name_from_path(f"opacity.{k}"),
                "tier": "primitive",
            }
        )

    border_width = {
        "0": {"$type": "dimension", "$value": "0px"},
        "DEFAULT": {"$type": "dimension", "$value": "1px"},
        "2": {"$type": "dimension", "$value": "2px"},
        "4": {"$type": "dimension", "$value": "4px"},
        "8": {"$type": "dimension", "$value": "8px"},
    }
    for k, tok in border_width.items():
        figma = "border-width/border" if k == "DEFAULT" else f"border-width/border-{k}" if k != "0" else "border-width/border-0"
        if k == "0":
            figma = "border-width/border-0"
        mappings.append(
            {
                "figma": figma,
                "figmaCollection": "1. TailwindCSS",
                "codePath": f"primitive.dimension.border-width.{k}",
                "cssVar": css_name_from_path(f"border-width.{k.lower()}"),
                "tier": "primitive",
            }
        )

    rounded = {
        "none": {"$type": "dimension", "$value": "0px"},
        "full": {"$type": "dimension", "$value": "9999px"},
        # aliases into theme.radius for the rest
        "xs": alias("theme.radius.xs", "dimension"),
        "sm": alias("theme.radius.sm", "dimension"),
        "md": alias("theme.radius.md", "dimension"),
        "lg": alias("theme.radius.lg", "dimension"),
        "xl": alias("theme.radius.xl", "dimension"),
        "2xl": alias("theme.radius.2xl", "dimension"),
        "3xl": alias("theme.radius.3xl", "dimension"),
        "4xl": alias("theme.radius.4xl", "dimension"),
    }
    for k in rounded:
        figma = f"border-radius/rounded-{k}"
        mappings.append(
            {
                "figma": figma,
                "figmaCollection": "1. TailwindCSS",
                "codePath": f"primitive.dimension.rounded.{k}",
                "cssVar": css_name_from_path(f"rounded.{k}"),
                "tier": "primitive",
            }
        )

    data = {
        "meta": {"tier": "primitive", "figmaCollection": "1. TailwindCSS"},
        "spacing": space_out,
        "opacity": opacity,
        "border-width": border_width,
        "rounded": rounded,
    }
    return data, mappings


def build_theme(export: dict) -> tuple[dict, dict, dict, dict, dict, list[dict]]:
    mappings = []
    # Theme colors: primary-light etc.
    theme_color = {"meta": {"tier": "theme", "figmaCollection": "2. Theme", "group": "colors"}}
    for key, ref in export["themeColors"].items():
        code_key = key  # already primary-light
        theme_color[code_key] = ref_to_alias(ref)
        mappings.append(
            {
                "figma": f"colors/{key}",
                "figmaCollection": "2. Theme",
                "codePath": f"theme.color.{code_key}",
                "cssVar": css_name_from_path(f"theme.{code_key}"),
                "tier": "theme",
            }
        )

    theme_radius = {"meta": {"tier": "theme", "figmaCollection": "2. Theme", "group": "radius"}}
    for k, v in export["radius"].items():
        if k == "none":
            theme_radius[k] = {"$type": "dimension", "$value": "0px"}
        elif k == "full":
            theme_radius[k] = {"$type": "dimension", "$value": "9999px"}
        else:
            num = int(str(v).replace("px", ""))
            theme_radius[k] = {"$type": "dimension", "$value": f"{num}px"}
        mappings.append(
            {
                "figma": f"radius/{k}" if k not in ("none", "full") else f"border-radius/rounded-{k}",
                "figmaCollection": "2. Theme" if k not in ("none", "full") else "1. TailwindCSS",
                "codePath": f"theme.radius.{k}",
                "cssVar": css_name_from_path(f"radius.{k}"),
                "tier": "theme",
            }
        )

    typo = export["typography"]
    theme_type = {
        "meta": {"tier": "theme", "figmaCollection": "2. Theme", "group": "font+text"},
        "font": typo["font"],
        "font-weight": typo["font-weight"],
        "text": typo["text"],
    }
    for figma_name, code_name in [("font/font-sans", "sans"), ("font/font-serif", "serif"), ("font/font-mono", "mono")]:
        mappings.append(
            {
                "figma": figma_name,
                "figmaCollection": "2. Theme",
                "codePath": f"theme.typography.font.{code_name}",
                "cssVar": css_name_from_path(f"font.{code_name}"),
                "tier": "theme",
            }
        )
    for weight in typo["font-weight"]:
        mappings.append(
            {
                "figma": f"font-weight/{weight}",
                "figmaCollection": "2. Theme",
                "codePath": f"theme.typography.font-weight.{weight}",
                "cssVar": css_name_from_path(f"font-weight.{weight}"),
                "tier": "theme",
            }
        )
    for size in typo["text"]:
        mappings.append(
            {
                "figma": f"text/{size}/font-size",
                "figmaCollection": "2. Theme",
                "codePath": f"theme.typography.text.{size}.font-size",
                "cssVar": css_name_from_path(f"text.{size}.size"),
                "tier": "theme",
            }
        )
        mappings.append(
            {
                "figma": f"text/{size}/line-height",
                "figmaCollection": "2. Theme",
                "codePath": f"theme.typography.text.{size}.line-height",
                "cssVar": css_name_from_path(f"text.{size}.line-height"),
                "tier": "theme",
            }
        )

    theme_shadow = {
        "meta": {"tier": "theme", "figmaCollection": "2. Theme", "group": "shadow+blur"},
        "shadow": export["shadow"]["shadow"],
        "blur": export["shadow"]["blur"],
    }
    for name in export["shadow"]["shadow"]:
        mappings.append(
            {
                "figma": f"shadow/{name}",
                "figmaCollection": "2. Theme",
                "codePath": f"theme.shadow.shadow.{name}",
                "cssVar": css_name_from_path(f"shadow.{name}"),
                "tier": "theme",
            }
        )
    for name in export["shadow"]["blur"]:
        mappings.append(
            {
                "figma": f"blur/{name}",
                "figmaCollection": "2. Theme",
                "codePath": f"theme.shadow.blur.{name}",
                "cssVar": css_name_from_path(f"blur.{name}"),
                "tier": "theme",
            }
        )

    # breakpoints + containers live in Theme in Figma
    theme_layout = {
        "meta": {"tier": "theme", "figmaCollection": "2. Theme", "group": "breakpoint+container"},
        "breakpoint": {},
        "container": {},
    }
    for k, v in export["breakpoints"].items():
        num = int(str(v).replace("px", ""))
        theme_layout["breakpoint"][k] = {"$type": "dimension", "$value": f"{num}px"}
        mappings.append(
            {
                "figma": f"breakpoint/{k}",
                "figmaCollection": "2. Theme",
                "codePath": f"theme.layout.breakpoint.{k}",
                "cssVar": css_name_from_path(f"breakpoint.{k}"),
                "tier": "theme",
            }
        )
    for k, v in export["containers"].items():
        num = int(str(v).replace("px", ""))
        theme_layout["container"][k] = {"$type": "dimension", "$value": f"{num}px"}
        mappings.append(
            {
                "figma": f"container/{k}",
                "figmaCollection": "2. Theme",
                "codePath": f"theme.layout.container.{k}",
                "cssVar": css_name_from_path(f"container.{k}"),
                "tier": "theme",
            }
        )

    return theme_color, theme_radius, theme_type, theme_shadow, theme_layout, mappings


def build_semantic(export: dict) -> tuple[dict, dict, list[dict]]:
    mappings = []
    semantic = {
        "meta": {
            "tier": "semantic",
            "figmaCollection": "3. Mode",
            "modes": ["light", "dark"],
            "note": "Normalized from Mode base/*; aliases Theme colors/*-light|dark",
        },
        "light": {},
        "dark": {},
    }
    for name in export["modeBase"]:
        if name in LAB_ONLY_FORBIDDEN:
            continue
        # Theme path: colors/{name}-light
        semantic["light"][name] = alias(f"theme.color.{name}-light")
        semantic["dark"][name] = alias(f"theme.color.{name}-dark")
        mappings.append(
            {
                "figma": f"base/{name}",
                "figmaCollection": "3. Mode",
                "codePath": f"semantic.color.{{mode}}.{name}",
                "cssVar": css_name_from_path(name),
                "tier": "semantic",
                "modes": ["Light", "Dark"],
            }
        )

    alpha = {"meta": {"tier": "semantic", "figmaCollection": "3. Mode", "group": "alpha"}, "light": {}, "dark": {}}
    for step, modes in export["modeAlpha"].items():
        alpha["light"][step] = color_token(modes["Light"]["hex"], modes["Light"]["alpha"])
        alpha["dark"][step] = color_token(modes["Dark"]["hex"], modes["Dark"]["alpha"])
        mappings.append(
            {
                "figma": f"alpha/{step}",
                "figmaCollection": "3. Mode",
                "codePath": f"semantic.alpha.{{mode}}.{step}",
                "cssVar": css_name_from_path(f"alpha.{step}"),
                "tier": "semantic",
                "modes": ["Light", "Dark"],
            }
        )
    return semantic, alpha, mappings


def build_custom(export: dict) -> tuple[dict, dict, list[dict]]:
    mappings = []
    recipes = {"meta": {"tier": "custom", "figmaCollection": "3. Mode", "group": "custom"}, "light": {}, "dark": {}}
    figma_names = export["modeCustomFigmaNames"]
    for key, modes in export["modeCustom"].items():
        recipes["light"][key] = ref_to_alias(modes["Light"])
        recipes["dark"][key] = ref_to_alias(modes["Dark"])
        mappings.append(
            {
                "figma": figma_names.get(key, f"custom/{key}"),
                "figmaCollection": "3. Mode",
                "codePath": f"custom.mode-recipes.{{mode}}.{key}",
                "cssVar": css_name_from_path(f"custom.{key}"),
                "tier": "custom",
                "modes": ["Light", "Dark"],
            }
        )

    layout = {
        "meta": {"tier": "custom", "figmaCollection": "4. Custom", "modes": ["desktop", "mobile"]},
        "desktop": {},
        "mobile": {},
    }
    # From typography headings + spacing layout
    typo = export["typography"]
    for size, modes in typo.get("heading", {}).items():
        for mode_name, props in modes.items():
            bucket = layout[mode_name]
            bucket.setdefault("heading", {})[size] = props
            mappings.append(
                {
                    "figma": f"heading-{size}/*",
                    "figmaCollection": "4. Custom",
                    "codePath": f"custom.layout.{mode_name}.heading.{size}",
                    "cssVar": css_name_from_path(f"heading.{size}.{mode_name}"),
                    "tier": "custom",
                }
            )
    for key, modes in export["layout"].items():
        for mode_name, tok in modes.items():
            layout[mode_name][key] = tok
            mappings.append(
                {
                    "figma": key.replace("_", "-") if False else key,
                    "figmaCollection": "4. Custom",
                    "codePath": f"custom.layout.{mode_name}.{key}",
                    "cssVar": css_name_from_path(f"layout.{key}.{mode_name}"),
                    "tier": "custom",
                }
            )
    return recipes, layout, mappings


def resolve_color_value(tok: dict, stores: dict, stack: list[str] | None = None) -> str:
    """Resolve token to CSS color value (hex or rgba or var())."""
    stack = stack or []
    val = tok["$value"]
    if isinstance(val, str) and val.startswith("{") and val.endswith("}"):
        path = val[1:-1]
        if path in stack:
            return f"/* cycle:{path} */"
        parts = path.split(".")
        # Look up in stores by path
        node = stores
        for p in parts:
            if p not in node:
                return f"/* unresolved:{path} */"
            node = node[p]
        if isinstance(node, dict) and "$value" in node:
            return resolve_color_value(node, stores, stack + [path])
        return f"/* unresolved:{path} */"
    hex_value = str(val)
    alpha = tok.get("alpha")
    if alpha is not None:
        h = hex_value.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f"rgba({r}, {g}, {b}, {alpha})"
    return hex_value.lower()


def build_css(stores: dict, semantic: dict, alpha: dict, recipes: dict, prim_color: dict, theme_radius: dict, theme_type: dict, theme_shadow: dict, prim_dim: dict) -> str:
    lines = [
        "/* GENERATED FILE — do not edit by hand.",
        " * Source: tokens/**/*.tokens.json via scripts/migrate-tokens.py",
        " * Figma: Design System V2 (TailwindCSS → Theme → Mode)",
        " */",
        "",
        ":root {",
    ]
    # primitives colors
    for family, scale in prim_color.items():
        if family in ("meta", "$description"):
            continue
        if isinstance(scale, dict) and "$type" in scale:
            lines.append(f"  {css_name_from_path(f'color.{family}')}: {resolve_color_value(scale, stores)};")
        else:
            for step, tok in scale.items():
                lines.append(f"  {css_name_from_path(f'color.{family}.{step}')}: {resolve_color_value(tok, stores)};")
    lines.append("")
    for k, tok in prim_dim["spacing"].items():
        lines.append(f"  {css_name_from_path(f'spacing.{k}')}: {tok['$value']};")
    lines.append("")
    for k, tok in theme_radius.items():
        if k == "meta":
            continue
        val = tok["$value"]
        if isinstance(val, str) and val.startswith("{"):
            # alias — emit var to radius target
            inner = val[1:-1].replace("theme.radius.", "")
            lines.append(f"  {css_name_from_path(f'radius.{k}')}: var({css_name_from_path(f'radius.{inner}')});")
        else:
            lines.append(f"  {css_name_from_path(f'radius.{k}')}: {val};")
    lines.append("")
    for name, tok in theme_type["font"].items():
        lines.append(f"  {css_name_from_path(f'font.{name}')}: {tok['$value']}, system-ui, sans-serif;")
    for name, tok in theme_type["font-weight"].items():
        lines.append(f"  {css_name_from_path(f'font-weight.{name}')}: {tok['$value']};")
    for size, props in theme_type["text"].items():
        lines.append(f"  {css_name_from_path(f'text.{size}.size')}: {props['font-size']['$value']};")
        lines.append(f"  {css_name_from_path(f'text.{size}.line-height')}: {props['line-height']['$value']};")
    lines.append("")
    for name, layers in theme_shadow["shadow"].items():
        parts = []
        for layer in layers:
            v = layer["$value"]
            parts.append(f"{v['offsetX']}px {v['offsetY']}px {v['blur']}px {v['spread']}px {v['color']}")
        lines.append(f"  {css_name_from_path(f'shadow.{name}')}: {', '.join(parts)};")
    lines.append("")
    lines.append("  /* Semantic (Mode / Light) */")
    for name, tok in semantic["light"].items():
        # Prefer CSS var() chain through theme for clarity
        theme_key = f"{name}-light"
        lines.append(f"  {css_name_from_path(name)}: var({css_name_from_path(f'theme.{theme_key}')});")
    # Emit theme color vars resolved
    lines.append("")
    lines.append("  /* Theme color knobs (light-facing defaults + resolved) */")
    for key, tok in stores["theme"]["color"].items():
        if key == "meta":
            continue
        lines.append(f"  {css_name_from_path(f'theme.{key}')}: {resolve_color_value(tok, stores)};")
    for step, tok in alpha["light"].items():
        lines.append(f"  {css_name_from_path(f'alpha.{step}')}: {resolve_color_value(tok, stores)};")
    for key, tok in recipes["light"].items():
        lines.append(f"  {css_name_from_path(f'custom.{key}')}: {resolve_color_value(tok, stores)};")
    lines.append("}")
    lines.append("")
    lines.append(".dark {")
    for name, tok in semantic["dark"].items():
        theme_key = f"{name}-dark"
        lines.append(f"  {css_name_from_path(name)}: var({css_name_from_path(f'theme.{theme_key}')});")
    for step, tok in alpha["dark"].items():
        lines.append(f"  {css_name_from_path(f'alpha.{step}')}: {resolve_color_value(tok, stores)};")
    for key, tok in recipes["dark"].items():
        lines.append(f"  {css_name_from_path(f'custom.{key}')}: {resolve_color_value(tok, stores)};")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def validate(stores: dict, mappings: list[dict], semantic: dict) -> dict:
    report = {
        "unresolvedAliases": [],
        "missingMappings": [],
        "duplicateNormalizedNames": [],
        "labOnlyLeaks": [],
        "tokenCounts": {},
        "parityStatus": "unknown",
    }

    def walk(node, prefix=""):
        count = 0
        if isinstance(node, dict):
            if "$type" in node:
                val = node.get("$value")
                if isinstance(val, str) and val.startswith("{") and val.endswith("}"):
                    path = val[1:-1]
                    parts = path.split(".")
                    cur = stores
                    ok = True
                    for p in parts:
                        if not isinstance(cur, dict) or p not in cur:
                            ok = False
                            break
                        cur = cur[p]
                    if not ok or not (isinstance(cur, dict) and "$value" in cur):
                        report["unresolvedAliases"].append({"from": prefix, "alias": path})
                return 1
            for k, v in node.items():
                if k in ("meta", "$description"):
                    continue
                count += walk(v, f"{prefix}.{k}" if prefix else k)
        return count

    for tier, data in stores.items():
        report["tokenCounts"][tier] = walk(data, tier)

    # duplicate css vars
    css_vars = defaultdict(list)
    for m in mappings:
        css_vars[m["cssVar"]].append(m["codePath"])
    for var, paths in css_vars.items():
        uniq = sorted(set(paths))
        if len(uniq) > 1:
            report["duplicateNormalizedNames"].append({"cssVar": var, "codePaths": uniq})

    # lab-only leaks in semantic
    for mode in ("light", "dark"):
        for name in semantic.get(mode, {}):
            if name in LAB_ONLY_FORBIDDEN:
                report["labOnlyLeaks"].append(f"semantic.color.{mode}.{name}")

    # expected Mode base tokens all mapped
    expected_base = set(semantic["light"].keys())
    mapped_base = {m["cssVar"].lstrip("-") for m in mappings if m["tier"] == "semantic" and m["figma"].startswith("base/")}
    # cssVar is --primary etc
    for name in expected_base:
        css = css_name_from_path(name)
        if not any(m["cssVar"] == css for m in mappings):
            report["missingMappings"].append(name)

    if not report["unresolvedAliases"] and not report["labOnlyLeaks"]:
        report["parityStatus"] = "PASS_WITH_NOTES" if report["duplicateNormalizedNames"] else "PASS"
    else:
        report["parityStatus"] = "FAIL"

    return report


def main() -> None:
    export = json.loads(RAW.read_text())
    all_mappings: list[dict] = []

    prim_color, m = build_primitive_color(export)
    all_mappings.extend(m)
    prim_dim, m = build_primitive_dimension(export)
    all_mappings.extend(m)
    theme_color, theme_radius, theme_type, theme_shadow, theme_layout, m = build_theme(export)
    all_mappings.extend(m)
    semantic, alpha, m = build_semantic(export)
    all_mappings.extend(m)
    recipes, layout, m = build_custom(export)
    all_mappings.extend(m)

    # Nested stores for alias resolution
    stores = {
        "primitive": {"color": {k: v for k, v in prim_color.items() if k not in ("meta", "$description")}, "dimension": prim_dim},
        "theme": {
            "color": {k: v for k, v in theme_color.items() if k != "meta"},
            "radius": {k: v for k, v in theme_radius.items() if k != "meta"},
            "typography": theme_type,
            "shadow": theme_shadow,
            "layout": theme_layout,
        },
        "semantic": {"color": semantic, "alpha": alpha},
        "custom": {"mode-recipes": recipes, "layout": layout},
    }

    # Write meta
    dump(
        TOKENS / "meta.json",
        {
            "version": "0.4.0",
            "architecture": "TailwindCSS → Theme → Mode",
            "decisions": {"Decision1": "A", "Decision2": "B", "Decision3": "B", "Decision4": "A"},
            "source": export["meta"],
            "labOnlyRemoved": sorted(LAB_ONLY_FORBIDDEN),
            "tiers": ["primitive", "theme", "semantic", "custom", "mappings"],
            "css": "src/styles/tokens.css",
            "generator": "scripts/migrate-tokens.py",
        },
    )

    dump(TOKENS / "primitive" / "color.tokens.json", prim_color)
    dump(TOKENS / "primitive" / "dimension.tokens.json", prim_dim)
    dump(TOKENS / "theme" / "color.tokens.json", theme_color)
    dump(TOKENS / "theme" / "radius.tokens.json", theme_radius)
    dump(TOKENS / "theme" / "typography.tokens.json", theme_type)
    dump(TOKENS / "theme" / "shadow.tokens.json", theme_shadow)
    dump(TOKENS / "theme" / "layout.tokens.json", theme_layout)
    dump(TOKENS / "semantic" / "color.tokens.json", semantic)
    dump(TOKENS / "semantic" / "alpha.tokens.json", alpha)
    dump(TOKENS / "custom" / "mode-recipes.tokens.json", recipes)
    dump(TOKENS / "custom" / "layout.tokens.json", layout)
    dump(
        TOKENS / "mappings" / "figma-to-code.json",
        {
            "meta": {
                "purpose": "Explicit Figma → repo/CSS mappings (Decision3=B)",
                "naming": "Figma paths preserved in `figma`; code uses normalized paths",
            },
            "mappings": all_mappings,
        },
    )

    css = build_css(stores, semantic, alpha, recipes, stores["primitive"]["color"], theme_radius, theme_type, theme_shadow, prim_dim)
    CSS_OUT.parent.mkdir(parents=True, exist_ok=True)
    CSS_OUT.write_text(css, encoding="utf-8")

    report = validate(stores, all_mappings, semantic)
    report["mappingCount"] = len(all_mappings)
    report["cssBytes"] = len(css)
    dump(TOKENS / "_validation-report.json", report)

    # Remove legacy flat token files (deprecated)
    for legacy in [
        TOKENS / "color.tokens.json",
        TOKENS / "spacing.tokens.json",
        TOKENS / "radius.tokens.json",
        TOKENS / "typography.tokens.json",
        TOKENS / "shadow.tokens.json",
    ]:
        if legacy.exists():
            legacy.unlink()

    # Remove old hardcoded sync script if present — replaced by migrate-tokens.py
    old_script = ROOT / "scripts" / "sync-figma-tokens.py"
    if old_script.exists():
        old_script.unlink()

    print(json.dumps({"parityStatus": report["parityStatus"], "tokenCounts": report["tokenCounts"], "unresolved": len(report["unresolvedAliases"]), "duplicates": len(report["duplicateNormalizedNames"]), "labLeaks": report["labOnlyLeaks"]}, indent=2))


if __name__ == "__main__":
    main()
