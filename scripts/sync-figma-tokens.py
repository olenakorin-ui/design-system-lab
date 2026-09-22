#!/usr/bin/env python3
"""Write canonical token files extracted from Design System V2 Figma."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "tokens"
CSS = ROOT / "src" / "styles" / "tokens.css"

SOURCE = "https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=580-9181"


def color(value: str, alpha: float | None = None) -> dict:
    token = {"$type": "color", "$value": value}
    if alpha is not None:
        token["alpha"] = alpha
    return token


def alias(path: str, type_name: str = "color") -> dict:
    return {"$type": type_name, "$value": f"{{{path}}}"}


def number(value: int | float, unit: str = "px") -> dict:
    return {"$type": "dimension", "$value": f"{value}{unit}" if unit else value}


def string(value: str) -> dict:
    return {"$type": "fontFamily" if True else "string", "$value": value}


def font_weight(value: int) -> dict:
    return {"$type": "fontWeight", "$value": value}


PALETTES = {
    "slate": {
        "50": "#F8FAFC", "100": "#F1F5F9", "200": "#E2E8F0", "300": "#CBD5E1",
        "400": "#94A3B8", "500": "#64748B", "600": "#475569", "700": "#334155",
        "800": "#1E293B", "900": "#0F172A", "950": "#020617",
    },
    "gray": {
        "50": "#F9FAFB", "100": "#F3F4F6", "200": "#E5E7EB", "300": "#D1D5DB",
        "400": "#9CA3AF", "500": "#6B7280", "600": "#4B5563", "700": "#374151",
        "800": "#1F2937", "900": "#111827", "950": "#030712",
    },
    "zinc": {
        "50": "#FAFAFA", "100": "#F4F4F5", "200": "#E4E4E7", "300": "#D4D4D8",
        "400": "#A1A1AA", "500": "#71717A", "600": "#52525B", "700": "#3F3F46",
        "800": "#27272A", "900": "#18181B", "950": "#09090B",
    },
    "neutral": {
        "50": "#FAFAFA", "100": "#F5F5F5", "200": "#E5E5E5", "300": "#D4D4D4",
        "400": "#A3A3A3", "500": "#737373", "600": "#525252", "700": "#404040",
        "800": "#262626", "900": "#171717", "950": "#0A0A0A",
    },
    "stone": {
        "50": "#FAFAF9", "100": "#F5F5F4", "200": "#E7E5E4", "300": "#D6D3D1",
        "400": "#A8A29E", "500": "#78716C", "600": "#57534E", "700": "#44403C",
        "800": "#292524", "900": "#1C1917", "950": "#0C0A09",
    },
    "red": {
        "50": "#FEF2F2", "100": "#FEE2E2", "200": "#FECACA", "300": "#FCA5A5",
        "400": "#F87171", "500": "#EF4444", "600": "#DC2626", "700": "#B91C1C",
        "800": "#991B1B", "900": "#7F1D1D", "950": "#450A0A",
    },
    "orange": {
        "50": "#FFF7ED", "100": "#FFEDD5", "200": "#FED7AA", "300": "#FDBA74",
        "400": "#FB923C", "500": "#F97316", "600": "#EA580C", "700": "#C2410C",
        "800": "#9A3412", "900": "#7C2D12", "950": "#431407",
    },
    "amber": {
        "50": "#FFFBEB", "100": "#FEF3C7", "200": "#FDE68A", "300": "#FCD34D",
        "400": "#FBBF24", "500": "#F59E0B", "600": "#D97706", "700": "#B45309",
        "800": "#92400E", "900": "#78350F", "950": "#451A03",
    },
    "yellow": {
        "50": "#FEFCE8", "100": "#FEF9C3", "200": "#FEF08A", "300": "#FDE047",
        "400": "#FACC15", "500": "#EAB308", "600": "#CA8A04", "700": "#A16207",
        "800": "#854D0E", "900": "#713F12", "950": "#422006",
    },
    "lime": {
        "50": "#F7FEE7", "100": "#ECFCCB", "200": "#D9F99D", "300": "#BEF264",
        "400": "#A3E635", "500": "#84CC16", "600": "#65A30D", "700": "#4D7C0F",
        "800": "#3F6212", "900": "#365314", "950": "#1A2E05",
    },
    "green": {
        "50": "#F0FDF4", "100": "#DCFCE7", "200": "#BBF7D0", "300": "#86EFAC",
        "400": "#4ADE80", "500": "#22C55E", "600": "#16A34A", "700": "#15803D",
        "800": "#166534", "900": "#14532D", "950": "#052E16",
    },
    "emerald": {
        "50": "#ECFDF5", "100": "#D1FAE5", "200": "#A7F3D0", "300": "#6EE7B7",
        "400": "#34D399", "500": "#10B981", "600": "#059669", "700": "#047857",
        "800": "#065F46", "900": "#064E3B", "950": "#022C22",
    },
    "teal": {
        "50": "#F0FDFA", "100": "#CCFBF1", "200": "#99F6E4", "300": "#5EEAD4",
        "400": "#2DD4BF", "500": "#14B8A6", "600": "#0D9488", "700": "#0F766E",
        "800": "#115E59", "900": "#134E4A", "950": "#042F2E",
    },
    "cyan": {
        "50": "#ECFEFF", "100": "#CFFAFE", "200": "#A5F3FC", "300": "#67E8F9",
        "400": "#22D3EE", "500": "#06B6D4", "600": "#0891B2", "700": "#0E7490",
        "800": "#155E75", "900": "#164E63", "950": "#083344",
    },
    "sky": {
        "50": "#F0F9FF", "100": "#E0F2FE", "200": "#BAE6FD", "300": "#7DD3FC",
        "400": "#38BDF8", "500": "#0EA5E9", "600": "#0284C7", "700": "#0369A1",
        "800": "#075985", "900": "#0C4A6E", "950": "#082F49",
    },
    "blue": {
        "50": "#EFF6FF", "100": "#DBEAFE", "200": "#BFDBFE", "300": "#93C5FD",
        "400": "#60A5FA", "500": "#3B82F6", "600": "#2563EB", "700": "#1D4ED8",
        "800": "#1E40AF", "900": "#1E3A8A", "950": "#172554",
    },
    "indigo": {
        "50": "#EEF2FF", "100": "#E0E7FF", "200": "#C7D2FE", "300": "#A5B4FC",
        "400": "#818CF8", "500": "#6366F1", "600": "#4F46E5", "700": "#4338CA",
        "800": "#3730A3", "900": "#312E81", "950": "#1E1B4B",
    },
    "violet": {
        "50": "#F5F3FF", "100": "#EDE9FE", "200": "#DDD6FE", "300": "#C4B5FD",
        "400": "#A78BFA", "500": "#8B5CF6", "600": "#7C3AED", "700": "#6D28D9",
        "800": "#5B21B6", "900": "#4C1D95", "950": "#1E1B4B",
    },
    "purple": {
        "50": "#FAF5FF", "100": "#F3E8FF", "200": "#E9D5FF", "300": "#D8B4FE",
        "400": "#C084FC", "500": "#A855F7", "600": "#9333EA", "700": "#7E22CE",
        "800": "#6B21A8", "900": "#581C87", "950": "#3B0764",
    },
    "fuchsia": {
        "50": "#FDF4FF", "100": "#FAE8FF", "200": "#F5D0FE", "300": "#F0ABFC",
        "400": "#E879F9", "500": "#D946EF", "600": "#C026D3", "700": "#A21CAF",
        "800": "#86198F", "900": "#701A75", "950": "#4A044E",
    },
    "pink": {
        "50": "#FDF2F8", "100": "#FCE7F3", "200": "#FBCFE8", "300": "#F9A8D4",
        "400": "#F472B6", "500": "#EC4899", "600": "#DB2777", "700": "#BE185D",
        "800": "#9D174D", "900": "#831843", "950": "#500724",
    },
    "rose": {
        "50": "#FFF1F2", "100": "#FFE4E6", "200": "#FECDD3", "300": "#FDA4AF",
        "400": "#FB7185", "500": "#F43F5E", "600": "#E11D48", "700": "#BE123C",
        "800": "#9F1239", "900": "#881337", "950": "#4C0519",
    },
}

SPACING = {
    "0": 0, "px": 1, "0-5": 2, "1": 4, "1-5": 6, "2": 8, "2-5": 10, "3": 12,
    "3-5": 14, "4": 16, "5": 20, "6": 24, "7": 28, "8": 32, "9": 36, "10": 40,
    "11": 44, "12": 48, "14": 56, "16": 64, "20": 80, "24": 96, "28": 112,
    "32": 128, "36": 144, "40": 160, "44": 176, "48": 192, "52": 208, "56": 224,
    "60": 240, "64": 256, "72": 288, "80": 320, "96": 384,
}

RADIUS = {
    "none": 0, "xs": 2, "sm": 6, "md": 8, "lg": 10, "xl": 14,
    "2xl": 16, "3xl": 24, "4xl": 32, "full": 9999,
}

TEXT = {
    "xs": (12, 16), "sm": (14, 20), "base": (16, 24), "lg": (18, 28),
    "xl": (20, 28), "2xl": (24, 32), "3xl": (30, 36), "4xl": (36, 40),
    "5xl": (48, 48), "6xl": (60, 60), "7xl": (72, 72), "8xl": (96, 96),
    "9xl": (128, 128),
}

FONT_WEIGHT = {
    "thin": 100, "extralight": 200, "light": 300, "normal": 400,
    "medium": 500, "semibold": 600, "bold": 700, "extrabold": 800, "black": 900,
}


def dump(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def build_color_tokens() -> dict:
    primitive = {
        "white": color("#FFFFFF"),
        "black": color("#000000"),
        "transparent": color("#FFFFFF", 0),
    }
    for name, scale in PALETTES.items():
        primitive[name] = {step: color(hex_value) for step, hex_value in scale.items()}
    primitive["neutral"] = {"0": color("#FFFFFF"), **primitive["neutral"]}
    primitive["brand"] = {step: alias(f"primitive.blue.{step}") for step in PALETTES["blue"]}

    light = {
        "background": alias("primitive.white"),
        "foreground": alias("primitive.neutral.950"),
        "card": alias("primitive.white"),
        "card-foreground": alias("primitive.neutral.950"),
        "popover": alias("primitive.white"),
        "popover-foreground": alias("primitive.neutral.950"),
        "primary": alias("primitive.blue.600"),
        "primary-foreground": alias("primitive.neutral.50"),
        "secondary": alias("primitive.neutral.100"),
        "secondary-foreground": alias("primitive.neutral.900"),
        "muted": alias("primitive.neutral.100"),
        "muted-foreground": alias("primitive.neutral.500"),
        "accent": alias("primitive.neutral.100"),
        "accent-foreground": alias("primitive.neutral.900"),
        "destructive": alias("primitive.red.600"),
        "destructive-foreground": alias("primitive.red.50"),
        "border": alias("primitive.neutral.200"),
        "input": alias("primitive.neutral.200"),
        "ring": alias("primitive.neutral.400"),
        "ring-offset": alias("primitive.white"),
        "sidebar": alias("primitive.neutral.50"),
        "sidebar-foreground": alias("primitive.neutral.950"),
        "sidebar-primary": alias("primitive.neutral.900"),
        "sidebar-primary-foreground": alias("primitive.neutral.50"),
        "sidebar-accent": alias("primitive.neutral.100"),
        "sidebar-accent-foreground": alias("primitive.neutral.900"),
        "sidebar-border": alias("primitive.neutral.200"),
        "sidebar-ring": alias("primitive.neutral.400"),
        "chart-1": alias("primitive.orange.600"),
        "chart-2": alias("primitive.teal.600"),
        "chart-3": alias("primitive.cyan.900"),
        "chart-4": alias("primitive.amber.400"),
        "chart-5": alias("primitive.amber.500"),
        "focus-ring": alias("semantic.light.ring"),
        "border-strong": alias("primitive.neutral.400"),
        "surface-raised": alias("semantic.light.card"),
        "surface-sunken": alias("semantic.light.muted"),
        "success": alias("primitive.green.700"),
        "success-foreground": alias("primitive.white"),
        "success-subtle": alias("primitive.green.50"),
        "success-subtle-foreground": alias("primitive.green.800"),
        "warning": alias("primitive.amber.700"),
        "warning-foreground": alias("primitive.white"),
        "warning-subtle": alias("primitive.amber.50"),
        "warning-subtle-foreground": alias("primitive.amber.900"),
        "info": alias("primitive.blue.700"),
        "info-foreground": alias("primitive.white"),
        "info-subtle": alias("primitive.blue.50"),
        "info-subtle-foreground": alias("primitive.blue.800"),
        "error-subtle": alias("primitive.red.50"),
        "error-subtle-foreground": alias("primitive.red.800"),
    }
    dark = {
        "background": alias("primitive.neutral.950"),
        "foreground": alias("primitive.neutral.50"),
        "card": alias("primitive.neutral.900"),
        "card-foreground": alias("primitive.neutral.50"),
        "popover": alias("primitive.neutral.800"),
        "popover-foreground": alias("primitive.neutral.50"),
        "primary": alias("primitive.neutral.200"),
        "primary-foreground": alias("primitive.neutral.900"),
        "secondary": alias("primitive.neutral.800"),
        "secondary-foreground": alias("primitive.neutral.50"),
        "muted": alias("primitive.neutral.800"),
        "muted-foreground": alias("primitive.neutral.400"),
        "accent": alias("primitive.neutral.700"),
        "accent-foreground": alias("primitive.neutral.50"),
        "destructive": alias("primitive.red.400"),
        "destructive-foreground": alias("primitive.red.50"),
        "border": color("#FFFFFF", 0.1),
        "input": color("#FFFFFF", 0.15),
        "ring": alias("primitive.neutral.500"),
        "ring-offset": alias("primitive.neutral.950"),
        "sidebar": alias("primitive.neutral.900"),
        "sidebar-foreground": alias("primitive.neutral.50"),
        "sidebar-primary": alias("primitive.blue.700"),
        "sidebar-primary-foreground": alias("primitive.neutral.50"),
        "sidebar-accent": alias("primitive.neutral.800"),
        "sidebar-accent-foreground": alias("primitive.neutral.50"),
        "sidebar-border": color("#FFFFFF", 0.1),
        "sidebar-ring": alias("primitive.neutral.600"),
        "chart-1": alias("primitive.blue.700"),
        "chart-2": alias("primitive.emerald.500"),
        "chart-3": alias("primitive.amber.500"),
        "chart-4": alias("primitive.purple.500"),
        "chart-5": alias("primitive.rose.500"),
        "focus-ring": alias("semantic.dark.ring"),
        "border-strong": alias("primitive.neutral.600"),
        "surface-raised": alias("semantic.dark.card"),
        "surface-sunken": alias("semantic.dark.background"),
        "success": alias("primitive.green.400"),
        "success-foreground": alias("primitive.neutral.950"),
        "success-subtle": alias("primitive.green.950"),
        "success-subtle-foreground": alias("primitive.green.200"),
        "warning": alias("primitive.amber.400"),
        "warning-foreground": alias("primitive.neutral.950"),
        "warning-subtle": alias("primitive.amber.950"),
        "warning-subtle-foreground": alias("primitive.amber.200"),
        "info": alias("primitive.blue.400"),
        "info-foreground": alias("primitive.neutral.950"),
        "info-subtle": alias("primitive.blue.950"),
        "info-subtle-foreground": alias("primitive.blue.200"),
        "error-subtle": alias("primitive.red.950"),
        "error-subtle-foreground": alias("primitive.red.200"),
    }
    alpha = {
        step: {
            "light": color("#FFFFFF", round((100 - int(step)) / 100, 2)),
            "dark": color("#0A0A0A", round((100 - int(step)) / 100, 2)),
        }
        for step in ["5", "10", "20", "30", "40", "50", "60", "70", "80", "90"]
    }
    return {
        "meta": {
            "name": "Design System V2 Color Tokens",
            "version": "0.3.0",
            "source": SOURCE,
            "figmaFileKey": "ZllxQplWi5QJcNeUHeY8T3",
            "direction": "Tailwind Neutral + Blue (shadcn/ui Mode collection)",
            "note": "Extracted from Figma Design System V2. Semantic tokens alias Figma Mode/Theme variables.",
        },
        "primitive": primitive,
        "semantic": {"light": light, "dark": dark},
        "alpha": alpha,
    }


def build_spacing_tokens() -> dict:
    return {
        "meta": {
            "name": "Design System V2 Spacing Tokens",
            "version": "0.3.0",
            "source": SOURCE,
            "collection": "1. TailwindCSS / spacing",
        },
        "space": {key: number(value) for key, value in SPACING.items()},
        "layout": {
            "container-padding-x": {
                "desktop": number(24),
                "mobile": number(24),
            },
            "section-padding-y": {
                "desktop": number(96),
                "mobile": number(64),
            },
            "section-title-gap-xl": {"desktop": number(24), "mobile": number(16)},
            "section-title-gap-lg": {"desktop": number(20), "mobile": number(16)},
            "section-title-gap-md": {"desktop": number(20), "mobile": number(20)},
            "section-title-gap-sm": {"desktop": number(16), "mobile": number(16)},
        },
        "breakpoint": {
            "sm": number(640),
            "md": number(768),
            "lg": number(1024),
            "xl": number(1280),
            "2xl": number(1536),
        },
        "container": {
            "3xs": number(256), "2xs": number(288), "xs": number(320),
            "sm": number(384), "md": number(448), "lg": number(512),
            "xl": number(576), "2xl": number(672), "3xl": number(768),
            "4xl": number(896), "5xl": number(1024), "6xl": number(1152),
            "7xl": number(1280),
        },
    }


def build_radius_tokens() -> dict:
    return {
        "meta": {
            "name": "Design System V2 Radius Tokens",
            "version": "0.3.0",
            "source": SOURCE,
            "collection": "2. Theme / radius",
        },
        "radius": {key: number(value) for key, value in RADIUS.items()},
    }


def build_typography_tokens() -> dict:
    text = {
        name: {
            "font-size": number(size),
            "line-height": number(line),
        }
        for name, (size, line) in TEXT.items()
    }
    headings = {
        "xl": {"desktop": {"font-size": number(48), "line-height": number(48)}, "mobile": {"font-size": number(30), "line-height": number(36)}},
        "lg": {"desktop": {"font-size": number(36), "line-height": number(40)}, "mobile": {"font-size": number(30), "line-height": number(36)}},
        "md": {"desktop": {"font-size": number(30), "line-height": number(36)}, "mobile": {"font-size": number(30), "line-height": number(36)}},
        "sm": {"desktop": {"font-size": number(24), "line-height": number(32)}, "mobile": {"font-size": number(24), "line-height": number(32)}},
    }
    for heading in headings.values():
        for mode in heading.values():
            mode["font-family"] = {"$type": "fontFamily", "$value": "Geist"}
            mode["font-weight"] = font_weight(700)
            mode["letter-spacing"] = number(0)
    return {
        "meta": {
            "name": "Design System V2 Typography Tokens",
            "version": "0.3.0",
            "source": SOURCE,
            "collection": "2. Theme / font + text, 4. Custom headings",
        },
        "font": {
            "sans": {"$type": "fontFamily", "$value": "Geist"},
            "serif": {"$type": "fontFamily", "$value": "Georgia"},
            "mono": {"$type": "fontFamily", "$value": "Geist Mono"},
        },
        "font-weight": {name: font_weight(value) for name, value in FONT_WEIGHT.items()},
        "text": text,
        "heading": headings,
    }


def shadow(offset_y: int, blur: int, spread: int, alpha: float, offset_x: int = 0) -> dict:
    return {
        "$type": "shadow",
        "$value": {
            "offsetX": offset_x,
            "offsetY": offset_y,
            "blur": blur,
            "spread": spread,
            "color": f"rgba(0,0,0,{alpha})",
        },
    }


def build_shadow_tokens() -> dict:
    return {
        "meta": {
            "name": "Design System V2 Shadow Tokens",
            "version": "0.3.0",
            "source": SOURCE,
            "collection": "2. Theme / shadow",
        },
        "shadow": {
            "2xs": [shadow(1, 0, 0, 0.05)],
            "xs": [shadow(1, 2, 0, 0.05)],
            "sm": [shadow(1, 3, 0, 0.1), shadow(1, 2, -1, 0.1)],
            "md": [shadow(4, 6, -1, 0.1), shadow(2, 4, -2, 0.1)],
            "lg": [shadow(10, 15, -3, 0.1), shadow(4, 6, -4, 0.1)],
            "xl": [shadow(20, 25, -5, 0.1), shadow(8, 10, -6, 0.1)],
            "2xl": [shadow(25, 50, -12, 0.25)],
        },
        "blur": {
            "xs": number(4), "sm": number(8), "md": number(12), "lg": number(16),
            "xl": number(24), "2xl": number(40), "3xl": number(64),
        },
    }


def css_color(token: dict) -> str:
    value = token["$value"]
    alpha = token.get("alpha")
    if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
        path = value[1:-1].split(".")
        if path[0] == "primitive" and path[1] == "white":
            hex_value = "#FFFFFF"
        elif path[0] == "primitive" and path[1] == "brand":
            hex_value = PALETTES["blue"][path[2]]
        elif path[0] == "primitive" and path[1] in PALETTES:
            hex_value = PALETTES[path[1]][path[2]]
        elif path == ["primitive", "neutral", "0"]:
            hex_value = "#FFFFFF"
        elif path[0] == "semantic":
            return css_color(build_color_tokens()["semantic"][path[1]][path[2]])
        else:
            hex_value = value
        return hex_value.lower()
    if alpha is not None:
        hex_value = value.lstrip("#")
        r = int(hex_value[0:2], 16)
        g = int(hex_value[2:4], 16)
        b = int(hex_value[4:6], 16)
        return f"rgba({r}, {g}, {b}, {alpha})"
    return str(value).lower()


def css_var_name(name: str) -> str:
    return f"--{name}"


def shadow_css(layers: list[dict]) -> str:
    parts = []
    for layer in layers:
        value = layer["$value"]
        parts.append(
            f"{value['offsetX']}px {value['offsetY']}px {value['blur']}px {value['spread']}px {value['color']}"
        )
    return ", ".join(parts)


def build_css(color_tokens: dict) -> str:
    lines = [
        "/* Design System V2 tokens v0.3",
        "   Extracted from Figma: Design System V2",
        f"   Source: {SOURCE}",
        "   Canonical values: /tokens/*.tokens.json",
        "*/",
        "",
        ":root {",
        "  --white: #ffffff;",
        "  --black: #000000;",
        "  --transparent: rgba(255, 255, 255, 0);",
        "",
    ]
    for step, hex_value in {"0": "#FFFFFF", **PALETTES["neutral"]}.items():
        lines.append(f"  --neutral-{step}: {hex_value.lower()};")
    lines.append("")
    for family in ["blue", "red", "green", "amber", "orange", "teal", "cyan", "emerald", "purple", "rose"]:
        for step, hex_value in PALETTES[family].items():
            lines.append(f"  --{family}-{step}: {hex_value.lower()};")
        lines.append("")
    for step in PALETTES["blue"]:
        lines.append(f"  --brand-{step}: var(--blue-{step});")
    lines.append("")
    for key, value in SPACING.items():
        css_key = key.replace("-", "\\.") if key.endswith("-5") or key == "0-5" else key
        lines.append(f"  --space-{key}: {value}px;")
    lines.append("")
    for key, value in RADIUS.items():
        lines.append(f"  --radius-{key}: {value}px;")
    lines.append("")
    lines.append("  --font-sans: Geist, ui-sans-serif, system-ui, sans-serif;")
    lines.append("  --font-serif: Georgia, ui-serif, serif;")
    lines.append("  --font-mono: \"Geist Mono\", ui-monospace, monospace;")
    for name, weight in FONT_WEIGHT.items():
        lines.append(f"  --font-weight-{name}: {weight};")
    lines.append("")
    for name, (size, line) in TEXT.items():
        lines.append(f"  --text-{name}-size: {size}px;")
        lines.append(f"  --text-{name}-line-height: {line}px;")
    lines.append("")
    shadow_tokens = build_shadow_tokens()["shadow"]
    for name, layers in shadow_tokens.items():
        lines.append(f"  --shadow-{name}: {shadow_css(layers)};")
    lines.append("")
    light = color_tokens["semantic"]["light"]
    lines.append("  /* Light semantic mappings (Figma Mode / Light) */")
    for name, token in light.items():
        lines.append(f"  {css_var_name(name)}: {css_color(token)};")
    for step, modes in color_tokens["alpha"].items():
        lines.append(f"  --alpha-{step}: {css_color(modes['light'])};")
    lines.append("}")
    lines.append("")
    lines.append(".dark {")
    dark = color_tokens["semantic"]["dark"]
    for name, token in dark.items():
        lines.append(f"  {css_var_name(name)}: {css_color(token)};")
    for step, modes in color_tokens["alpha"].items():
        lines.append(f"  --alpha-{step}: {css_color(modes['dark'])};")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    TOKENS.mkdir(exist_ok=True)
    color_tokens = build_color_tokens()
    dump(TOKENS / "color.tokens.json", color_tokens)
    dump(TOKENS / "spacing.tokens.json", build_spacing_tokens())
    dump(TOKENS / "radius.tokens.json", build_radius_tokens())
    dump(TOKENS / "typography.tokens.json", build_typography_tokens())
    dump(TOKENS / "shadow.tokens.json", build_shadow_tokens())
    CSS.parent.mkdir(parents=True, exist_ok=True)
    CSS.write_text(build_css(color_tokens), encoding="utf-8")
    print("Wrote token files and CSS mirror.")


if __name__ == "__main__":
    main()
