#!/usr/bin/env python3
"""Generate assets/compass.svg, the animated README banner. Standard library only.

  scripts/build-banner.py            write assets/compass.svg

The banner has two parts:

  1. Intro (plays once, 3 s): a compass needle swings, overshoots, and settles
     on north; the wordmark and tagline fade in.
  2. Route (loops every 12 s): a marker leaves the compass and walks the main
     flow, lighting each waypoint as it arrives, then the route resets.

Timings live in the constants below. Edit them here and rerun; never hand-edit
the SVG, because the keyframe percentages are derived from these numbers.

The base (unanimated) style is the finished composition, so viewers that
disable motion (prefers-reduced-motion) or don't run SVG CSS see a complete
static banner.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "compass.svg")

# ---- canvas and palette -----------------------------------------------------
W, H = 960, 320
BG, BG2 = "#0b1622", "#10283b"
GRID, CONTOUR = "#132a3d", "#14304a"
DIM, DIMTXT = "#34506a", "#6d879d"
LIT, LITTXT = "#5ec8ff", "#e8f1f8"
GREEN, GREEN_FILL = "#7ee2a8", "#153a2c"
NORTH, SOUTH = "#ff7a59", "#b9c7d6"
TITLE, TAGLINE = "#f2f7fb", "#8fb3cf"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
SANS = "system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"

# ---- compass ----------------------------------------------------------------
CX, CY, R = 130, 232, 64
INTRO = 3.0  # seconds; the route loop starts after the intro

# ---- route ------------------------------------------------------------------
T = 12.0  # route cycle length, seconds
R0 = (CX + R + 14, CY)
NODES = [  # x, y, label, chip text, chip color
    (322, 226, "/probe-with-docs", "in plain terms", LIT),
    (462, 194, "/to-spec", "type: Spec", LIT),
    (602, 238, "/to-tickets", None, LIT),
    (742, 200, "/implement", None, LIT),
    (882, 230, "/code-review", "shipped", GREEN),
]
POINTS = [R0] + [(n[0], n[1]) for n in NODES]
TRAVEL = 1.1
STARTS = [0.5, 2.2, 3.9, 5.6, 7.3]  # when the marker leaves each point
ARRIVE = [s + TRAVEL for s in STARTS]  # 1.6 3.3 5.0 6.7 8.4
FADE_START, FADE_END = 10.6, 11.6


def pct(t):
    return f"{t / T * 100:.3f}%"


def kf(name, frames, period=None):
    """frames: [(t_seconds, 'css props', timing or None)]"""
    p = period or T
    out = [f"@keyframes {name}{{"]
    for t, props, timing in frames:
        tf = f"animation-timing-function:{timing};" if timing else ""
        out.append(f"{t / p * 100:.3f}%{{{props.rstrip(';')};{tf}}}")
    out.append("}")
    return "".join(out)


def ticks():
    parts = []
    for i in range(72):
        deg = i * 5
        if deg % 90 == 0:
            ln, col, w = 13, "#8fb3cf", 2
        elif deg % 45 == 0:
            ln, col, w = 9, "#5d7f9d", 1.6
        elif deg % 15 == 0:
            ln, col, w = 7, "#44637f", 1.3
        else:
            ln, col, w = 4, "#2e475f", 1
        import math

        a = math.radians(deg - 90)
        x1, y1 = CX + (R - 2) * math.cos(a), CY + (R - 2) * math.sin(a)
        x2, y2 = CX + (R - 2 - ln) * math.cos(a), CY + (R - 2 - ln) * math.sin(a)
        parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{col}" stroke-width="{w}"/>'
        )
    return "".join(parts)


def build():
    css = []
    css.append(
        "text{font-family:%s}.mono{font-family:%s}" % (SANS, MONO)
        + ".fx{transform-box:fill-box;transform-origin:center}"
        + "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
    )

    # --- intro: needle settles, wordmark rises (once) ------------------------
    css.append(
        kf(
            "settle",
            [
                (0.00, "transform:rotate(-115deg)", "ease-in-out"),
                (0.54, "transform:rotate(42deg)", "ease-in-out"),
                (1.02, "transform:rotate(-24deg)", "ease-in-out"),
                (1.44, "transform:rotate(12deg)", "ease-in-out"),
                (1.86, "transform:rotate(-6deg)", "ease-in-out"),
                (2.28, "transform:rotate(2.5deg)", "ease-in-out"),
                (2.7, "transform:rotate(-0.8deg)", "ease-in-out"),
                (3.0, "transform:rotate(0deg)", None),
            ],
            period=3.0,
        )
    )
    css.append(
        "@keyframes sway{from{transform:rotate(-1.3deg)}to{transform:rotate(1.3deg)}}"
        "@keyframes rise{from{opacity:0;transform:translateY(10px)}"
        "to{opacity:1;transform:translateY(0)}}"
    )
    css.append(
        ".needle{transform-origin:%dpx %dpx;animation:settle 3s 1 both}" % (CX, CY)
        + ".sway{transform-origin:%dpx %dpx;animation:sway 4.6s ease-in-out %ss infinite alternate backwards}"
        % (CX, CY, INTRO)
        + ".t1{animation:rise .9s ease-out 1.4s 1 both}.t2{animation:rise .9s ease-out 1.9s 1 both}"
    )

    # --- route cycle ---------------------------------------------------------
    def cyc(name, extra=""):
        return f"animation:{name} {T}s linear {INTRO}s infinite backwards;{extra}"

    # launch pulse around the compass
    css.append(
        kf(
            "pulse",
            [
                (0, "opacity:0;transform:scale(1)", None),
                (0.2, "opacity:.7;transform:scale(1.05)", "ease-out"),
                (1.1, "opacity:0;transform:scale(1.4)", None),
                (T, "opacity:0;transform:scale(1.4)", None),
            ],
        )
    )
    css.append(".pulse{opacity:0;%s}" % cyc("pulse"))

    # marker
    m = []
    m.append((0, f"transform:translate({POINTS[0][0]}px,{POINTS[0][1]}px) scale(0);opacity:0", "ease-out"))
    m.append((0.5, f"transform:translate({POINTS[0][0]}px,{POINTS[0][1]}px) scale(1);opacity:1", "ease-in-out"))
    for k in range(1, 5):
        x, y = POINTS[k]
        m.append((ARRIVE[k - 1], f"transform:translate({x}px,{y}px) scale(1);opacity:1", "linear"))
        m.append((STARTS[k], f"transform:translate({x}px,{y}px) scale(1);opacity:1", "ease-in-out"))
    x, y = POINTS[5]
    m.append((ARRIVE[4], f"transform:translate({x}px,{y}px) scale(1);opacity:1", "ease-in"))
    m.append((8.9, f"transform:translate({x}px,{y}px) scale(0);opacity:0", None))
    m.append((T, f"transform:translate({x}px,{y}px) scale(0);opacity:0", None))
    css.append(kf("marker", m))
    css.append(".marker{opacity:0;transform:translate(%dpx,%dpx) scale(0);%s}" % (POINTS[5][0], POINTS[5][1], cyc("marker")))

    # progress segments
    for k in range(5):
        s, e = STARTS[k], ARRIVE[k]
        css.append(
            kf(
                f"seg{k}",
                [
                    (0, "stroke-dashoffset:1;opacity:1", None),
                    (s, "stroke-dashoffset:1;opacity:1", "ease-in-out"),
                    (e, "stroke-dashoffset:0;opacity:1", None),
                    (FADE_START, "stroke-dashoffset:0;opacity:1", None),
                    (FADE_END, "stroke-dashoffset:0;opacity:0", None),
                    (T, "stroke-dashoffset:0;opacity:0", None),
                ],
            )
        )
        css.append(f".seg{k}{{{cyc(f'seg{k}')}}}")

    # nodes, labels, ripples, chips
    for k, (x, y, label, chip, color) in enumerate(NODES):
        a = ARRIVE[k]
        lit_stroke = color
        lit_fill = GREEN_FILL if color == GREEN else "#15405a"
        css.append(
            kf(
                f"node{k}",
                [
                    (0, f"stroke:{DIM};fill:{BG}", None),
                    (a - 0.05, f"stroke:{DIM};fill:{BG}", None),
                    (a + 0.25, f"stroke:{lit_stroke};fill:{lit_fill}", None),
                    (FADE_START, f"stroke:{lit_stroke};fill:{lit_fill}", None),
                    (FADE_END, f"stroke:{DIM};fill:{BG}", None),
                    (T, f"stroke:{DIM};fill:{BG}", None),
                ],
            )
        )
        css.append(f".node{k}{{{cyc(f'node{k}')}}}")
        css.append(
            kf(
                f"lab{k}",
                [
                    (0, f"fill:{DIMTXT}", None),
                    (a - 0.05, f"fill:{DIMTXT}", None),
                    (a + 0.25, f"fill:{LITTXT}", None),
                    (FADE_START, f"fill:{LITTXT}", None),
                    (FADE_END, f"fill:{DIMTXT}", None),
                    (T, f"fill:{DIMTXT}", None),
                ],
            )
        )
        css.append(f".lab{k}{{{cyc(f'lab{k}')}}}")
        css.append(
            kf(
                f"rip{k}",
                [
                    (0, "opacity:0;transform:scale(1)", None),
                    (a, "opacity:.9;transform:scale(1)", "ease-out"),
                    (a + 0.7, "opacity:0;transform:scale(2.8)", None),
                    (T, "opacity:0;transform:scale(2.8)", None),
                ],
            )
        )
        css.append(f".rip{k}{{opacity:0;{cyc(f'rip{k}')}}}")
        if chip:
            css.append(
                kf(
                    f"chip{k}",
                    [
                        (0, "opacity:0;transform:scale(.6)", None),
                        (a + 0.1, "opacity:0;transform:scale(.6)", "ease-out"),
                        (a + 0.45, "opacity:1;transform:scale(1)", None),
                        (FADE_START, "opacity:1;transform:scale(1)", None),
                        (FADE_END, "opacity:0;transform:scale(1)", None),
                        (T, "opacity:0;transform:scale(1)", None),
                    ],
                )
            )
            css.append(f".chip{k}{{{cyc(f'chip{k}')}}}")

    # check mark inside the last node
    ca = ARRIVE[4] + 0.2
    css.append(
        kf(
            "check",
            [
                (0, "stroke-dashoffset:1;opacity:1", None),
                (ca, "stroke-dashoffset:1;opacity:1", "ease-out"),
                (ca + 0.5, "stroke-dashoffset:0;opacity:1", None),
                (FADE_START, "stroke-dashoffset:0;opacity:1", None),
                (FADE_END, "stroke-dashoffset:0;opacity:0", None),
                (T, "stroke-dashoffset:0;opacity:0", None),
            ],
        )
    )
    css.append(".check{%s}" % cyc("check"))

    # --- markup --------------------------------------------------------------
    body = []
    body.append(
        f'<defs>'
        f'<pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse">'
        f'<path d="M40 0H0V40" fill="none" stroke="{GRID}" stroke-width="1"/></pattern>'
        f'<radialGradient id="glow" cx="50%" cy="50%" r="50%">'
        f'<stop offset="0" stop-color="#1f5f8b" stop-opacity=".45"/>'
        f'<stop offset="1" stop-color="#1f5f8b" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="vig" cx="25%" cy="30%" r="90%">'
        f'<stop offset="0" stop-color="#16324a" stop-opacity=".55"/>'
        f'<stop offset="1" stop-color="{BG}" stop-opacity="0"/></radialGradient>'
        f'<clipPath id="card"><rect width="{W}" height="{H}" rx="16"/></clipPath></defs>'
    )
    body.append(f'<g clip-path="url(#card)">')
    body.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    body.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')
    body.append(f'<rect width="{W}" height="{H}" fill="url(#g)"/>')
    # faint contour lines, for the map feel
    for d in (
        "M-20 290 C 180 240, 330 330, 520 280 S 820 250, 980 300",
        "M-20 318 C 220 280, 380 350, 560 306 S 840 280, 980 330",
        "M300 -10 C 380 60, 520 40, 600 -10",
        "M560 -10 C 660 90, 820 60, 900 -10",
    ):
        body.append(f'<path d="{d}" fill="none" stroke="{CONTOUR}" stroke-width="1.2"/>')

    # title
    body.append(
        f'<text class="t1" x="48" y="72" font-size="44" font-weight="700" '
        f'letter-spacing=".5" fill="{TITLE}">Compass</text>'
    )
    body.append(
        f'<text class="t2" x="50" y="100" font-size="17" fill="{TAGLINE}">'
        f"Skills that take work from idea to shipped code</text>"
    )

    # compass
    body.append(f'<circle cx="{CX}" cy="{CY}" r="110" fill="url(#glow)"/>')
    body.append(f'<circle class="pulse fx" cx="{CX}" cy="{CY}" r="{R + 8}" fill="none" stroke="{LIT}" stroke-width="2"/>')
    body.append(f'<circle cx="{CX}" cy="{CY}" r="{R + 8}" fill="none" stroke="#1c3248" stroke-width="1"/>')
    body.append(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="{BG}" fill-opacity=".6" stroke="#2f4a63" stroke-width="2"/>')
    body.append(ticks())
    body.append(
        f'<text x="{CX}" y="{CY - R - 13}" text-anchor="middle" font-size="13" '
        f'font-weight="700" fill="{NORTH}">N</text>'
    )
    body.append(
        f'<g class="needle"><g class="sway">'
        f'<polygon points="{CX},{CY - 46} {CX - 9},{CY} {CX + 9},{CY}" fill="{NORTH}"/>'
        f'<polygon points="{CX},{CY + 46} {CX - 9},{CY} {CX + 9},{CY}" fill="{SOUTH}"/>'
        f'<circle cx="{CX}" cy="{CY}" r="4.5" fill="{BG}" stroke="{LITTXT}" stroke-width="1.5"/>'
        f"</g></g>"
    )

    # planned route (always visible, dotted) then progress (solid, animated)
    pts = " ".join(f"{x},{y}" for x, y in POINTS)
    body.append(
        f'<polyline points="{pts}" fill="none" stroke="{DIM}" stroke-width="3" '
        f'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="0.1 9"/>'
    )
    for k in range(5):
        (x1, y1), (x2, y2) = POINTS[k], POINTS[k + 1]
        body.append(
            f'<path class="seg{k}" d="M{x1} {y1}L{x2} {y2}" pathLength="1" fill="none" '
            f'stroke="{GREEN if k == 4 else LIT}" stroke-width="3" stroke-linecap="round" '
            f'stroke-dasharray="1 2" stroke-dashoffset="0"/>'
        )

    # nodes
    for k, (x, y, label, chip, color) in enumerate(NODES):
        lit_fill = GREEN_FILL if color == GREEN else "#15405a"
        body.append(
            f'<circle class="rip{k} fx" cx="{x}" cy="{y}" r="9" fill="none" stroke="{color}" stroke-width="2"/>'
        )
        body.append(
            f'<circle class="node{k}" cx="{x}" cy="{y}" r="9" fill="{lit_fill}" stroke="{color}" stroke-width="2.5"/>'
        )
        body.append(
            f'<text class="lab{k} mono" x="{x}" y="{y + 36}" text-anchor="middle" '
            f'font-size="13" fill="{LITTXT}">{label}</text>'
        )
        if chip:
            cw = len(chip) * 7.4 + 24
            cy = y - 46
            body.append(
                f'<g class="chip{k} fx">'
                f'<rect x="{x - cw / 2:.1f}" y="{cy - 12}" width="{cw:.1f}" height="24" rx="12" '
                f'fill="{BG2}" stroke="{color}" stroke-width="1.2"/>'
                f'<text class="mono" x="{x}" y="{cy + 4}" text-anchor="middle" font-size="12" fill="{color}">{chip}</text>'
                f"</g>"
            )

    # check mark, last node
    lx, ly = NODES[4][0], NODES[4][1]
    body.append(
        f'<path class="check" d="M{lx - 4.5} {ly + 0.5}L{lx - 1.2} {ly + 3.8}L{lx + 4.8} {ly - 3.6}" '
        f'pathLength="1" fill="none" stroke="{GREEN}" stroke-width="2.4" stroke-linecap="round" '
        f'stroke-linejoin="round" stroke-dasharray="1 2" stroke-dashoffset="0"/>'
    )

    # marker (drawn last so it rides on top)
    body.append(
        f'<g class="marker fx"><circle r="13" fill="{LIT}" fill-opacity=".22"/>'
        f'<circle r="5.5" fill="#d8f2ff"/></g>'
    )
    body.append("</g>")

    alt = (
        "Compass: a needle settles on north, then a route runs from /probe-with-docs "
        "through /to-spec, /to-tickets and /implement to /code-review, ending in shipped."
    )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-label="{alt}">'
        f"<title>{alt}</title>"
        f"<style>{''.join(css)}</style>" + "".join(body) + "</svg>\n"
    )
    return svg


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    svg = build()
    open(OUT, "w", encoding="utf-8").write(svg)
    print(f"wrote {os.path.relpath(OUT, ROOT)} ({len(svg) / 1024:.1f} KB)")
