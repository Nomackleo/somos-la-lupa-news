#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for the standalone interactive commercial & investor pitch deck:
  deliverables/pitch_comercial/Presentacion_Pitch_Comercial_Somos_La_Lupa_News.html

Optimizes and Base64-embeds all official brand assets (with clean anti-aliased
alpha extraction for solid-background logos) and real portal captures as WebP.
"""

import base64
import io
import os
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
ASSETS_BRAND = ROOT / "assets" / "branding" / "logos"
ASSETS_CAPTURES = ROOT / "assets" / "captures"
OUT_HTML = ROOT / "deliverables" / "pitch_comercial" / "Presentacion_Pitch_Comercial_Somos_La_Lupa_News.html"


def extract_monochrome_alpha(img_path: Path, bg_rgb: tuple, fg_rgb: tuple, max_width: int, pad: int = 12) -> str:
    """Convert a two-tone solid-background PNG into a crisp anti-aliased RGBA PNG and return data URI."""
    im = Image.open(img_path).convert("RGB")
    arr = np.array(im, dtype=np.float32)

    bg = np.array(bg_rgb, dtype=np.float32)
    fg = np.array(fg_rgb, dtype=np.float32)
    diff = fg - bg
    denom = float(np.dot(diff, diff))

    # Project each pixel onto the vector from bg to fg for smooth anti-aliased alpha
    proj = np.sum((arr - bg) * diff, axis=2) / denom
    alpha = np.clip(proj, 0.0, 1.0)
    # Remove tiny noise near 0 and snap near 1
    alpha = np.where(alpha < 0.02, 0.0, alpha)
    alpha = np.where(alpha > 0.98, 1.0, alpha)

    rgba = np.zeros((arr.shape[0], arr.shape[1], 4), dtype=np.uint8)
    rgba[..., 0] = int(fg_rgb[0])
    rgba[..., 1] = int(fg_rgb[1])
    rgba[..., 2] = int(fg_rgb[2])
    rgba[..., 3] = np.round(alpha * 255.0).astype(np.uint8)

    out = Image.fromarray(rgba, mode="RGBA")
    bbox = out.getbbox()
    if bbox:
        x0 = max(0, bbox[0] - pad)
        y0 = max(0, bbox[1] - pad)
        x1 = min(out.width, bbox[2] + pad)
        y1 = min(out.height, bbox[3] + pad)
        out = out.crop((x0, y0, x1, y1))

    if out.width > max_width:
        ratio = max_width / out.width
        out = out.resize((max_width, max(1, int(round(out.height * ratio)))), Image.Resampling.LANCZOS)

    buf = io.BytesIO()
    out.save(buf, format="PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}", len(buf.getvalue()), out.size


def encode_rgba_png(img_path: Path, max_width: int, trim: bool = True, pad: int = 10) -> str:
    """Resize and optimize an already-transparent PNG into Base64 data URI."""
    im = Image.open(img_path).convert("RGBA")
    if trim:
        bbox = im.getbbox()
        if bbox:
            x0 = max(0, bbox[0] - pad)
            y0 = max(0, bbox[1] - pad)
            x1 = min(im.width, bbox[2] + pad)
            y1 = min(im.height, bbox[3] + pad)
            im = im.crop((x0, y0, x1, y1))
    if im.width > max_width:
        ratio = max_width / im.width
        im = im.resize((max_width, max(1, int(round(im.height * ratio)))), Image.Resampling.LANCZOS)

    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}", len(buf.getvalue()), im.size


def encode_webp_capture(img_path: Path, max_width: int, quality: int) -> str:
    """Resize and encode a screenshot capture as high-fidelity Base64 WebP."""
    im = Image.open(img_path).convert("RGB")
    if im.width > max_width:
        ratio = max_width / im.width
        im = im.resize((max_width, max(1, int(round(im.height * ratio)))), Image.Resampling.LANCZOS)

    buf = io.BytesIO()
    im.save(buf, format="WEBP", quality=quality, method=6)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/webp;base64,{b64}", len(buf.getvalue()), im.size


def build_assets() -> dict:
    assets = {}
    stats = []

    # 1. Brand logos (SSOT in assets/branding/logos/, clean alpha extraction so ZERO box artifacts!)
    uri, sz, dim = extract_monochrome_alpha(
        ASSETS_BRAND / "Logo 2.png",
        bg_rgb=(5, 41, 98),
        fg_rgb=(255, 255, 255),
        max_width=520,
    )
    assets["LOGO_WHITE"] = uri
    stats.append(("Logo 2 (navy bg) -> white RGBA", dim, sz))

    uri, sz, dim = extract_monochrome_alpha(
        ASSETS_BRAND / "Logo 1.png",
        bg_rgb=(255, 255, 255),
        fg_rgb=(5, 41, 98),
        max_width=480,
    )
    assets["LOGO_NAVY"] = uri
    stats.append(("Logo 1 (white bg) -> navy RGBA", dim, sz))

    uri, sz, dim = encode_rgba_png(ASSETS_BRAND / "Imago favi2.png", max_width=180, trim=True)
    assets["IMAGO_WHITE"] = uri
    stats.append(("Imago favi2 -> white RGBA", dim, sz))

    uri, sz, dim = extract_monochrome_alpha(
        ASSETS_BRAND / "Imago 1.png",
        bg_rgb=(255, 255, 255),
        fg_rgb=(5, 41, 98),
        max_width=180,
    )
    assets["IMAGO_NAVY"] = uri
    stats.append(("Imago 1 -> navy RGBA", dim, sz))

    uri, sz, dim = encode_rgba_png(ASSETS_BRAND / "favicon.png", max_width=128, trim=False)
    assets["FAVICON"] = uri
    stats.append(("favicon -> RGBA", dim, sz))

    # 2. Portal real captures (Base64 WebP — ultra-crisp Retina fidelity)
    capture_specs = [
        ("CAP_DESKTOP", "01_portada_desktop.png", 1440, 88),
        ("CAP_TRM", "03_trm_widget.png", 1440, 92),
        ("CAP_ARTICLE", "04_articulo_o_seccion.png", 1440, 88),
        ("CAP_MOBILE", "05_portada_mobile.png", 580, 88),
        ("CAP_FULL", "02_portada_full.png", 1120, 84),
    ]
    for key, fname, max_w, qual in capture_specs:
        uri, sz, dim = encode_webp_capture(ASSETS_CAPTURES / fname, max_width=max_w, quality=qual)
        assets[key] = uri
        stats.append((f"{fname} -> WebP q={qual}", dim, sz))

    print("Asset optimization summary:")
    total_raw = 0
    for label, dim, sz in stats:
        total_raw += sz
        print(f"  - {label:42s} {str(dim):14s} {sz/1024:7.1f} KB")
    print(f"  Total embedded binary payload: {total_raw/1024:.1f} KB (Base64 ~{total_raw*1.34/1024:.1f} KB)")
    return assets


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Somos La Lupa News — Pitch Comercial y de Inversión 2026</title>
<meta name="description" content="Presentación comercial y de inversión de Somos La Lupa News (somoslalupanews.com): ecosistema editorial colombiano, patrocinio exclusivo del indicador diario TRM, formatos de alto recuerdo y resultados medibles.">
<link rel="icon" type="image/png" href="__FAVICON__">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Funnel+Sans:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,700;0,800;1,700&family=Source+Serif+4:ital,wght@0,400;0,600;1,400;1,600&display=swap" rel="stylesheet">
<style>
/* ==========================================================================
   SISTEMA DE DISEÑO EDITORIAL — SOMOS LA LUPA NEWS (somoslalupanews.com)
   Paleta oficial del medio: #052962 · #041F4A · #02132F · #346E9B · #AA5959 · #B9AF07
   Tipografía: Playfair Display · Source Serif 4 · Funnel Sans
   ========================================================================== */
:root {
  --navy: #052962;
  --navy-deep: #041F4A;
  --navy-mid: #0A377D;
  --ink: #02132F;
  --editorial-blue: #346E9B;
  --terracotta: #AA5959;
  --terracotta-soft: rgba(170, 89, 89, 0.12);
  --olive: #B9AF07;
  --olive-bright: #D4C914;
  --olive-dark: #7A7304;
  --olive-soft: rgba(185, 175, 7, 0.14);
  --slate: #2E3C46;
  --paper: #FFFFFF;
  --surface: #F7F7F7;
  --surface-2: #EEF2F6;
  --border: #DEE2E6;
  --text-sec: #2B2F33;
  --muted: #69727D;

  --on-dark: #FFFFFF;
  --on-dark-2: #D5E2F2;
  --on-dark-muted: #9CB4D4;
  --dark-card: rgba(255, 255, 255, 0.06);
  --dark-border: rgba(255, 255, 255, 0.14);

  --ff-display: "Playfair Display", Georgia, "Times New Roman", serif;
  --ff-serif: "Source Serif 4", Georgia, "Times New Roman", serif;
  --ff-sans: "Funnel Sans", "Segoe UI", system-ui, -apple-system, sans-serif;

  --ease-out: cubic-bezier(0.22, 1, 0.36, 1);
  --ease-expo: cubic-bezier(0.16, 1, 0.3, 1);

  --shell: min(1220px, 92vw);
  --topbar-h: 66px;
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-lg: 18px;
  --shadow-card: 0 10px 30px rgba(2, 19, 47, 0.07);
  --shadow-lg: 0 22px 54px rgba(2, 19, 47, 0.14);
}

*, *::before, *::after {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
  -webkit-text-size-adjust: 100%;
  overflow-x: clip;
}

body {
  margin: 0;
  font-family: var(--ff-sans);
  font-size: 16px;
  line-height: 1.6;
  color: var(--ink);
  background: var(--navy-deep);
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
  overflow-x: clip;
}

img {
  max-width: 100%;
  display: block;
}

button, input {
  font-family: inherit;
}

a {
  color: var(--editorial-blue);
  text-decoration: none;
  transition: color 0.2s ease;
}

a:hover {
  color: var(--navy);
}

::selection {
  background: var(--olive);
  color: var(--ink);
}

/* ==========================================================================
   BARRA DE PROGRESO Y CABECERA FIJA
   ========================================================================== */
.prog {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  width: 0%;
  background: linear-gradient(90deg, var(--olive), var(--olive-bright));
  z-index: 120;
  transition: width 0.12s linear;
}

.topbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  min-height: var(--topbar-h);
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  padding: 10px clamp(14px, 3vw, 32px);
  background: rgba(4, 31, 74, 0.94);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: 0 6px 24px rgba(2, 19, 47, 0.25);
}

.brand-lockup {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  flex-shrink: 0;
}

.brand-lockup img {
  height: 36px;
  width: auto;
  object-fit: contain;
}

.brand-divider {
  width: 1px;
  height: 24px;
  background: rgba(255, 255, 255, 0.22);
}

.brand-caption {
  display: flex;
  flex-direction: column;
  line-height: 1.15;
}

.brand-caption strong {
  color: #FFFFFF;
  font-size: 0.72rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  font-weight: 700;
}

.brand-caption span {
  color: var(--olive-bright);
  font-size: 0.66rem;
  letter-spacing: 0.06em;
  font-weight: 500;
}

/* Selector Dual Persistente */
.profile-switch {
  display: inline-flex;
  align-items: center;
  background: rgba(2, 19, 47, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 999px;
  padding: 3px;
  gap: 2px;
  position: relative;
}

.profile-btn {
  appearance: none;
  border: none;
  background: transparent;
  color: var(--on-dark-2);
  font-size: 0.78rem;
  font-weight: 600;
  padding: 7px 14px;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.24s var(--ease-out);
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.profile-btn:hover {
  color: #FFFFFF;
}

.profile-btn[aria-pressed="true"] {
  background: var(--olive);
  color: var(--ink);
  font-weight: 800;
  box-shadow: 0 3px 12px rgba(185, 175, 7, 0.35);
}

.topbar-tools {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.tool-btn {
  appearance: none;
  border: 1px solid rgba(255, 255, 255, 0.22);
  background: rgba(255, 255, 255, 0.06);
  color: #FFFFFF;
  font-size: 0.74rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  padding: 7px 12px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.22s var(--ease-out);
  white-space: nowrap;
}

.tool-btn:hover,
.tool-btn[aria-pressed="true"] {
  background: var(--olive);
  border-color: var(--olive);
  color: var(--ink);
}

.tool-btn--pdf {
  background: rgba(185, 175, 7, 0.16);
  border-color: rgba(185, 175, 7, 0.55);
  color: #F4EE7B;
}

.tool-btn--pdf:hover {
  background: var(--olive);
  color: var(--ink);
}

/* ==========================================================================
   RAIL LATERAL DE NAVEGACIÓN (7 ACTOS)
   ========================================================================== */
.rail {
  position: fixed;
  right: clamp(10px, 1.5vw, 22px);
  top: 50%;
  transform: translateY(-50%);
  z-index: 80;
  display: flex;
  flex-direction: column;
  gap: 11px;
  padding: 12px 8px;
  border-radius: 999px;
  background: rgba(4, 31, 74, 0.78);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.16);
  box-shadow: 0 8px 24px rgba(2, 19, 47, 0.22);
}

.rail button {
  width: 10px;
  height: 10px;
  padding: 0;
  border-radius: 50%;
  border: 1.5px solid rgba(255, 255, 255, 0.55);
  background: transparent;
  cursor: pointer;
  position: relative;
  transition: all 0.25s var(--ease-out);
}

.rail button:hover {
  border-color: var(--olive-bright);
  transform: scale(1.2);
}

.rail button[aria-current="true"] {
  background: var(--olive);
  border-color: var(--olive);
  transform: scale(1.35);
  box-shadow: 0 0 0 4px rgba(185, 175, 7, 0.24);
}

.rail button::after {
  content: attr(data-label);
  position: absolute;
  right: 22px;
  top: 50%;
  transform: translateY(-50%) translateX(6px);
  opacity: 0;
  pointer-events: none;
  white-space: nowrap;
  background: var(--navy-deep);
  color: #FFFFFF;
  border: 1px solid rgba(185, 175, 7, 0.55);
  font-size: 0.72rem;
  font-weight: 600;
  padding: 5px 10px;
  border-radius: var(--radius-sm);
  box-shadow: 0 6px 18px rgba(2, 19, 47, 0.35);
  transition: all 0.2s ease;
}

.rail button:hover::after,
.rail button:focus-visible::after {
  opacity: 1;
  transform: translateY(-50%) translateX(0);
}

/* ==========================================================================
   ESTRUCTURA DE ACTOS / DIAPOSITIVAS
   ========================================================================== */
#track {
  display: block;
}

.slide {
  position: relative;
  padding: clamp(92px, 11vh, 130px) 0 clamp(64px, 8vh, 102px);
  overflow: hidden;
}

.slide--navy {
  background: linear-gradient(155deg, #052962 0%, #041F4A 62%, #02132F 100%);
  color: var(--on-dark);
}

.slide--paper {
  background: var(--paper);
  color: var(--ink);
  border-bottom: 1px solid var(--border);
}

.slide--surface {
  background: var(--surface);
  color: var(--ink);
  border-bottom: 1px solid var(--border);
}

.shell {
  width: var(--shell);
  margin-inline: auto;
  position: relative;
  z-index: 2;
}

/* Tipografía de Actos */
.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: 0.74rem;
  font-weight: 800;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  margin-bottom: 14px;
}

.slide--navy .eyebrow {
  color: var(--olive-bright);
}

.slide--paper .eyebrow,
.slide--surface .eyebrow {
  color: var(--terracotta);
}

.eyebrow::before {
  content: "";
  width: 24px;
  height: 2px;
  background: currentColor;
  display: inline-block;
}

.act-title {
  font-family: var(--ff-display);
  font-weight: 800;
  font-size: clamp(1.9rem, 3.6vw, 3rem);
  line-height: 1.12;
  letter-spacing: -0.015em;
  margin: 0 0 16px;
}

.slide--navy .act-title {
  color: #FFFFFF;
}

.slide--paper .act-title,
.slide--surface .act-title {
  color: var(--navy);
}

.act-lead {
  font-family: var(--ff-serif);
  font-size: clamp(1.06rem, 1.45vw, 1.24rem);
  line-height: 1.62;
  max-width: 72ch;
  margin: 0 0 32px;
}

.slide--navy .act-lead {
  color: var(--on-dark-2);
}

.slide--paper .act-lead,
.slide--surface .act-lead {
  color: var(--slate);
}

.section-rule {
  width: 64px;
  height: 3px;
  background: var(--terracotta);
  margin: 0 0 26px;
  border-radius: 2px;
}

.slide--navy .section-rule {
  background: var(--olive);
}

/* Revelado Dinámico */
.rv {
  opacity: 0;
  transform: translateY(22px);
  transition: opacity 0.68s var(--ease-out), transform 0.75s var(--ease-out);
}
.rv.on {
  opacity: 1;
  transform: none;
}
.rv-d1 { transition-delay: 0.06s; }
.rv-d2 { transition-delay: 0.12s; }
.rv-d3 { transition-delay: 0.18s; }
.rv-d4 { transition-delay: 0.24s; }

/* Botones Generales */
.cta-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  font-size: 0.92rem;
  font-weight: 700;
  padding: 13px 22px;
  border-radius: var(--radius-sm);
  border: 2px solid transparent;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.25s var(--ease-out);
}

.cta-btn--olive {
  background: var(--olive);
  color: var(--ink);
  border-color: var(--olive);
  box-shadow: 0 8px 24px rgba(185, 175, 7, 0.28);
}

.cta-btn--olive:hover {
  background: var(--olive-bright);
  border-color: var(--olive-bright);
  color: var(--ink);
  transform: translateY(-2px);
}

.cta-btn--ghost-light {
  background: rgba(255, 255, 255, 0.08);
  color: #FFFFFF;
  border-color: rgba(255, 255, 255, 0.35);
}

.cta-btn--ghost-light:hover {
  background: #FFFFFF;
  color: var(--navy);
  border-color: #FFFFFF;
  transform: translateY(-2px);
}

.cta-btn--navy {
  background: var(--navy);
  color: #FFFFFF;
  border-color: var(--navy);
}

.cta-btn--navy:hover {
  background: var(--navy-mid);
  border-color: var(--navy-mid);
  color: #FFFFFF;
  transform: translateY(-2px);
}

.cta-btn--active-route {
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.3), 0 10px 26px rgba(185, 175, 7, 0.35);
}

/* ==========================================================================
   ACTO 1 — HERO DE ALTO IMPACTO
   ========================================================================== */
#act-1 {
  min-height: 100dvh;
  display: flex;
  align-items: center;
  padding-top: calc(var(--topbar-h) + 38px);
  padding-bottom: 72px;
}

.hero-grid-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0.32;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.08) 1px, transparent 1px);
  background-size: 56px 56px;
  mask-image: radial-gradient(85% 70% at 50% 35%, #000 18%, transparent 80%);
  -webkit-mask-image: radial-gradient(85% 70% at 50% 35%, #000 18%, transparent 80%);
}

.hero-glow {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    radial-gradient(620px 420px at 84% 18%, rgba(52, 110, 155, 0.38) 0%, transparent 70%),
    radial-gradient(500px 360px at 12% 85%, rgba(170, 89, 89, 0.18) 0%, transparent 72%);
  animation: ambientShift 12s ease-in-out infinite alternate;
}

@keyframes ambientShift {
  0% { opacity: 0.85; transform: scale(1); }
  100% { opacity: 1; transform: scale(1.04); }
}

.hero-watermark {
  position: absolute;
  right: -30px;
  bottom: -20px;
  width: clamp(220px, 28vw, 390px);
  opacity: 0.055;
  pointer-events: none;
  user-select: none;
}

.hero-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 24px;
}

.hero-logo-badge {
  display: inline-flex;
  align-items: center;
  gap: 16px;
}

.hero-logo-badge img {
  height: clamp(54px, 7vw, 76px);
  width: auto;
}

.live-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  border-radius: 999px;
  background: rgba(170, 89, 89, 0.22);
  border: 1px solid rgba(170, 89, 89, 0.65);
  color: #FFDCDC;
  font-size: 0.74rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.live-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #FF7E7E;
  box-shadow: 0 0 0 0 rgba(255, 126, 126, 0.7);
  animation: pulseDot 1.8s infinite;
}

@keyframes pulseDot {
  0% { box-shadow: 0 0 0 0 rgba(255, 126, 126, 0.75); }
  70% { box-shadow: 0 0 0 10px rgba(255, 126, 126, 0); }
  100% { box-shadow: 0 0 0 0 rgba(255, 126, 126, 0); }
}

.hero-h1 {
  font-family: var(--ff-display);
  font-weight: 800;
  font-size: clamp(2rem, 4.3vw, 3.65rem);
  line-height: 1.1;
  color: #FFFFFF;
  margin: 0 0 20px;
  max-width: 24ch;
}

.hero-h1 .hl {
  color: var(--olive-bright);
}

.hero-subtitle {
  font-family: var(--ff-serif);
  font-size: clamp(1.06rem, 1.55vw, 1.32rem);
  line-height: 1.58;
  color: var(--on-dark-2);
  max-width: 68ch;
  margin: 0 0 28px;
}

.hero-subtitle strong {
  color: #FFFFFF;
}

.hero-route-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
  margin-bottom: 36px;
}

.hero-kpis {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.kpi-box {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-top: 3px solid var(--olive);
  border-radius: var(--radius-md);
  padding: 20px 18px;
  transition: transform 0.25s var(--ease-out), border-color 0.25s ease, background 0.25s ease;
}

.kpi-box:hover {
  transform: translateY(-4px);
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(185, 175, 7, 0.65);
}

.kpi-box--terracotta {
  border-top-color: var(--terracotta);
}

.kpi-val {
  font-family: var(--ff-display);
  font-weight: 800;
  font-size: clamp(1.7rem, 2.7vw, 2.35rem);
  line-height: 1.05;
  color: #FFFFFF;
  margin-bottom: 6px;
  font-variant-numeric: tabular-nums;
}

.kpi-val .accent-num {
  color: var(--olive-bright);
}

.kpi-lbl {
  font-size: 0.84rem;
  font-weight: 700;
  color: #FFFFFF;
  margin-bottom: 3px;
}

.kpi-sub {
  font-size: 0.76rem;
  color: var(--on-dark-muted);
  line-height: 1.38;
}

.scroll-cue {
  position: absolute;
  bottom: 18px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  font-size: 0.68rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--on-dark-muted);
  z-index: 3;
}

.scroll-cue span {
  white-space: nowrap;
}

.scroll-cue i {
  width: 2px;
  height: 22px;
  background: linear-gradient(var(--olive), transparent);
  display: block;
  animation: cueDrop 2s infinite;
}

@keyframes cueDrop {
  0% { transform: scaleY(0); transform-origin: top; }
  50% { transform: scaleY(1); transform-origin: top; }
  51% { transform-origin: bottom; }
  100% { transform: scaleY(0); transform-origin: bottom; }
}

/* ==========================================================================
   ACTO 2 — PULSO DEL MERCADO COLOMBIA 2025-2026
   ========================================================================== */
.stat-grid-4 {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 18px;
  margin-bottom: 32px;
}

.editorial-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 22px 20px;
  transition: transform 0.25s var(--ease-out), box-shadow 0.25s ease, border-color 0.25s ease;
}

.editorial-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-card);
  border-color: var(--editorial-blue);
}

.editorial-card--alert {
  border-top: 3px solid var(--terracotta);
  background: #FFFDFD;
}

.editorial-card--primary {
  border-top: 3px solid var(--navy);
}

.editorial-card--blue {
  border-top: 3px solid var(--editorial-blue);
}

.editorial-card--olive {
  border-top: 3px solid var(--olive);
}

.stat-big {
  font-family: var(--ff-display);
  font-weight: 800;
  font-size: clamp(1.85rem, 2.8vw, 2.45rem);
  line-height: 1.05;
  color: var(--editorial-blue);
  margin-bottom: 8px;
  font-variant-numeric: tabular-nums;
}

.editorial-card--alert .stat-big {
  color: var(--terracotta);
}

.editorial-card h3 {
  font-size: 0.96rem;
  font-weight: 700;
  color: var(--ink);
  margin: 0 0 6px;
}

.editorial-card p {
  font-size: 0.86rem;
  color: var(--slate);
  margin: 0;
  line-height: 1.5;
}

.market-split {
  display: grid;
  grid-template-columns: 1.25fr 1fr;
  gap: 24px;
  align-items: stretch;
}

.chart-panel {
  background: var(--paper);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 26px;
  box-shadow: var(--shadow-card);
}

.chart-panel-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border);
}

.chart-panel-head h3 {
  font-family: var(--ff-display);
  font-size: 1.25rem;
  color: var(--navy);
  margin: 0;
}

.chart-tag {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--terracotta);
  background: var(--terracotta-soft);
  padding: 4px 10px;
  border-radius: 999px;
}

.bar-row {
  margin-bottom: 16px;
}

.bar-row:last-child {
  margin-bottom: 0;
}

.bar-meta {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  font-size: 0.88rem;
  margin-bottom: 6px;
  gap: 8px;
}

.bar-meta strong {
  color: var(--ink);
}

.bar-meta .bar-pct {
  font-weight: 800;
  color: var(--navy);
  font-variant-numeric: tabular-nums;
}

.bar-meta .bar-pct--hot {
  color: var(--terracotta);
  font-size: 1rem;
}

.bar-track {
  height: 14px;
  background: var(--surface-2);
  border-radius: 999px;
  overflow: hidden;
  position: relative;
}

.bar-fill {
  height: 100%;
  width: 0;
  border-radius: 999px;
  transition: width 1.1s var(--ease-expo);
}

.bar-fill--hot { background: linear-gradient(90deg, var(--terracotta), #C96B6B); }
.bar-fill--blue { background: linear-gradient(90deg, var(--navy), var(--editorial-blue)); }
.bar-fill--mid { background: linear-gradient(90deg, var(--editorial-blue), #5A93BD); }
.bar-fill--olive { background: linear-gradient(90deg, var(--olive-dark), var(--olive)); }

.bar-sub {
  font-size: 0.76rem;
  color: var(--muted);
  margin-top: 4px;
}

.paradox-card {
  background: linear-gradient(160deg, var(--navy) 0%, var(--navy-deep) 100%);
  color: #FFFFFF;
  border-radius: var(--radius-md);
  padding: 28px 26px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-lg);
}

.paradox-card::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--terracotta), var(--olive));
}

.paradox-badge {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--olive-bright);
  margin-bottom: 12px;
}

.paradox-card h3 {
  font-family: var(--ff-display);
  font-size: 1.48rem;
  line-height: 1.22;
  margin: 0 0 14px;
  color: #FFFFFF;
}

.paradox-card p {
  font-size: 0.93rem;
  color: var(--on-dark-2);
  margin: 0 0 18px;
  line-height: 1.58;
}

.paradox-lens {
  background: rgba(255, 255, 255, 0.08);
  border-left: 3px solid var(--olive);
  padding: 14px 16px;
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  font-size: 0.88rem;
  color: #FFFFFF;
}

.paradox-lens strong {
  color: var(--olive-bright);
  display: block;
  font-size: 0.74rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 4px;
}

.source-footnote {
  margin-top: 22px;
  font-size: 0.76rem;
  color: var(--muted);
  border-top: 1px solid var(--border);
  padding-top: 12px;
}

/* ==========================================================================
   ACTO 3 — COMPARADOR INTERACTIVO ANTES / DESPUÉS
   ========================================================================== */
.compare-controls {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  background: var(--paper);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 16px 20px;
  margin-bottom: 26px;
  box-shadow: var(--shadow-card);
}

.toggle-track {
  display: inline-flex;
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 4px;
  gap: 4px;
}

.toggle-opt {
  appearance: none;
  border: none;
  background: transparent;
  color: var(--slate);
  font-size: 0.86rem;
  font-weight: 700;
  padding: 10px 18px;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.25s var(--ease-out);
}

.toggle-opt.is-before[aria-pressed="true"] {
  background: var(--terracotta);
  color: #FFFFFF;
  box-shadow: 0 4px 14px rgba(170, 89, 89, 0.32);
}

.toggle-opt.is-after[aria-pressed="true"] {
  background: var(--navy);
  color: #FFFFFF;
  box-shadow: 0 4px 14px rgba(5, 41, 98, 0.32);
}

.compare-meter {
  display: flex;
  align-items: center;
  gap: 14px;
  min-width: 240px;
}

.compare-meter-label {
  font-size: 0.76rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--slate);
}

.compare-meter-bar {
  width: 130px;
  height: 10px;
  background: var(--surface-2);
  border-radius: 999px;
  overflow: hidden;
}

.compare-meter-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.5s var(--ease-out), background 0.4s ease;
}

.compare-meter-score {
  font-family: var(--ff-display);
  font-weight: 800;
  font-size: 1.15rem;
  color: var(--navy);
}

.pillars-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 16px;
}

.pillar-card {
  background: var(--paper);
  border: 1px solid var(--border);
  border-top: 4px solid var(--navy);
  border-radius: var(--radius-md);
  padding: 22px 18px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: all 0.35s var(--ease-out);
  box-shadow: var(--shadow-card);
}

.pillar-card.state-before {
  border-top-color: var(--terracotta);
  background: #FFFBFB;
}

.pillar-card.state-after {
  border-top-color: var(--navy);
  background: #FFFFFF;
}

.pillar-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.pillar-num {
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--editorial-blue);
  margin-bottom: 8px;
}

.pillar-card.state-before .pillar-num {
  color: var(--terracotta);
}

.pillar-card h3 {
  font-family: var(--ff-display);
  font-size: 1.1rem;
  line-height: 1.25;
  color: var(--ink);
  margin: 0 0 10px;
}

.pillar-body {
  font-size: 0.86rem;
  color: var(--slate);
  line-height: 1.52;
  margin: 0 0 16px;
  flex: 1;
}

.pillar-metric {
  padding-top: 12px;
  border-top: 1px solid var(--border);
  font-size: 0.78rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: 6px;
}

.pillar-card.state-before .pillar-metric {
  color: var(--terracotta);
}

.pillar-card.state-after .pillar-metric {
  color: var(--navy);
}

.compare-bottom-note {
  margin-top: 22px;
  background: var(--navy);
  color: #FFFFFF;
  border-radius: var(--radius-md);
  padding: 18px 22px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.compare-bottom-note p {
  margin: 0;
  font-size: 0.92rem;
  color: var(--on-dark-2);
  max-width: 76ch;
}

.compare-bottom-note strong {
  color: var(--olive-bright);
}

/* ==========================================================================
   ACTO 4 — VITRINA VIVA CON HOTSPOTS + JOYA ESTELAR TRM
   ========================================================================== */
.showcase-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 22px;
}

.view-tab {
  appearance: none;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--slate);
  font-size: 0.85rem;
  font-weight: 700;
  padding: 11px 18px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.22s var(--ease-out);
}

.view-tab:hover {
  border-color: var(--navy);
  color: var(--navy);
}

.view-tab[aria-selected="true"] {
  background: var(--navy);
  border-color: var(--navy);
  color: #FFFFFF;
  box-shadow: 0 6px 18px rgba(5, 41, 98, 0.24);
}

.view-tab .tab-badge {
  font-size: 0.68rem;
  font-weight: 800;
  padding: 2px 7px;
  border-radius: 999px;
  background: rgba(5, 41, 98, 0.1);
  color: var(--navy);
}

.view-tab[aria-selected="true"] .tab-badge {
  background: var(--olive);
  color: var(--ink);
}

.showcase-stage {
  display: grid;
  grid-template-columns: minmax(0, 1.55fr) minmax(300px, 0.95fr);
  gap: 24px;
  align-items: start;
  margin-bottom: 34px;
}

.browser-frame {
  background: var(--navy-deep);
  border-radius: var(--radius-md);
  border: 2px solid var(--navy);
  overflow: hidden;
  box-shadow: var(--shadow-lg);
}

.browser-chrome {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 10px 14px;
  background: var(--navy-deep);
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
}

.browser-dots {
  display: flex;
  gap: 6px;
}

.browser-dots i {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  display: block;
}
.browser-dots i:nth-child(1) { background: #E36B6B; }
.browser-dots i:nth-child(2) { background: var(--olive); }
.browser-dots i:nth-child(3) { background: #4DA870; }

.browser-url {
  flex: 1;
  max-width: 420px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 999px;
  padding: 4px 14px;
  font-size: 0.74rem;
  color: var(--on-dark-2);
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.browser-hint {
  font-size: 0.7rem;
  color: var(--olive-bright);
  font-weight: 700;
  white-space: nowrap;
}

.capture-canvas {
  position: relative;
  background: #FFFFFF;
  line-height: 0;
}

.capture-canvas img {
  width: 100%;
  height: auto;
  display: block;
}

/* Marco Móvil para Pestaña 3 */
.mobile-stage-bg {
  background: linear-gradient(145deg, #EEF2F6 0%, #DCE5F0 100%);
  padding: 26px 16px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.phone-bezel {
  width: min(330px, 100%);
  background: #0B1424;
  border-radius: 34px;
  padding: 12px;
  box-shadow: 0 24px 48px rgba(2, 19, 47, 0.28);
  border: 2px solid #243857;
}

.phone-notch {
  width: 96px;
  height: 16px;
  background: #0B1424;
  border-radius: 0 0 12px 12px;
  margin: 0 auto 6px;
}

.phone-screen {
  border-radius: 22px;
  overflow: hidden;
  position: relative;
  background: #FFFFFF;
}

/* Scroll controlado para Pestaña 4 (Portada Completa) */
.fullpage-toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 10px 14px;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
}

.jump-btn {
  appearance: none;
  border: 1px solid var(--border);
  background: #FFFFFF;
  color: var(--navy);
  font-size: 0.74rem;
  font-weight: 700;
  padding: 5px 11px;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.jump-btn:hover {
  background: var(--navy);
  color: #FFFFFF;
  border-color: var(--navy);
}

.fullpage-scroll {
  max-height: 540px;
  overflow-y: auto;
  position: relative;
  scroll-behavior: smooth;
}

/* Hotspots Pulsantes */
.hs-pin {
  position: absolute;
  transform: translate(-50%, -50%);
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: 2.5px solid #FFFFFF;
  background: var(--terracotta);
  color: #FFFFFF;
  font-size: 0.74rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 12;
  box-shadow: 0 4px 16px rgba(2, 19, 47, 0.42);
  transition: transform 0.22s var(--ease-out), background 0.22s ease;
}

.hs-pin::before {
  content: "";
  position: absolute;
  inset: -6px;
  border-radius: 50%;
  border: 2px solid var(--terracotta);
  animation: hsPulse 2s ease-out infinite;
  pointer-events: none;
}

@keyframes hsPulse {
  0% { transform: scale(0.85); opacity: 0.9; }
  100% { transform: scale(1.6); opacity: 0; }
}

.hs-pin:hover {
  transform: translate(-50%, -50%) scale(1.16);
}

.hs-pin.active {
  background: var(--olive);
  color: var(--ink);
  border-color: var(--navy);
  transform: translate(-50%, -50%) scale(1.18);
  z-index: 15;
}

.hs-pin.active::before {
  border-color: var(--olive);
}

/* Panel Detalle de Hotspot */
.hs-panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-top: 4px solid var(--navy);
  border-radius: var(--radius-md);
  padding: 24px 22px;
  box-shadow: var(--shadow-card);
  position: sticky;
  top: calc(var(--topbar-h) + 20px);
}

.hs-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 16px;
}

.hs-chip {
  appearance: none;
  border: 1px solid var(--border);
  background: #FFFFFF;
  color: var(--slate);
  font-size: 0.72rem;
  font-weight: 700;
  padding: 5px 10px;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.hs-chip.active {
  background: var(--navy);
  color: #FFFFFF;
  border-color: var(--navy);
}

.hs-kicker {
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--terracotta);
  margin-bottom: 6px;
}

.hs-title {
  font-family: var(--ff-display);
  font-size: 1.38rem;
  line-height: 1.2;
  color: var(--navy);
  margin: 0 0 12px;
}

.hs-desc {
  font-size: 0.91rem;
  color: var(--text-sec);
  line-height: 1.56;
  margin: 0 0 16px;
}

.hs-meta-list {
  display: grid;
  gap: 10px;
  margin-bottom: 16px;
}

.hs-meta-item {
  background: #FFFFFF;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 11px 13px;
}

.hs-meta-item strong {
  display: block;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--editorial-blue);
  margin-bottom: 3px;
}

.hs-meta-item span {
  font-size: 0.85rem;
  color: var(--ink);
  font-weight: 600;
}

.hs-proof-pill {
  background: rgba(5, 41, 98, 0.06);
  border-left: 3px solid var(--olive-dark);
  padding: 10px 12px;
  font-size: 0.82rem;
  color: var(--navy);
  font-weight: 600;
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}

/* ==========================================================================
   JOYA ESTELAR — WIDGET TRM INTERACTIVO CO-BRANDED
   ========================================================================== */
.trm-spotlight {
  background: linear-gradient(155deg, var(--navy) 0%, var(--navy-deep) 100%);
  border-radius: var(--radius-lg);
  padding: clamp(24px, 3.5vw, 38px);
  color: #FFFFFF;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  margin-bottom: 26px;
}

.trm-spotlight::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--olive), var(--terracotta), var(--editorial-blue));
}

.trm-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 22px;
}

.trm-head h3 {
  font-family: var(--ff-display);
  font-size: clamp(1.45rem, 2.5vw, 2.05rem);
  margin: 6px 0 0;
  color: #FFFFFF;
}

.trm-badge-excl {
  background: var(--olive);
  color: var(--ink);
  font-size: 0.74rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 6px 14px;
  border-radius: 999px;
}

.trm-simulator-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
  margin-bottom: 18px;
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: var(--radius-md);
  padding: 14px 16px;
}

.trm-sim-label {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--olive-bright);
  margin-right: 4px;
}

.trm-preset {
  appearance: none;
  border: 1px solid rgba(255, 255, 255, 0.25);
  background: rgba(255, 255, 255, 0.06);
  color: #FFFFFF;
  font-size: 0.76rem;
  font-weight: 600;
  padding: 6px 12px;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.trm-preset:hover,
.trm-preset.active {
  background: var(--olive);
  border-color: var(--olive);
  color: var(--ink);
  font-weight: 800;
}

.trm-input {
  flex: 1;
  min-width: 190px;
  max-width: 280px;
  background: #FFFFFF;
  color: var(--ink);
  border: 2px solid transparent;
  border-radius: 999px;
  padding: 7px 14px;
  font-size: 0.82rem;
  font-weight: 600;
  outline: none;
}

.trm-input:focus {
  border-color: var(--olive);
}

.trm-live-mockup {
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 2px solid rgba(185, 175, 7, 0.65);
  background: #FFFFFF;
  box-shadow: 0 14px 36px rgba(0, 0, 0, 0.35);
}

.trm-cobrand-strip {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  padding: 11px 20px;
  background: linear-gradient(90deg, #02132F 0%, #052962 65%, #0A377D 100%);
  border-bottom: 2px solid var(--olive);
}

.trm-cobrand-left {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.trm-cobrand-pill {
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  background: var(--terracotta);
  color: #FFFFFF;
  padding: 3px 9px;
  border-radius: 4px;
}

.trm-cobrand-text {
  font-size: 0.9rem;
  color: #FFFFFF;
}

.trm-cobrand-text strong {
  color: var(--olive-bright);
  font-size: 1rem;
  letter-spacing: 0.02em;
}

.trm-cobrand-cta {
  font-size: 0.76rem;
  font-weight: 800;
  background: var(--olive);
  color: var(--ink);
  padding: 6px 14px;
  border-radius: 999px;
}

.trm-benefits-row {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-top: 20px;
}

.trm-ben {
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: var(--radius-sm);
  padding: 15px 16px;
}

.trm-ben strong {
  display: block;
  color: var(--olive-bright);
  font-size: 0.86rem;
  margin-bottom: 4px;
}

.trm-ben p {
  margin: 0;
  font-size: 0.82rem;
  color: var(--on-dark-2);
  line-height: 1.48;
}

/* Banda de Autoridad y Prueba Comercial */
.authority-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}

.auth-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.auth-card strong {
  font-family: var(--ff-display);
  font-size: 1.08rem;
  color: var(--navy);
}

.auth-card p {
  margin: 0;
  font-size: 0.86rem;
  color: var(--slate);
  line-height: 1.5;
}

/* ==========================================================================
   ACTO 5 — ECOSISTEMA SOCIAL MULTICANAL Y ACTIVACIÓN 90 DÍAS
   ========================================================================== */
.social-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 24px;
}

.social-card {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: var(--radius-md);
  padding: 18px 16px;
  color: #FFFFFF;
  text-decoration: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: all 0.25s var(--ease-out);
}

.social-card:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: var(--olive);
  transform: translateY(-3px);
  color: #FFFFFF;
}

.social-card--new {
  border-style: dashed;
  border-color: rgba(185, 175, 7, 0.65);
  background: rgba(185, 175, 7, 0.08);
}

.social-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.social-icon {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--olive-bright);
  flex-shrink: 0;
}

.social-status {
  font-size: 0.64rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 3px 8px;
  border-radius: 999px;
  background: rgba(52, 110, 155, 0.35);
  color: #D9EEFF;
}

.social-card--new .social-status {
  background: var(--olive);
  color: var(--ink);
}

.social-card h3 {
  font-size: 0.96rem;
  margin: 0;
  color: #FFFFFF;
}

.social-handle {
  font-size: 0.78rem;
  color: var(--olive-bright);
  font-weight: 700;
}

.social-card p {
  font-size: 0.8rem;
  color: var(--on-dark-2);
  margin: 0;
  line-height: 1.45;
}

.founder-spotlight {
  background: linear-gradient(115deg, rgba(170, 89, 89, 0.22) 0%, rgba(255, 255, 255, 0.07) 55%, rgba(185, 175, 7, 0.14) 100%);
  border: 1px solid rgba(185, 175, 7, 0.45);
  border-radius: var(--radius-md);
  padding: 22px 24px;
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 20px;
  align-items: center;
  margin-bottom: 28px;
}

.founder-spotlight h3 {
  font-family: var(--ff-display);
  font-size: 1.32rem;
  color: #FFFFFF;
  margin: 4px 0 8px;
}

.founder-spotlight p {
  margin: 0;
  font-size: 0.89rem;
  color: var(--on-dark-2);
  line-height: 1.54;
}

.founder-metrics {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.founder-stat {
  background: rgba(2, 19, 47, 0.55);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: var(--radius-sm);
  padding: 14px;
}

.founder-stat strong {
  display: block;
  font-family: var(--ff-display);
  font-size: 1.45rem;
  color: var(--olive-bright);
  line-height: 1.1;
}

.founder-stat span {
  display: block;
  font-size: 0.74rem;
  color: var(--on-dark-2);
  margin-top: 4px;
  line-height: 1.35;
}

.guarantees-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 28px;
}

.guarantee-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.13);
  border-left: 3px solid var(--olive);
  border-radius: var(--radius-sm);
  padding: 16px;
}

.guarantee-card strong {
  display: block;
  font-size: 0.9rem;
  color: #FFFFFF;
  margin-bottom: 5px;
}

.guarantee-card p {
  margin: 0;
  font-size: 0.81rem;
  color: var(--on-dark-2);
  line-height: 1.48;
}

/* Hoja de Ruta 90 Días Interactiva */
.roadmap-box {
  background: rgba(2, 19, 47, 0.55);
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: var(--radius-md);
  padding: 22px;
}

.roadmap-tabs {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin-bottom: 18px;
}

.road-btn {
  appearance: none;
  border: 1px solid rgba(255, 255, 255, 0.18);
  background: rgba(255, 255, 255, 0.05);
  color: var(--on-dark-2);
  text-align: left;
  padding: 13px 16px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.24s var(--ease-out);
}

.road-btn span {
  display: block;
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--olive-bright);
  margin-bottom: 3px;
}

.road-btn strong {
  display: block;
  font-size: 0.92rem;
  color: #FFFFFF;
}

.road-btn[aria-selected="true"] {
  background: var(--olive);
  border-color: var(--olive);
}

.road-btn[aria-selected="true"] span,
.road-btn[aria-selected="true"] strong {
  color: var(--ink);
}

.road-panel {
  display: grid;
  grid-template-columns: 1.35fr 1fr;
  gap: 20px;
  align-items: center;
  padding-top: 8px;
}

.road-panel ul {
  margin: 0;
  padding-left: 18px;
  color: var(--on-dark-2);
  font-size: 0.9rem;
  display: grid;
  gap: 8px;
}

.road-deliverable {
  background: rgba(52, 110, 155, 0.22);
  border: 1px solid rgba(185, 175, 7, 0.4);
  border-radius: var(--radius-sm);
  padding: 16px 18px;
}

.road-deliverable span {
  display: block;
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--olive-bright);
  margin-bottom: 6px;
}

.road-deliverable p {
  margin: 0;
  font-size: 0.9rem;
  color: #FFFFFF;
  line-height: 1.5;
}

/* ==========================================================================
   ACTO 6 — SIMULADOR INTERACTIVO DUAL
   ========================================================================== */
.sim-watermark {
  position: absolute;
  right: 2%;
  top: 48px;
  width: 170px;
  opacity: 0.055;
  pointer-events: none;
}

.sim-mode-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 14px;
  margin-bottom: 24px;
}

.sim-local-switch {
  display: inline-flex;
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 4px;
  gap: 4px;
}

.sim-local-btn {
  appearance: none;
  border: none;
  background: transparent;
  color: var(--slate);
  font-size: 0.84rem;
  font-weight: 700;
  padding: 9px 18px;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.22s ease;
}

.sim-local-btn[aria-selected="true"] {
  background: var(--navy);
  color: #FFFFFF;
}

.sim-grid {
  display: grid;
  grid-template-columns: 1.05fr 1fr;
  gap: 24px;
  align-items: start;
}

.sim-controls-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 26px 24px;
  box-shadow: var(--shadow-card);
}

.sim-controls-card h3 {
  font-family: var(--ff-display);
  font-size: 1.3rem;
  color: var(--navy);
  margin: 0 0 18px;
}

.pkg-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 22px;
}

.pkg-opt {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 13px 14px;
  background: #FFFFFF;
  border: 2px solid var(--border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.2s ease;
}

.pkg-opt:hover {
  border-color: var(--editorial-blue);
}

.pkg-opt.checked {
  border-color: var(--navy);
  background: #F4F8FC;
  box-shadow: 0 4px 12px rgba(5, 41, 98, 0.1);
}

.pkg-opt input {
  position: absolute;
  top: 12px;
  right: 12px;
  accent-color: var(--navy);
  width: 17px;
  height: 17px;
  cursor: pointer;
}

.pkg-opt strong {
  font-size: 0.88rem;
  color: var(--navy);
  padding-right: 22px;
}

.pkg-opt span {
  font-size: 0.76rem;
  color: var(--slate);
  line-height: 1.38;
}

.slider-group {
  margin-bottom: 20px;
}

.slider-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 8px;
  gap: 10px;
}

.slider-head label {
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--ink);
}

.slider-val {
  font-family: var(--ff-display);
  font-weight: 800;
  font-size: 1.15rem;
  color: var(--editorial-blue);
  font-variant-numeric: tabular-nums;
}

input[type="range"].lupa-range {
  width: 100%;
  accent-color: var(--navy);
  height: 7px;
  cursor: pointer;
}

.slider-ticks {
  display: flex;
  justify-content: space-between;
  font-size: 0.72rem;
  color: var(--muted);
  margin-top: 4px;
}

.scenario-pills {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin-bottom: 20px;
}

.scen-btn {
  appearance: none;
  border: 1.5px solid var(--border);
  background: #FFFFFF;
  color: var(--slate);
  font-size: 0.82rem;
  font-weight: 700;
  padding: 10px 8px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.2s ease;
}

.scen-btn[aria-pressed="true"] {
  background: var(--navy);
  border-color: var(--navy);
  color: #FFFFFF;
}

/* Panel de Resultados del Simulador */
.sim-results-card {
  background: linear-gradient(155deg, var(--navy) 0%, var(--navy-deep) 100%);
  color: #FFFFFF;
  border-radius: var(--radius-md);
  padding: 26px 24px;
  box-shadow: var(--shadow-lg);
  position: relative;
  overflow: hidden;
}

.sim-results-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--olive);
}

.sim-res-kicker {
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--olive-bright);
  margin-bottom: 6px;
}

.sim-results-card h3 {
  font-family: var(--ff-display);
  font-size: 1.38rem;
  margin: 0 0 18px;
  color: #FFFFFF;
}

.res-kpi-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 18px;
}

.res-kpi {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: var(--radius-sm);
  padding: 14px;
}

.res-kpi span {
  display: block;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--on-dark-muted);
  margin-bottom: 4px;
}

.res-kpi strong {
  font-family: var(--ff-display);
  font-size: 1.42rem;
  color: var(--olive-bright);
  line-height: 1.1;
  font-variant-numeric: tabular-nums;
}

.res-kpi small {
  display: block;
  font-size: 0.73rem;
  color: var(--on-dark-2);
  margin-top: 3px;
}

.sim-visual-box {
  background: rgba(2, 19, 47, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: var(--radius-sm);
  padding: 15px 16px;
  margin-bottom: 16px;
}

.sim-visual-box h4 {
  font-size: 0.76rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--on-dark-2);
  margin: 0 0 12px;
}

.alloc-row {
  margin-bottom: 9px;
}

.alloc-row:last-child {
  margin-bottom: 0;
}

.alloc-label {
  display: flex;
  justify-content: space-between;
  font-size: 0.78rem;
  color: #FFFFFF;
  margin-bottom: 4px;
}

.alloc-track {
  height: 8px;
  background: rgba(255, 255, 255, 0.12);
  border-radius: 999px;
  overflow: hidden;
}

.alloc-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.45s var(--ease-out);
}

.deliverables-list {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin-bottom: 16px;
}

.deliv-pill {
  font-size: 0.74rem;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.18);
  color: #FFFFFF;
  padding: 5px 10px;
  border-radius: 999px;
}

.donut-wrap {
  display: flex;
  align-items: center;
  gap: 18px;
  flex-wrap: wrap;
}

.donut-legend {
  flex: 1;
  min-width: 170px;
  display: grid;
  gap: 7px;
  font-size: 0.78rem;
}

.donut-legend-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.donut-dot {
  width: 10px;
  height: 10px;
  border-radius: 2px;
  display: inline-block;
  margin-right: 6px;
}

.sim-disclaimer {
  margin-top: 20px;
  padding: 14px 16px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-left: 3px solid var(--editorial-blue);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  font-size: 0.78rem;
  color: var(--slate);
  line-height: 1.5;
}

/* ==========================================================================
   ACTO 7 — VENTANA DE PIONEROS Y CIERRE EJECUTIVO
   ========================================================================== */
.pioneer-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
  margin-bottom: 30px;
}

.pioneer-card {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-top: 4px solid var(--olive);
  border-radius: var(--radius-md);
  padding: 24px 22px;
  transition: transform 0.25s var(--ease-out), border-color 0.25s ease;
}

.pioneer-card--hot {
  border-top-color: var(--terracotta);
  background: rgba(170, 89, 89, 0.14);
}

.pioneer-card:hover {
  transform: translateY(-4px);
  border-color: var(--olive-bright);
}

.pioneer-quota {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 999px;
  background: var(--olive);
  color: var(--ink);
  margin-bottom: 12px;
}

.pioneer-card--hot .pioneer-quota {
  background: var(--terracotta);
  color: #FFFFFF;
}

.pioneer-card h3 {
  font-family: var(--ff-display);
  font-size: 1.24rem;
  color: #FFFFFF;
  margin: 0 0 10px;
}

.pioneer-card p {
  margin: 0;
  font-size: 0.88rem;
  color: var(--on-dark-2);
  line-height: 1.54;
}

.closing-card {
  background: #FFFFFF;
  color: var(--ink);
  border-radius: var(--radius-lg);
  padding: clamp(24px, 3.5vw, 38px);
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 28px;
  align-items: center;
  box-shadow: var(--shadow-lg);
}

.closing-brand-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.closing-brand-row img {
  height: 46px;
  width: auto;
}

.ceo-badge {
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--terracotta);
}

.closing-ceo-name {
  font-family: var(--ff-display);
  font-size: clamp(1.5rem, 2.4vw, 2rem);
  color: var(--navy);
  margin: 2px 0 6px;
}

.closing-ceo-role {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--slate);
  margin: 0 0 14px;
}

.closing-quote {
  font-family: var(--ff-serif);
  font-style: italic;
  font-size: 1.02rem;
  color: var(--text-sec);
  border-left: 3px solid var(--olive);
  padding-left: 14px;
  margin: 0 0 16px;
}

.contact-meta {
  display: grid;
  gap: 6px;
  font-size: 0.85rem;
  color: var(--slate);
}

.contact-meta strong {
  color: var(--navy);
}

.closing-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 22px;
}

.closing-actions h4 {
  font-family: var(--ff-display);
  font-size: 1.15rem;
  color: var(--navy);
  margin: 0 0 4px;
}

.closing-actions p {
  font-size: 0.84rem;
  color: var(--slate);
  margin: 0 0 8px;
}

.pitch-footer {
  margin-top: 34px;
  padding-top: 18px;
  border-top: 1px solid rgba(255, 255, 255, 0.15);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  font-size: 0.78rem;
  color: var(--on-dark-muted);
}

/* ==========================================================================
   MODAL DE CONTACTO DIRECTO / WHATSAPP
   ========================================================================== */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(2, 19, 47, 0.76);
  backdrop-filter: blur(6px);
  z-index: 200;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-backdrop.open {
  display: flex;
}

.modal-dialog {
  background: #FFFFFF;
  color: var(--ink);
  width: min(540px, 100%);
  border-radius: var(--radius-md);
  padding: 26px;
  box-shadow: 0 28px 64px rgba(0, 0, 0, 0.45);
  border-top: 4px solid var(--olive);
}

.modal-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.modal-head h3 {
  font-family: var(--ff-display);
  font-size: 1.32rem;
  color: var(--navy);
  margin: 0;
}

.modal-close {
  appearance: none;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--ink);
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-size: 1.1rem;
  cursor: pointer;
}

.modal-summary {
  width: 100%;
  min-height: 150px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 12px;
  font-family: var(--ff-sans);
  font-size: 0.85rem;
  line-height: 1.5;
  color: var(--ink);
  background: var(--surface);
  resize: vertical;
  margin-bottom: 14px;
}

.modal-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: flex-end;
}

/* ==========================================================================
   MODO PRESENTACIÓN FULLSCREEN (DECK MODE)
   ========================================================================== */
body.deck {
  overflow: hidden;
}

body.deck .rail,
body.deck .scroll-cue {
  display: none;
}

body.deck #deck {
  position: fixed;
  inset: 0;
  overflow: hidden;
}

body.deck #track {
  display: flex;
  height: 100dvh;
  will-change: transform;
  transform: translate3d(calc(var(--i, 0) * -100vw), 0, 0);
  transition: transform 0.72s var(--ease-expo);
}

body.deck .slide {
  flex: 0 0 100vw;
  height: 100dvh;
  overflow-y: auto;
  overflow-x: hidden;
  padding: calc(var(--topbar-h) + 26px) 0 76px;
  border-bottom: none;
}

body.deck #act-1 {
  min-height: 0;
  align-items: flex-start;
}

body.deck #act-7 {
  padding-top: calc(var(--topbar-h) + 16px);
  padding-bottom: 62px;
}
body.deck #act-7 .eyebrow {
  margin-bottom: 8px;
}
body.deck #act-7 .act-title {
  font-size: clamp(1.65rem, 2.7vw, 2.35rem);
  margin-bottom: 10px;
}
body.deck #act-7 .section-rule {
  margin-bottom: 12px;
}
body.deck #act-7 .act-lead {
  font-size: 1rem;
  margin-bottom: 16px;
}
body.deck #act-7 .pioneer-grid {
  gap: 14px;
  margin-bottom: 18px;
}
body.deck #act-7 .pioneer-card {
  padding: 16px 18px;
}
body.deck #act-7 .pioneer-quota {
  margin-bottom: 8px;
}
body.deck #act-7 .pioneer-card h3 {
  font-size: 1.08rem;
  margin-bottom: 6px;
}
body.deck #act-7 .pioneer-card p {
  font-size: 0.82rem;
  line-height: 1.44;
}
body.deck #act-7 .closing-card {
  padding: 20px 26px;
  gap: 20px;
}
body.deck #act-7 .closing-brand-row {
  margin-bottom: 8px;
}
body.deck #act-7 .closing-brand-row img {
  height: 36px;
}
body.deck #act-7 .closing-ceo-name {
  font-size: 1.48rem;
}
body.deck #act-7 .closing-ceo-role {
  margin-bottom: 8px;
}
body.deck #act-7 .closing-quote {
  font-size: 0.92rem;
  margin-bottom: 10px;
}
body.deck #act-7 .closing-actions {
  padding: 16px 18px;
  gap: 9px;
}
body.deck #act-7 .closing-actions .cta-btn {
  padding: 10px 16px;
  font-size: 0.86rem;
}
body.deck #act-7 .pitch-footer {
  margin-top: 14px;
  padding-top: 12px;
}

body.deck .rv {
  opacity: 1 !important;
  transform: none !important;
}

.deckbar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 110;
  display: none;
  align-items: center;
  gap: 14px;
  padding: 10px clamp(16px, 3vw, 34px);
  background: rgba(4, 31, 74, 0.95);
  backdrop-filter: blur(12px);
  border-top: 1px solid rgba(255, 255, 255, 0.14);
}

body.deck .deckbar {
  display: flex;
}

.deck-nav-btn {
  width: 34px;
  height: 34px;
  border-radius: var(--radius-sm);
  border: 1px solid rgba(255, 255, 255, 0.25);
  background: rgba(255, 255, 255, 0.08);
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.deck-nav-btn:hover {
  background: var(--olive);
  border-color: var(--olive);
  color: var(--ink);
}

.deck-title {
  flex: 1;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--on-dark-2);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.deck-count {
  font-size: 0.82rem;
  font-weight: 800;
  color: var(--olive-bright);
  font-variant-numeric: tabular-nums;
}

/* Toast */
#toast {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%) translateY(90px);
  opacity: 0;
  z-index: 250;
  background: var(--olive);
  color: var(--ink);
  font-size: 0.84rem;
  font-weight: 800;
  padding: 11px 22px;
  border-radius: 999px;
  box-shadow: 0 12px 30px rgba(2, 19, 47, 0.4);
  transition: all 0.3s var(--ease-out);
  pointer-events: none;
  white-space: nowrap;
}

#toast.show {
  transform: translateX(-50%) translateY(0);
  opacity: 1;
}

/* ==========================================================================
   RESPONSIVE (TABLET & SMARTPHONE 390px)
   ========================================================================== */
@media (max-width: 1120px) {
  .pillars-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
  .showcase-stage {
    grid-template-columns: 1fr;
  }
  .hs-panel {
    position: static;
  }
  .social-grid,
  .guarantees-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 900px) {
  .brand-divider,
  .brand-caption {
    display: none;
  }
  .rail {
    display: none;
  }
  .hero-kpis,
  .stat-grid-4 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .market-split,
  .sim-grid,
  .founder-spotlight,
  .road-panel,
  .closing-card {
    grid-template-columns: 1fr;
  }
  .trm-benefits-row,
  .authority-strip,
  .pioneer-grid {
    grid-template-columns: 1fr;
  }
  .pillars-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 600px) {
  .topbar {
    padding: 8px 12px;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: space-between;
  }
  .brand-lockup img {
    height: 28px;
  }
  .profile-switch {
    order: 3;
    width: 100%;
    justify-content: stretch;
  }
  .profile-btn {
    flex: 1;
    justify-content: center;
    padding: 7px 10px;
    font-size: 0.74rem;
  }
  .tool-btn .btn-txt-hide {
    display: none;
  }
  .tool-btn {
    padding: 6px 10px;
    font-size: 0.72rem;
  }
  #act-1 {
    padding-top: 122px;
  }
  .slide {
    padding: 84px 0 54px;
  }
  .hero-kpis,
  .stat-grid-4,
  .pillars-grid,
  .social-grid,
  .guarantees-grid,
  .pkg-grid,
  .res-kpi-grid,
  .roadmap-tabs,
  .founder-metrics {
    grid-template-columns: 1fr;
  }
  .compare-controls {
    padding: 14px;
  }
  .toggle-track {
    width: 100%;
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
  .toggle-opt {
    padding: 9px 10px;
    font-size: 0.76rem;
    text-align: center;
  }
  .browser-hint {
    display: none;
  }
  .hs-pin {
    width: 28px;
    height: 28px;
    font-size: 0.68rem;
  }
  .trm-cobrand-strip {
    padding: 10px 12px;
  }
  .scroll-cue {
    display: none;
  }
  .deck-title {
    font-size: 0.68rem;
  }
}

/* ==========================================================================
   PREFERS REDUCED MOTION
   ========================================================================== */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.001ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.001ms !important;
    scroll-behavior: auto !important;
  }
  .rv {
    opacity: 1 !important;
    transform: none !important;
  }
}

/* ==========================================================================
   EXPORTACIÓN LIMPIA A PDF (@media print)
   ========================================================================== */
@media print {
  .topbar, .rail, .deckbar, .scroll-cue, #toast, .modal-backdrop, .tool-btn, .fullpage-toolbar {
    display: none !important;
  }
  body {
    background: #FFFFFF !important;
    color: var(--ink) !important;
  }
  .slide {
    padding: 24px 0 !important;
    page-break-inside: avoid;
    break-inside: avoid;
  }
  .rv {
    opacity: 1 !important;
    transform: none !important;
  }
  .fullpage-scroll {
    max-height: none !important;
    overflow: visible !important;
  }
  .print-banner {
    display: flex !important;
  }
}

.print-banner {
  display: none;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  border-bottom: 2px solid var(--navy);
  background: #FFFFFF;
}

.print-banner img {
  height: 36px;
}

/* Utilidades de perfil dinámico */
.only-inversor {
  display: none;
}
body[data-profile="inversor"] .only-marca {
  display: none;
}
body[data-profile="inversor"] .only-inversor {
  display: block;
}
body[data-profile="inversor"] .sim-grid.only-inversor {
  display: grid;
}
body[data-profile="inversor"] .only-inversor-inline {
  display: inline-flex;
}
.only-inversor-inline {
  display: none;
}
body[data-profile="inversor"] .only-marca-inline {
  display: none;
}
</style>
</head>
<body data-profile="marca">

<div class="prog" id="prog"></div>

<!-- Encabezado exclusivo para impresión PDF -->
<div class="print-banner">
  <img src="__LOGO_NAVY__" alt="Somos La Lupa News">
  <span style="font-weight:700;color:#052962;font-size:0.85rem;">Pitch Comercial y de Inversión · somoslalupanews.com · 2026</span>
</div>

<!-- ========================================================================
     BARRA SUPERIOR FIJA (TOPBAR)
     ======================================================================== -->
<header class="topbar" role="banner">
  <a href="#act-1" class="brand-lockup" aria-label="Somos La Lupa News — Ir al inicio">
    <img src="__LOGO_WHITE__" alt="Somos La Lupa News">
    <span class="brand-divider" aria-hidden="true"></span>
    <span class="brand-caption">
      <strong>Somos La Lupa News</strong>
      <span>Pitch Comercial &amp; Inversión 2026</span>
    </span>
  </a>

  <div class="profile-switch" role="group" aria-label="Seleccionar perfil de visitante">
    <button type="button" class="profile-btn" id="sw-marca" data-set-profile="marca" aria-pressed="true">
      Soy Marca / Anunciante
    </button>
    <button type="button" class="profile-btn" id="sw-inversor" data-set-profile="inversor" aria-pressed="false">
      Soy Inversionista
    </button>
  </div>

  <div class="topbar-tools">
    <button type="button" class="tool-btn" id="btn-deck" aria-pressed="false" title="Modo Presentación en vivo (Tecla F)">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H8V4h12v12z"/></svg>
      <span class="btn-txt-hide">Presentación</span> [F]
    </button>
    <button type="button" class="tool-btn tool-btn--pdf" id="btn-print" title="Imprimir o guardar en PDF">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19 8H5c-1.66 0-3 1.34-3 3v6h4v4h12v-4h4v-6c0-1.66-1.34-3-3-3zm-3 11H8v-5h8v5zm3-7c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm-1-9H6v4h12V3z"/></svg>
      PDF
    </button>
  </div>
</header>

<!-- ========================================================================
     RAIL LATERAL DE NAVEGACIÓN (7 ACTOS)
     ======================================================================== -->
<nav class="rail" id="rail" aria-label="Navegación por actos">
  <button type="button" data-idx="0" data-label="01 · Apertura &amp; Oportunidad" aria-current="true"></button>
  <button type="button" data-idx="1" data-label="02 · Pulso del Mercado CO"></button>
  <button type="button" data-idx="2" data-label="03 · Redes vs. Portal Propio"></button>
  <button type="button" data-idx="3" data-label="04 · Vitrina Viva &amp; Joya TRM"></button>
  <button type="button" data-idx="4" data-label="05 · Red Social &amp; Plan 90 Días"></button>
  <button type="button" data-idx="5" data-label="06 · Simulador Interactivo"></button>
  <button type="button" data-idx="6" data-label="07 · Pioneros &amp; Cierre Ejecutivo"></button>
</nav>

<div id="deck">
<main id="track">

<!-- ========================================================================
     ACTO 1 — APERTURA DE ALTO IMPACTO
     ======================================================================== -->
<section class="slide slide--navy" id="act-1" data-t="01 · APERTURA DE ALTO IMPACTO · SOMOS LA LUPA NEWS">
  <div class="hero-grid-bg" aria-hidden="true"></div>
  <div class="hero-glow" aria-hidden="true"></div>
  <img src="__IMAGO_WHITE__" alt="" class="hero-watermark" aria-hidden="true">

  <div class="shell">
    <div class="hero-top-row rv">
      <div class="hero-logo-badge">
        <img src="__LOGO_WHITE__" alt="Logotipo Oficial Somos La Lupa News">
      </div>
      <div class="live-pill">
        <span class="live-dot" aria-hidden="true"></span>
        Portal Operativo · TRM Viva Hoy ($3,327 COP)
      </div>
    </div>

    <div class="eyebrow rv rv-d1">SOMOS LA LUPA NEWS · MEDIO DIGITAL COLOMBIANO EN REACTIVACIÓN ESTRATÉGICA</div>

    <h1 class="hero-h1 rv rv-d1">
      El 59% de la pauta en Colombia ya es digital, pero <span class="hl">3 de cada 4 lectores</span> desconfían de las redes. Tu marca merece un medio propio, creíble y medible.
    </h1>

    <p class="hero-subtitle rv rv-d2 only-marca">
      <strong>Somos La Lupa News (somoslalupanews.com)</strong> reactiva su ecosistema informativo con formatos editoriales de alto recuerdo, el <strong>patrocinio exclusivo del indicador diario TRM</strong> y reportes transparentes de resultados reales para cada campaña.
    </p>
    <p class="hero-subtitle rv rv-d2 only-inversor">
      Un <strong>activo mediático colombiano ya construido</strong> —con <strong>4.583 historias publicadas</strong>, marcas reales validadas y liderazgo periodístico nacional— listo para inyectar capital 100% en tracción de audiencia, comunidad propia y monetización directa de alto margen.
    </p>

    <div class="hero-route-bar rv rv-d3">
      <button type="button" class="cta-btn cta-btn--olive cta-btn--active-route" id="hero-btn-marca" data-set-profile="marca" data-scroll-next="#act-2">
        Explorar como Marca / Anunciante
        <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8z"/></svg>
      </button>
      <button type="button" class="cta-btn cta-btn--ghost-light" id="hero-btn-inversor" data-set-profile="inversor" data-scroll-next="#act-2">
        Explorar como Inversionista
        <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8z"/></svg>
      </button>
      <a href="#act-4" class="cta-btn cta-btn--ghost-light" style="border-color:rgba(185,175,7,0.55);color:#F4EE7B;">
        Ver Portal y Joya TRM
      </a>
    </div>

    <div class="hero-kpis rv rv-d4">
      <div class="kpi-box">
        <div class="kpi-val"><span class="count-up" data-target="4583" data-format="int">4.583</span></div>
        <div class="kpi-lbl">Historias publicadas</div>
        <div class="kpi-sub">Archivo periodístico real en somoslalupanews.com, listo para reactivación</div>
      </div>
      <div class="kpi-box kpi-box--terracotta">
        <div class="kpi-val"><span class="accent-num">$3,327</span> COP</div>
        <div class="kpi-lbl">Indicador TRM vivo hoy</div>
        <div class="kpi-sub">Actualización diaria en portada (19 nov 2026) · Patrocinio exclusivo</div>
      </div>
      <div class="kpi-box">
        <div class="kpi-val">$<span class="count-up" data-target="3.04" data-format="dec2">3,04</span>B COP</div>
        <div class="kpi-lbl">Mercado digital Colombia</div>
        <div class="kpi-sub">59% de la inversión total en medios y +9,1% interanual en Q2 2026</div>
      </div>
      <div class="kpi-box">
        <div class="kpi-val"><span class="count-up" data-target="20" data-format="int">20</span> Verticales</div>
        <div class="kpi-lbl">Cobertura nacional</div>
        <div class="kpi-sub">Colombia, Deportes, Mundo, Poder, Economía, Negocios e Historias</div>
      </div>
    </div>
  </div>

  <div class="scroll-cue" aria-hidden="true">
    <span>Desplázate o presiona F para presentar</span>
    <i></i>
  </div>
</section>

<!-- ========================================================================
     ACTO 2 — PULSO DEL MERCADO DIGITAL COLOMBIA (2025–2026)
     ======================================================================== -->
<section class="slide slide--paper" id="act-2" data-t="02 · PULSO DEL MERCADO COLOMBIA 2025–2026">
  <div class="shell">
    <div class="eyebrow rv">ACTO 02 · INTELIGENCIA DE MERCADO COLOMBIA 2025–2026</div>
    <h2 class="act-title rv rv-d1">Una audiencia móvil masiva buscando información en la que pueda confiar</h2>
    <div class="section-rule rv rv-d1"></div>
    <p class="act-lead rv rv-d2">
      Los presupuestos publicitarios en Colombia ya son mayoritariamente digitales y los formatos editoriales viven su mayor aceleración histórica. Al mismo tiempo, la fatiga frente a las redes sociales abre una ventana extraordinaria para medios independientes curados.
    </p>

    <div class="stat-grid-4 rv rv-d2">
      <article class="editorial-card editorial-card--primary">
        <div class="stat-big">80,9%</div>
        <h3>Penetración de Internet</h3>
        <p><strong>43,7 millones</strong> de colombianos conectados, 87,6 millones de líneas celulares y más de <strong>10,7 millones</strong> de accesos 5G en expansión.</p>
      </article>
      <article class="editorial-card editorial-card--blue">
        <div class="stat-big">75%</div>
        <h3>Lectura desde Smartphone</h3>
        <p>3 de cada 4 lectores colombianos consumen noticias en su celular, con un promedio de <strong>19,9 GB/mes</strong> de datos móviles por línea.</p>
      </article>
      <article class="editorial-card editorial-card--olive">
        <div class="stat-big">$847.662M</div>
        <h3>Pauta Digital Q2 2026 (COP)</h3>
        <p>Salto de <strong>+91,5% frente a Q1</strong> y <strong>+9,1% interanual</strong> sobre un mercado que superó los $3,04 billones COP en 2025.</p>
      </article>
      <article class="editorial-card editorial-card--alert">
        <div class="stat-big">25%</div>
        <h3>Confianza en Noticias en Redes</h3>
        <p>Cayó del 32% al <strong>25% en 2026</strong>, mientras el <strong>59%</strong> expresa alta preocupación por la desinformación en feeds sociales.</p>
      </article>
    </div>

    <div class="market-split rv rv-d3">
      <div class="chart-panel" id="market-chart">
        <div class="chart-panel-head">
          <h3>Crecimiento de Formatos Digitales en Colombia (Q2 2026)</h3>
          <span class="chart-tag">Auge Editorial</span>
        </div>

        <div class="bar-row">
          <div class="bar-meta">
            <strong>Branded Content &amp; Notas Patrocinadas</strong>
            <span class="bar-pct bar-pct--hot">+90,5% YoY</span>
          </div>
          <div class="bar-track"><div class="bar-fill bar-fill--hot" data-w="96%"></div></div>
          <div class="bar-sub">El formato de mayor crecimiento en Colombia: historias de marca con hasta 86% de recordación espontánea.</div>
        </div>

        <div class="bar-row">
          <div class="bar-meta">
            <strong>Display Editorial en Portales</strong>
            <span class="bar-pct">+34,4% YoY</span>
          </div>
          <div class="bar-track"><div class="bar-fill bar-fill--blue" data-w="64%"></div></div>
          <div class="bar-sub">$125.834 millones COP en Q2 2026 (14,8% del total) impulsado por entornos seguros y visibles.</div>
        </div>

        <div class="bar-row">
          <div class="bar-meta">
            <strong>Video Digital &amp; Cápsulas Cortas</strong>
            <span class="bar-pct">+19,2% YoY</span>
          </div>
          <div class="bar-track"><div class="bar-fill bar-fill--mid" data-w="48%"></div></div>
          <div class="bar-sub">Líder de participación con 32,1% ($272.396 millones COP), en perfecta sinergia con YouTube y Reels.</div>
        </div>

        <div class="bar-row">
          <div class="bar-meta">
            <strong>Inversión Digital Total Colombia (Q2 2026)</strong>
            <span class="bar-pct">+9,1% YoY</span>
          </div>
          <div class="bar-track"><div class="bar-fill bar-fill--olive" data-w="34%"></div></div>
          <div class="bar-sub">Ritmo sostenido por encima de la economía general: el 59% de la pauta nacional ya vive en digital.</div>
        </div>
      </div>

      <aside class="paradox-card">
        <div>
          <span class="paradox-badge">LA PARADOJA DE LA CONFIANZA 2026</span>
          <h3>Más presupuesto digital que nunca, pero menos lugares seguros para tu reputación</h3>
          <p>
            Mientras el 72% descubre temas en redes sociales, 3 de cada 4 lectores ya desconfían de lo que circula sin curaduría. Las marcas serias están migrando presupuesto hacia <strong>portales periodísticos propios</strong> donde su mensaje se asocia con credibilidad y orden.
          </p>
        </div>
        <div class="paradox-lens only-marca">
          <strong>Qué significa para tu marca</strong>
          Aparecer en <em>somoslalupanews.com</em> protege tu reputación, eleva en <strong>+9% la afinidad de marca</strong> y multiplica la atención frente a anuncios perdidos en feeds saturados.
        </div>
        <div class="paradox-lens only-inversor">
          <strong>Qué significa para tu inversión</strong>
          La demanda comercial se desplaza justo hacia los dos productos de mayor margen de un portal propio: <strong>Branded Content (+90,5%)</strong> y <strong>patrocinios directos (+34,4% en Display)</strong>.
        </div>
      </aside>
    </div>

    <div class="source-footnote rv rv-d4">
      Fuentes verificadas: IAB Colombia (Reporte Anual 2025 y Q1–Q2 2026) · Reuters Institute for the Study of Journalism, Universidad de Oxford (Digital News Report Colombia 2025–2026) · DataReportal &amp; MinTIC Colombia (2026).
    </div>
  </div>
</section>

<!-- ========================================================================
     ACTO 3 — COMPARADOR INTERACTIVO: SOLO REDES VS. PORTAL PROPIO ACTIVADO
     ======================================================================== -->
<section class="slide slide--surface" id="act-3" data-t="03 · COMPARADOR INTERACTIVO · REDES VS. PORTAL PROPIO">
  <div class="shell">
    <div class="eyebrow rv">ACTO 03 · CONTRASTE ESTRATÉGICO EN VIVO</div>
    <h2 class="act-title rv rv-d1">Las redes sociales despiertan curiosidad; un portal propio construye autoridad, patrimonio y ventas</h2>
    <div class="section-rule rv rv-d1"></div>
    <p class="act-lead rv rv-d2">
      Compara en un clic cómo cambia el desempeño de una marca —y el valor del negocio— cuando pasa de depender únicamente de algoritmos sociales a activar un medio propio conectado con buscadores, comunidad directa y reporte transparente.
    </p>

    <div class="compare-controls rv rv-d2">
      <div class="toggle-track" role="group" aria-label="Comparar escenarios">
        <button type="button" class="toggle-opt is-before" id="cmp-before" aria-pressed="false">
          Solo Redes Sociales
        </button>
        <button type="button" class="toggle-opt is-after" id="cmp-after" aria-pressed="true">
          Portal Propio Activado
        </button>
      </div>

      <div class="compare-meter">
        <span class="compare-meter-label" id="cmp-meter-lbl">Solidez &amp; Control Comercial</span>
        <div class="compare-meter-bar">
          <div class="compare-meter-fill" id="cmp-meter-fill" style="width:94%;background:var(--navy);"></div>
        </div>
        <span class="compare-meter-score" id="cmp-meter-score">94 / 100</span>
      </div>
    </div>

    <div class="pillars-grid rv rv-d3" id="pillars-grid">
      <article class="pillar-card state-after" data-pillar="0">
        <div>
          <div class="pillar-num">Pilar 01</div>
          <h3>Propiedad de la Audiencia</h3>
          <p class="pillar-body">Audiencia propia en <strong>somoslalupanews.com</strong> respaldada por Google, Google Discover (67,5% del tráfico móvil de noticias) y comunidad directa en WhatsApp y boletín.</p>
        </div>
        <div class="pillar-metric">Activo propio blindado</div>
      </article>

      <article class="pillar-card state-after" data-pillar="1">
        <div>
          <div class="pillar-num">Pilar 02</div>
          <h3>Seguridad de Marca</h3>
          <p class="pillar-body">Entorno editorial limpio, ordenado y curado por periodistas. Tu anuncio transfiere confianza institucional y eleva la afinidad con audiencias exigentes.</p>
        </div>
        <div class="pillar-metric">+9% afinidad de marca</div>
      </article>

      <article class="pillar-card state-after" data-pillar="2">
        <div>
          <div class="pillar-num">Pilar 03</div>
          <h3>Atención y Recordación</h3>
          <p class="pillar-body">Formatos nativos, patrocinios de sección y notas de valor leídas con atención real, sin pelear contra el deslizamiento compulsivo de un feed.</p>
        </div>
        <div class="pillar-metric">+53% atención · hasta 86% recuerdo</div>
      </article>

      <article class="pillar-card state-after" data-pillar="3">
        <div>
          <div class="pillar-num">Pilar 04</div>
          <h3>Hábito Diario (TRM)</h3>
          <p class="pillar-body">Utilidad financiera consultada todos los días por empresarios, viajeros e importadores: un motivo recurrente para regresar al portal cada mañana.</p>
        </div>
        <div class="pillar-metric">100% exclusividad diaria</div>
      </article>

      <article class="pillar-card state-after" data-pillar="4">
        <div>
          <div class="pillar-num">Pilar 05</div>
          <h3>Medición Transparente</h3>
          <p class="pillar-body">Trazabilidad exacta de cada clic por espacio, reimpacto inteligente a lectores interesados y reporte ejecutivo mensual listo para gerencia.</p>
        </div>
        <div class="pillar-metric">Cero "pauta a ciegas"</div>
      </article>
    </div>

    <div class="compare-bottom-note rv rv-d4">
      <p class="only-marca">
        <strong>Conclusión clave para anunciantes:</strong> No abandonamos las redes sociales; las convertimos en autopistas de amplificación que traen lectores calificados hacia tu marca viviendo en <em>somoslalupanews.com</em>.
      </p>
      <p class="only-inversor">
        <strong>Conclusión clave para inversionistas:</strong> Un portal propio con venta directa, audiencia recurrente y base propia de lectores construye patrimonio transferible valorado en múltiplos de <strong>6x a 12x+ EBITDA</strong>, muy por encima de cuentas dependientes de terceros.
      </p>
      <a href="#act-4" class="cta-btn cta-btn--olive" style="padding:10px 18px;font-size:0.84rem;">
        Explorar el portal real →
      </a>
    </div>
  </div>
</section>

<!-- ========================================================================
     ACTO 4 — VITRINA VIVA DE SOMOSLALUPANEWS.COM + JOYA ESTELAR TRM
     ======================================================================== -->
<section class="slide slide--paper" id="act-4" data-t="04 · VITRINA VIVA DE SOMOSLALUPANEWS.COM &amp; JOYA TRM">
  <div class="shell">
    <div class="eyebrow rv">ACTO 04 · PRODUCTO REAL VERIFICADO EN PRODUCCIÓN</div>
    <h2 class="act-title rv rv-d1">Una plataforma viva, probada con grandes marcas y lista para escalar</h2>
    <div class="section-rule rv rv-d1"></div>
    <p class="act-lead rv rv-d2">
      Estas son capturas reales de <strong>somoslalupanews.com</strong>. Cambia entre las 4 vistas y haz clic sobre los puntos pulsantes para descubrir cómo luce tu marca en cada posición estratégica del medio.
    </p>

    <!-- Selector de 4 Vistas Reales -->
    <div class="showcase-tabs rv rv-d2" role="tablist" aria-label="Vistas reales de somoslalupanews.com">
      <button type="button" class="view-tab" role="tab" aria-selected="true" data-view="desktop">
        1. Portada Escritorio <span class="tab-badge">4 zonas</span>
      </button>
      <button type="button" class="view-tab" role="tab" aria-selected="false" data-view="article">
        2. Patrocinio &amp; Artículo Real <span class="tab-badge">Café Águila Roja</span>
      </button>
      <button type="button" class="view-tab" role="tab" aria-selected="false" data-view="mobile">
        3. Experiencia Móvil <span class="tab-badge">75% CO</span>
      </button>
      <button type="button" class="view-tab" role="tab" aria-selected="false" data-view="full">
        4. Ecosistema Completo <span class="tab-badge">Scroll vivo</span>
      </button>
    </div>

    <div class="showcase-stage rv rv-d3">
      <!-- Visor Izquierdo -->
      <div class="browser-frame">
        <div class="browser-chrome">
          <div class="browser-dots" aria-hidden="true"><i></i><i></i><i></i></div>
          <div class="browser-url" id="browser-url">https://somoslalupanews.com/</div>
          <div class="browser-hint">Haz clic en los puntos pulsantes</div>
        </div>

        <!-- Vista 1: Portada Escritorio -->
        <div class="capture-canvas view-pane" id="pane-desktop">
          <img src="__CAP_DESKTOP__" alt="Captura real de portada escritorio de somoslalupanews.com con widget TRM y banner Súper Astro">
          <button type="button" class="hs-pin active" style="left:48%;top:16%;" data-hs="h1" aria-label="Hotspot 1: Cabecera Premium">1</button>
          <button type="button" class="hs-pin" style="left:29%;top:32%;" data-hs="h2" aria-label="Hotspot 2: Patrocinio Exclusivo TRM">2</button>
          <button type="button" class="hs-pin" style="left:55%;top:44%;" data-hs="h3" aria-label="Hotspot 3: Leaderboard Premium Superior">3</button>
          <button type="button" class="hs-pin" style="left:75%;top:64%;" data-hs="h3b" aria-label="Hotspot 4: Destacadas y Nativo In-Feed">4</button>
        </div>

        <!-- Vista 2: Artículo & Patrocinio Café Águila Roja -->
        <div class="capture-canvas view-pane" id="pane-article" hidden>
          <img src="__CAP_ARTICLE__" alt="Captura real de artículo de Deportes en somoslalupanews.com patrocinado por Café Águila Roja">
          <button type="button" class="hs-pin active" style="left:46%;top:26%;" data-hs="h4" aria-label="Hotspot 4: Patrocinio de Sección Café Águila Roja">4</button>
          <button type="button" class="hs-pin" style="left:34%;top:43%;" data-hs="h5" aria-label="Hotspot 5: Branded Content y Nota Patrocinada">5</button>
          <button type="button" class="hs-pin" style="left:78%;top:54%;" data-hs="h6" aria-label="Hotspot 6: Mid-Article y Columna Tendencias">6</button>
        </div>

        <!-- Vista 3: Experiencia Móvil -->
        <div class="view-pane" id="pane-mobile" hidden>
          <div class="mobile-stage-bg">
            <div class="phone-bezel">
              <div class="phone-notch" aria-hidden="true"></div>
              <div class="phone-screen">
                <img src="__CAP_MOBILE__" alt="Captura real móvil 390px de somoslalupanews.com con TRM en 3 columnas">
                <button type="button" class="hs-pin active" style="left:50%;top:22.5%;" data-hs="h7a" aria-label="Hotspot Móvil: TRM 3 columnas">7A</button>
                <button type="button" class="hs-pin" style="left:50%;top:32.5%;" data-hs="h7b" aria-label="Hotspot Móvil: Banner Superior">7B</button>
                <button type="button" class="hs-pin" style="left:50%;top:55%;" data-hs="h7c" aria-label="Hotspot Móvil: Lectura Limpia">7C</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Vista 4: Ecosistema Completo Scrollable -->
        <div class="view-pane" id="pane-full" hidden>
          <div class="fullpage-toolbar">
            <button type="button" class="jump-btn" data-jump="0">↑ Portada y TRM</button>
            <button type="button" class="jump-btn" data-jump="0.40" data-select-hs="h8">Ver Half-Page 300×600 (H8)</button>
            <button type="button" class="jump-btn" data-jump="0.62" data-select-hs="h9">Ver Encuesta Tu Mirada &amp; Video (H9)</button>
            <button type="button" class="jump-btn" data-jump="0.88">Ver Cierre y Pre-Footer</button>
          </div>
          <div class="fullpage-scroll" id="fullpage-scroll">
            <div class="capture-canvas">
              <img src="__CAP_FULL__" alt="Captura real completa de la portada de somoslalupanews.com mostrando inventario display, deportes, encuesta y YouTube">
              <button type="button" class="hs-pin active" style="left:76%;top:45.5%;" data-hs="h8" aria-label="Hotspot 8: Half-Page Lateral 300x600">8</button>
              <button type="button" class="hs-pin" style="left:75%;top:65%;" data-hs="h9" aria-label="Hotspot 9: Encuesta Tu Mirada y Vitrina YouTube">9</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Panel Derecho: Ficha del Hotspot Activo -->
      <aside class="hs-panel" aria-live="polite">
        <div class="hs-pills" id="hs-pills"></div>
        <div class="hs-kicker" id="hs-kicker">ZONA H1 · PRESENCIA INSTITUCIONAL</div>
        <h3 class="hs-title" id="hs-title">Cabecera Editorial &amp; Navegación de Verticales</h3>
        <p class="hs-desc" id="hs-desc">
          Arquitectura de prensa digital sobria y confiable que organiza 20 verticales de interés nacional (Colombia, Política, Deportes, Mundo, Historias, Música y Opinión) más acceso directo a transmisiones En Vivo.
        </p>
        <div class="hs-meta-list">
          <div class="hs-meta-item">
            <strong>Beneficio comercial</strong>
            <span id="hs-benefit">Transferencia inmediata de autoridad editorial desde el primer segundo en pantalla.</span>
          </div>
          <div class="hs-meta-item">
            <strong>Anunciante ideal</strong>
            <span id="hs-ideal">Marcas corporativas, consumo masivo, finanzas, entretenimiento y lanzamientos nacionales.</span>
          </div>
          <div class="hs-meta-item">
            <strong>Impacto y visibilidad</strong>
            <span id="hs-impact">100% visibilidad inicial (primer pantallazo en escritorio y móvil).</span>
          </div>
        </div>
        <div class="hs-proof-pill" id="hs-proof">
          Evidencia real: 4.583 publicaciones en archivo y navegación multi-sección operativa hoy.
        </div>
      </aside>
    </div>

    <!-- ====================================================================
         BLOQUE ESTELAR: LA JOYA COMERCIAL — PATROCINIO EXCLUSIVO WIDGET TRM
         ==================================================================== -->
    <div class="trm-spotlight rv rv-d3">
      <div class="trm-head">
        <div>
          <span class="eyebrow" style="margin-bottom:4px;">LA JOYA COMERCIAL DEL PORTAL · 1 ÚNICO CUPO</span>
          <h3>Patrocinio Exclusivo del Indicador Diario TRM</h3>
        </div>
        <span class="trm-badge-excl">100% Exclusividad de Categoría</span>
      </div>

      <!-- Simulador Visual Instantáneo de Co-Branding TRM -->
      <div class="trm-simulator-bar">
        <span class="trm-sim-label">Simula tu marca patrocinando la TRM hoy:</span>
        <button type="button" class="trm-preset active" data-brand="Tu Banco / Fintech" data-cta="Cotiza dólar hoy →">Banco / Fintech</button>
        <button type="button" class="trm-preset" data-brand="Aerolínea / Viajes" data-cta="Reserva tu vuelo →">Aerolínea / Viajes</button>
        <button type="button" class="trm-preset" data-brand="Importadora / Comercio" data-cta="Calcula tu envío →">Comercio Exterior</button>
        <input type="text" class="trm-input" id="trm-brand-input" maxlength="38" placeholder="O escribe el nombre de tu marca..." aria-label="Escribe el nombre de tu marca para simular el patrocinio de la TRM">
      </div>

      <div class="trm-live-mockup">
        <div class="trm-cobrand-strip">
          <div class="trm-cobrand-left">
            <span class="trm-cobrand-pill">PATROCINIO EXCLUSIVO</span>
            <span class="trm-cobrand-text">TRM del día presentada por <strong id="trm-brand-output">Tu Banco / Fintech</strong></span>
          </div>
          <span class="trm-cobrand-cta" id="trm-cta-output">Cotiza dólar hoy →</span>
        </div>
        <img src="__CAP_TRM__" alt="Captura real del Widget TRM de somoslalupanews.com mostrando TRM HOY $3,327 COP el 19 de noviembre de 2026">
      </div>

      <div class="trm-benefits-row">
        <div class="trm-ben">
          <strong>Hábito de Consulta Diaria</strong>
          <p>En Colombia, consultar el dólar es una rutina matutina de empresarios, importadores, viajeros y decisores financieros — generando visitas repetidas sin depender de viralidad.</p>
        </div>
        <div class="trm-ben">
          <strong>Cero Ceguera de Banner</strong>
          <p>Ubicado en el primer pantallazo tanto en escritorio como en celular, el lector mira activamente la cifra del dólar y asocia esa utilidad cotidiana con tu marca.</p>
        </div>
        <div class="trm-ben">
          <strong>Verticales de Alto Valor</strong>
          <p>Espacio irreplicable para <strong>Bancos, Fintechs, Remesadoras, Casas de Cambio, Aerolíneas, Aseguradoras y Bienes Raíces</strong> con trazabilidad exacta de cada clic.</p>
        </div>
      </div>
    </div>

    <!-- Banda de Prueba Comercial y Liderazgo -->
    <div class="authority-strip rv rv-d4">
      <div class="auth-card">
        <strong>Prueba Comercial Real</strong>
        <p>Espacios ya validados con marcas nacionales de primer nivel como <strong>Café Águila Roja</strong> (patrocinio de sección en Deportes) y <strong>Súper Astro</strong> (6 ubicaciones display de alto impacto).</p>
      </div>
      <div class="auth-card">
        <strong>Liderazgo Mediático Nacional</strong>
        <p>Dirigido por <strong>Javier Fernández Franco («El Cantante del Gol»)</strong>, aportando credibilidad inmediata, cercanía popular y sinergia irreplicable en Deportes y actualidad.</p>
      </div>
      <div class="auth-card">
        <strong>Capacidad Editorial Probada</strong>
        <p>Más de <strong>4.583 artículos reales</strong> en archivo con picos históricos superiores a <strong>1.100 noticias por trimestre</strong> — una redacción lista para encender motores de inmediato.</p>
      </div>
    </div>
  </div>
</section>

<!-- ========================================================================
     ACTO 5 — ECOSISTEMA SOCIAL MULTICANAL Y ACTIVACIÓN INTELIGENTE
     ======================================================================== -->
<section class="slide slide--navy" id="act-5" data-t="05 · ECOSISTEMA SOCIAL &amp; ACTIVACIÓN INTELIGENTE 90 DÍAS">
  <img src="__IMAGO_WHITE__" alt="" class="hero-watermark" style="left:-40px;right:auto;bottom:10px;opacity:0.045;" aria-hidden="true">

  <div class="shell">
    <div class="eyebrow rv">ACTO 05 · RED MULTICANAL Y MARKETING DE RETORNO MEDIBLE</div>
    <h2 class="act-title rv rv-d1">El portal es el hogar; nuestra campaña inteligente es el motor que trae lectores todos los días</h2>
    <div class="section-rule rv rv-d1"></div>
    <p class="act-lead rv rv-d2">
      Cada historia, patrocinio y entrevista publicada en <strong>somoslalupanews.com</strong> se amplifica a través de nuestra red social verificada, el impulso del fundador y nuevos canales de comunidad propia — con medición clara de principio a fin.
    </p>

    <!-- Grilla de Canales Reales Confirmados + 2 Palancas Propias -->
    <div class="social-grid rv rv-d2">
      <a class="social-card" href="https://www.instagram.com/lalupanewsco/" target="_blank" rel="noopener noreferrer">
        <div class="social-top">
          <div class="social-icon" aria-hidden="true">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M7.8 2h8.4C19.4 2 22 4.6 22 7.8v8.4a5.8 5.8 0 0 1-5.8 5.8H7.8C4.6 22 2 19.4 2 16.2V7.8A5.8 5.8 0 0 1 7.8 2m-.2 2A3.6 3.6 0 0 0 4 7.6v8.8C4 18.39 5.61 20 7.6 20h8.8a3.6 3.6 0 0 0 3.6-3.6V7.6C20 5.61 18.39 4 16.4 4H7.6m9.65 1.5a1.25 1.25 0 0 1 1.25 1.25A1.25 1.25 0 0 1 17.25 8 1.25 1.25 0 0 1 16 6.75a1.25 1.25 0 0 1 1.25-1.25M12 7a5 5 0 0 1 5 5 5 5 0 0 1-5 5 5 5 0 0 1-5-5 5 5 0 0 1 5-5m0 2a3 3 0 0 0-3 3 3 3 0 0 0 3 3 3 3 0 0 0 3-3 3 3 0 0 0-3-3z"/></svg>
          </div>
          <span class="social-status">Canal Oficial</span>
        </div>
        <h3>Instagram</h3>
        <div class="social-handle">@lalupanewsco</div>
        <p>Vitrina visual de noticias rápidas, carruseles editoriales y Reels patrocinados hacia el portal.</p>
      </a>

      <a class="social-card" href="https://x.com/lalupanewsco" target="_blank" rel="noopener noreferrer">
        <div class="social-top">
          <div class="social-icon" aria-hidden="true">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
          </div>
          <span class="social-status">Canal Oficial</span>
        </div>
        <h3>X (Twitter)</h3>
        <div class="social-handle">@lalupanewsco</div>
        <p>Minuto a minuto de opinión pública, política, economía, alertas TRM y conversación en tiempo real.</p>
      </a>

      <a class="social-card" href="https://www.youtube.com/@LaLupaNews" target="_blank" rel="noopener noreferrer">
        <div class="social-top">
          <div class="social-icon" aria-hidden="true">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 0 0 .5 6.2 31.4 31.4 0 0 0 0 12a31.4 31.4 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 0 0 2.1-2.1A31.4 31.4 0 0 0 24 12a31.4 31.4 0 0 0-.5-5.8zM9.6 15.6V8.4l6.3 3.6-6.3 3.6z"/></svg>
          </div>
          <span class="social-status">Hub Video</span>
        </div>
        <h3>YouTube</h3>
        <div class="social-handle">@LaLupaNews</div>
        <p>Centro audiovisual de entrevistas, crónicas, programas en vivo y cápsulas Shorts integradas a portada.</p>
      </a>

      <a class="social-card" href="https://www.tiktok.com/@lalupanews" target="_blank" rel="noopener noreferrer">
        <div class="social-top">
          <div class="social-icon" aria-hidden="true">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z"/></svg>
          </div>
          <span class="social-status">Video Vertical</span>
        </div>
        <h3>TikTok</h3>
        <div class="social-handle">@lalupanews</div>
        <p>Descubrimiento vertical masivo para nuevas generaciones (el canal de mayor crecimiento informativo en Colombia).</p>
      </a>

      <a class="social-card" href="https://www.facebook.com/profile.php?id=61572383767685" target="_blank" rel="noopener noreferrer">
        <div class="social-top">
          <div class="social-icon" aria-hidden="true">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M22 12c0-5.52-4.48-10-10-10S2 6.48 2 12c0 4.84 3.44 8.87 8 9.8V15H8v-3h2V9.5C10 7.57 11.57 6 13.5 6H16v3h-2c-.55 0-1 .45-1 1v2h3v3h-3v6.95c5.05-.5 9-4.76 9-9.95z"/></svg>
          </div>
          <span class="social-status">Alcance Regional</span>
        </div>
        <h3>Facebook</h3>
        <div class="social-handle">La Lupa News Oficial</div>
        <p>Comunidad masiva en ciudades y regiones de Colombia (red #1 en consulta de noticias en el país).</p>
      </a>

      <a class="social-card" href="https://www.linkedin.com/in/la-lupa-news-504432338/" target="_blank" rel="noopener noreferrer">
        <div class="social-top">
          <div class="social-icon" aria-hidden="true">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>
          </div>
          <span class="social-status">Conexión B2B</span>
        </div>
        <h3>LinkedIn</h3>
        <div class="social-handle">La Lupa News</div>
        <p>Relacionamiento ejecutivo con gerentes de mercadeo, gremios, empresas y aliados corporativos.</p>
      </a>

      <div class="social-card social-card--new">
        <div class="social-top">
          <div class="social-icon" aria-hidden="true">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91C21.95 6.45 17.5 2 12.04 2zm5.82 14.08c-.24.68-1.42 1.31-1.97 1.39-.51.08-1.16.11-1.87-.12-.44-.14-1-.33-1.72-.64-3.03-1.31-5.01-4.38-5.16-4.58-.15-.2-1.23-1.64-1.23-3.12s.78-2.21 1.06-2.51c.28-.3.61-.38.81-.38h.58c.19 0 .44-.07.69.52.25.6.86 2.1.94 2.25.08.15.13.33.02.53-.1.2-.15.33-.3.51-.15.18-.32.4-.45.54-.15.15-.31.32-.13.62.18.3.79 1.3 1.69 2.11 1.17 1.04 2.15 1.36 2.45 1.51.3.15.48.13.66-.08.18-.2.76-.89.96-1.19.2-.3.4-.25.68-.15.28.1 1.77.83 2.07.98.3.15.5.23.58.35.08.13.08.73-.16 1.41z"/></svg>
          </div>
          <span class="social-status">Activación Fase 2</span>
        </div>
        <h3>Canal WhatsApp</h3>
        <div class="social-handle">Comunidad Propia</div>
        <p>Alertas diarias de última hora y TRM directo al celular (35% de Colombia se informa vía WhatsApp).</p>
      </div>

      <div class="social-card social-card--new">
        <div class="social-top">
          <div class="social-icon" aria-hidden="true">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4-8 5-8-5V6l8 5 8-5v2z"/></svg>
          </div>
          <span class="social-status">Activación Fase 2</span>
        </div>
        <h3>Boletín Ejecutivo</h3>
        <div class="social-handle">Audiencia Directa</div>
        <p>Resumen matutino de actualidad y dólar patrocinable con altísima apertura, independiente de algoritmos.</p>
      </div>
    </div>

    <!-- Amplificador Legítimo del Fundador (claramente separado del portal) -->
    <div class="founder-spotlight rv rv-d2">
      <div>
        <span class="eyebrow" style="margin-bottom:4px;">TRAMPOLÍN DE CREDIBILIDAD Y AMPLIFICACIÓN · MARCA PERSONAL DEL CEO</span>
        <h3>Javier Fernández Franco («El Cantante del Gol»)</h3>
        <p>
          A diferencia de portales anónimos que tardan años en ganar confianza, Somos La Lupa News cuenta con la dirección y respaldo directo de una de las voces más reconocidas de Colombia — generando sinergia natural en Deportes, Selección Colombia y formatos de video en vivo.
        </p>
      </div>
      <div class="founder-metrics">
        <a href="https://www.youtube.com/@elcantantedelgol.oficial" target="_blank" rel="noopener noreferrer" class="founder-stat" style="text-decoration:none;">
          <strong>&gt;9.200</strong>
          <span>Suscriptores y 301 videos en canal personal de YouTube (<em>@elcantantedelgol.oficial</em>) ↗</span>
        </a>
        <div class="founder-stat">
          <strong>&gt;180.000</strong>
          <span>Seguidores en Instagram personal reportados en prensa nacional <em>(métrica propia del fundador)</em></span>
        </div>
      </div>
    </div>

    <!-- 4 Garantías de Marketing Inteligente ("Cero Caja Negra") -->
    <div class="guarantees-grid rv rv-d3">
      <div class="guarantee-card">
        <strong>1. Alcance Activo y Segmentado</strong>
        <p>Distribución inteligente (orgánica y pautada) hacia lectores reales en Colombia afines a cada vertical.</p>
      </div>
      <div class="guarantee-card">
        <strong>2. Trazabilidad Exacta por Espacio</strong>
        <p>Cero "caja negra": sabes con precisión qué formato (TRM, portada o nota patrocinada) generó más interés.</p>
      </div>
      <div class="guarantee-card">
        <strong>3. Reimpacto Inteligente</strong>
        <p>Recordamos tu marca a quienes ya leyeron secciones de Economía o Deportes sin desperdiciar presupuesto.</p>
      </div>
      <div class="guarantee-card">
        <strong>4. Fórmula 1-a-6 + Reporte Mensual</strong>
        <p>Cada historia se multiplica en 6 formatos y se cierra cada mes con un tablero ejecutivo de resultados.</p>
      </div>
    </div>

    <!-- Hoja de Ruta Interactiva 90 Días -->
    <div class="roadmap-box rv rv-d4">
      <div class="roadmap-tabs" role="tablist" aria-label="Hoja de ruta de activación 90 días">
        <button type="button" class="road-btn" role="tab" aria-selected="true" data-phase="0">
          <span>Fase 1 · Días 1–30</span>
          <strong>Puesta a Punto y Despegue</strong>
        </button>
        <button type="button" class="road-btn" role="tab" aria-selected="false" data-phase="1">
          <span>Fase 2 · Días 31–60</span>
          <strong>Tracción y Comunidad Propia</strong>
        </button>
        <button type="button" class="road-btn" role="tab" aria-selected="false" data-phase="2">
          <span>Fase 3 · Días 61–90</span>
          <strong>Escala y Monetización 360°</strong>
        </button>
      </div>

      <div class="road-panel" id="road-panel" aria-live="polite">
        <ul id="road-list">
          <li>Reactivación del ritmo editorial diario con foco en Colombia, Deportes, Economía y actualidad.</li>
          <li>Sincronización completa de las 6 redes sociales hacia <strong>somoslalupanews.com</strong> y refuerzo de identidad ejecutiva.</li>
          <li>Puesta en marcha del tablero comercial de medición transparente y lanzamiento junto a Javier Fernández Franco.</li>
        </ul>
        <div class="road-deliverable">
          <span>Entregable visible de la fase</span>
          <p id="road-deliv">Portal renovado, ecosistema social unificado y primer reporte base de audiencia verificada para anunciantes pioneros.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ========================================================================
     ACTO 6 — SIMULADOR INTERACTIVO DUAL (ANUNCIANTE ↔ INVERSIONISTA)
     ======================================================================== -->
<section class="slide slide--paper" id="act-6" data-t="06 · SIMULADOR INTERACTIVO DUAL · ANUNCIANTE &amp; INVERSIONISTA">
  <img src="__IMAGO_NAVY__" alt="" class="sim-watermark" aria-hidden="true">

  <div class="shell">
    <div class="eyebrow rv">ACTO 06 · CONSOLA INTERACTIVA DE PROYECCIÓN</div>
    <div class="sim-mode-bar rv rv-d1">
      <div>
        <h2 class="act-title" style="margin-bottom:6px;">Diseña tu escenario a la medida en tiempo real</h2>
        <div class="section-rule" style="margin-bottom:0;"></div>
      </div>
      <div class="sim-local-switch" role="tablist" aria-label="Cambiar modo del simulador">
        <button type="button" class="sim-local-btn" id="sim-tab-marca" role="tab" aria-selected="true" data-set-profile="marca">
          Simulador de Pauta (Marca)
        </button>
        <button type="button" class="sim-local-btn" id="sim-tab-inversor" role="tab" aria-selected="false" data-set-profile="inversor">
          Simulador de Escala (Inversionista)
        </button>
      </div>
    </div>

    <!-- ================================================================
         MODO A: SIMULADOR PARA MARCAS Y ANUNCIANTES
         ================================================================ -->
    <div class="sim-grid only-marca rv rv-d2" id="sim-marca-wrap">
      <div class="sim-controls-card">
        <h3>1. Configura tu campaña en Somos La Lupa News</h3>

        <div class="pkg-grid" id="pkg-grid">
          <label class="pkg-opt checked">
            <input type="checkbox" value="trm" checked>
            <strong>Patrocinio Exclusivo TRM</strong>
            <span>100% exclusividad diaria sobre el indicador de dólar en portada.</span>
          </label>
          <label class="pkg-opt checked">
            <input type="checkbox" value="branded" checked>
            <strong>Branded Content + Sección</strong>
            <span>Nota patrocinada y sello de sección (estilo Café Águila Roja).</span>
          </label>
          <label class="pkg-opt">
            <input type="checkbox" value="display">
            <strong>Campaña 360° Display + Redes</strong>
            <span>Banners de alto impacto en portada/móvil + amplificación social.</span>
          </label>
          <label class="pkg-opt">
            <input type="checkbox" value="video">
            <strong>Cápsulas Video + WhatsApp</strong>
            <span>Mención en video vertical y presencia en comunidad propia.</span>
          </label>
        </div>

        <div class="slider-group">
          <div class="slider-head">
            <label for="sl-budget">Inversión mensual estimada (COP)</label>
            <span class="slider-val" id="val-budget">$12.000.000 COP</span>
          </div>
          <input type="range" id="sl-budget" class="lupa-range" min="4" max="35" step="1" value="12">
          <div class="slider-ticks"><span>$4M COP</span><span>$15M COP</span><span>$35M COP</span></div>
        </div>

        <div class="slider-group" style="margin-bottom:0;">
          <div class="slider-head">
            <label for="sl-months">Duración de la campaña</label>
            <span class="slider-val" id="val-months">3 meses</span>
          </div>
          <input type="range" id="sl-months" class="lupa-range" min="1" max="6" step="1" value="3">
          <div class="slider-ticks"><span>1 mes (Piloto)</span><span>3 meses (Tracción)</span><span>6 meses (Posicionamiento)</span></div>
        </div>
      </div>

      <div class="sim-results-card" aria-live="polite">
        <div class="sim-res-kicker">PROYECCIÓN ILUSTRATIVA DE CAMPAÑA</div>
        <h3 id="res-marca-title">Plan Combinado de Alto Impacto · 3 Meses</h3>

        <div class="res-kpi-grid">
          <div class="res-kpi">
            <span>Exposición total estimada</span>
            <strong id="res-impr">480.000 – 720.000</strong>
            <small>Impresiones visibles en portal y amplificación</small>
          </div>
          <div class="res-kpi">
            <span>Clics cualificados proyectados</span>
            <strong id="res-clicks">3.840 – 6.910</strong>
            <small id="res-ctr">CTR nativo ref. 0,65%–1,05% (3x–10x vs. banner)</small>
          </div>
          <div class="res-kpi">
            <span>Impulso estimado en recordación</span>
            <strong id="res-lift">+24% a +86%</strong>
            <small>Recuerdo espontáneo con formato editorial</small>
          </div>
          <div class="res-kpi">
            <span>Inversión total estimada</span>
            <strong id="res-total">$36.000.000</strong>
            <small id="res-bonif">Tarifa preferencial de relanzamiento incluida</small>
          </div>
        </div>

        <div class="sim-visual-box">
          <h4>Distribución de Impacto por Canal</h4>
          <div class="alloc-row">
            <div class="alloc-label"><span>Portada, TRM &amp; Lectura Editorial</span><strong id="m-bar1-v">52%</strong></div>
            <div class="alloc-track"><div class="alloc-fill" id="m-bar1" style="width:52%;background:var(--olive);"></div></div>
          </div>
          <div class="alloc-row">
            <div class="alloc-label"><span>Amplificación en Redes &amp; Video</span><strong id="m-bar2-v">30%</strong></div>
            <div class="alloc-track"><div class="alloc-fill" id="m-bar2" style="width:30%;background:#5AA0D6;"></div></div>
          </div>
          <div class="alloc-row">
            <div class="alloc-label"><span>Reimpacto Inteligente a Lectores</span><strong id="m-bar3-v">18%</strong></div>
            <div class="alloc-track"><div class="alloc-fill" id="m-bar3" style="width:18%;background:#D47A7A;"></div></div>
          </div>
        </div>

        <div class="deliverables-list" id="res-deliverables">
          <span class="deliv-pill">✓ Reporte ejecutivo mensual</span>
          <span class="deliv-pill">✓ Trazabilidad exacta de clics</span>
          <span class="deliv-pill">✓ Exclusividad de categoría</span>
          <span class="deliv-pill">✓ Reimpacto inteligente</span>
        </div>

        <button type="button" class="cta-btn cta-btn--olive" style="width:100%;" id="btn-copy-sim-marca">
          Copiar resumen de mi simulación para agendar
        </button>
      </div>
    </div>

    <!-- ================================================================
         MODO B: SIMULADOR PARA INVERSIONISTAS
         ================================================================ -->
    <div class="sim-grid only-inversor rv rv-d2" id="sim-inversor-wrap">
      <div class="sim-controls-card">
        <h3>1. Modela la aceleración y despliegue de capital</h3>

        <div class="scenario-pills" role="group" aria-label="Escenario de ejecución">
          <button type="button" class="scen-btn" data-scen="conservador" aria-pressed="false">Conservador</button>
          <button type="button" class="scen-btn" data-scen="base" aria-pressed="true">Base Recomendado</button>
          <button type="button" class="scen-btn" data-scen="acelerado" aria-pressed="false">Acelerado</button>
        </div>

        <div class="slider-group">
          <div class="slider-head">
            <label for="sl-cap">Inyección de capital de crecimiento (COP)</label>
            <span class="slider-val" id="val-cap">$120.000.000 COP</span>
          </div>
          <input type="range" id="sl-cap" class="lupa-range" min="50" max="300" step="10" value="120">
          <div class="slider-ticks"><span>$50M COP</span><span>$150M COP</span><span>$300M COP</span></div>
        </div>

        <div class="slider-group">
          <div class="slider-head">
            <label for="sl-horizon">Horizonte de escalamiento</label>
            <span class="slider-val" id="val-horizon">12 meses</span>
          </div>
          <input type="range" id="sl-horizon" class="lupa-range" min="3" max="12" step="3" value="12">
          <div class="slider-ticks"><span>3 meses</span><span>6 meses</span><span>9 meses</span><span>12 meses</span></div>
        </div>

        <div class="sim-visual-box" style="background:#FFFFFF;border-color:var(--border);color:var(--ink);margin-bottom:0;">
          <h4 style="color:var(--navy);">Asignación Disciplinada del Capital (100% Tracción)</h4>
          <div class="alloc-row">
            <div class="alloc-label" style="color:var(--ink);"><span>35% Motor Editorial &amp; Descubrimiento</span><strong id="cap-35" style="color:var(--navy);">$42,0M</strong></div>
            <div class="alloc-track" style="background:var(--surface-2);"><div class="alloc-fill" style="width:35%;background:var(--navy);"></div></div>
          </div>
          <div class="alloc-row">
            <div class="alloc-label" style="color:var(--ink);"><span>30% Distribución Inteligente &amp; Crecimiento</span><strong id="cap-30" style="color:var(--editorial-blue);">$36,0M</strong></div>
            <div class="alloc-track" style="background:var(--surface-2);"><div class="alloc-fill" style="width:30%;background:var(--editorial-blue);"></div></div>
          </div>
          <div class="alloc-row">
            <div class="alloc-label" style="color:var(--ink);"><span>20% Fuerza Comercial B2B &amp; Anclas</span><strong id="cap-20" style="color:var(--terracotta);">$24,0M</strong></div>
            <div class="alloc-track" style="background:var(--surface-2);"><div class="alloc-fill" style="width:20%;background:var(--terracotta);"></div></div>
          </div>
          <div class="alloc-row">
            <div class="alloc-label" style="color:var(--ink);"><span>15% Analítica &amp; Comunidad Propia</span><strong id="cap-15" style="color:var(--olive-dark);">$18,0M</strong></div>
            <div class="alloc-track" style="background:var(--surface-2);"><div class="alloc-fill" style="width:15%;background:var(--olive);"></div></div>
          </div>
        </div>
      </div>

      <div class="sim-results-card" aria-live="polite">
        <div class="sim-res-kicker">TESIS DE CRECIMIENTO &amp; MIX DE INGRESOS</div>
        <h3 id="res-inv-title">Escenario Base Recomendado · 12 Meses</h3>

        <div class="res-kpi-grid">
          <div class="res-kpi">
            <span>Ritmo mensual proyectado al cierre</span>
            <strong id="res-inv-rev">$38M – $52M</strong>
            <small>COP/mes en venta directa y patrocinios</small>
          </div>
          <div class="res-kpi">
            <span>Clientes ancla objetivo</span>
            <strong id="res-inv-clients">6 a 9 marcas</strong>
            <small>1 exclusivo TRM + secciones + Branded Content</small>
          </div>
          <div class="res-kpi">
            <span>Infraestructura ya construida</span>
            <strong>100% Activa</strong>
            <small>4.583 notas + TRM vivo · cero gasto desde cero</small>
          </div>
          <div class="res-kpi">
            <span>Referencia patrimonial del sector</span>
            <strong>6x – 12x+ EBITDA</strong>
            <small>Múltiplo en medios propios con venta directa</small>
          </div>
        </div>

        <div class="sim-visual-box">
          <h4>Mezcla Diversificada de Ingresos Proyectada</h4>
          <div class="donut-wrap">
            <svg width="118" height="118" viewBox="0 0 42 42" aria-label="Gráfico circular de mezcla de ingresos">
              <circle cx="21" cy="21" r="15.9155" fill="transparent" stroke="rgba(255,255,255,0.12)" stroke-width="5.2"></circle>
              <circle id="seg-trm" cx="21" cy="21" r="15.9155" fill="transparent" stroke="#B9AF07" stroke-width="5.2" stroke-dasharray="30 70" stroke-dashoffset="25"></circle>
              <circle id="seg-bc" cx="21" cy="21" r="15.9155" fill="transparent" stroke="#AA5959" stroke-width="5.2" stroke-dasharray="32 68" stroke-dashoffset="-5"></circle>
              <circle id="seg-sec" cx="21" cy="21" r="15.9155" fill="transparent" stroke="#5AA0D6" stroke-width="5.2" stroke-dasharray="23 77" stroke-dashoffset="-37"></circle>
              <circle id="seg-disp" cx="21" cy="21" r="15.9155" fill="transparent" stroke="#FFFFFF" stroke-width="5.2" stroke-dasharray="15 85" stroke-dashoffset="-60"></circle>
              <text x="21" y="20" text-anchor="middle" fill="#FFFFFF" font-size="5" font-weight="800">MIX</text>
              <text x="21" y="25.5" text-anchor="middle" fill="#D4C914" font-size="3.6" font-weight="700">100%</text>
            </svg>
            <div class="donut-legend">
              <div class="donut-legend-item"><span><i class="donut-dot" style="background:#B9AF07;"></i>Patrocinio TRM Ancla</span><strong id="leg-trm">30%</strong></div>
              <div class="donut-legend-item"><span><i class="donut-dot" style="background:#AA5959;"></i>Branded Content Alto Margen</span><strong id="leg-bc">32%</strong></div>
              <div class="donut-legend-item"><span><i class="donut-dot" style="background:#5AA0D6;"></i>Patrocinio de Secciones</span><strong id="leg-sec">23%</strong></div>
              <div class="donut-legend-item"><span><i class="donut-dot" style="background:#FFFFFF;"></i>Display Directo &amp; Video</span><strong id="leg-disp">15%</strong></div>
            </div>
          </div>
        </div>

        <button type="button" class="cta-btn cta-btn--olive" style="width:100%;" id="btn-copy-sim-inversor">
          Copiar resumen de tesis para sesión ejecutiva
        </button>
      </div>
    </div>

    <div class="sim-disclaimer rv rv-d3">
      <strong>Nota de transparencia ejecutiva:</strong> Escenarios ilustrativos basados en benchmarks oficiales del mercado digital de Colombia y LATAM 2025–2026 (IAB Colombia, Native Advertising Institute y reportes sectoriales de medios). Los resultados reales dependen del plan editorial, la estacionalidad y el presupuesto de activación acordado.
    </div>
  </div>
</section>

<!-- ========================================================================
     ACTO 7 — VENTANA DE PIONEROS Y CIERRE EJECUTIVO
     ======================================================================== -->
<section class="slide slide--navy" id="act-7" data-t="07 · VENTANA DE PIONEROS &amp; CIERRE EJECUTIVO">
  <img src="__IMAGO_WHITE__" alt="" class="hero-watermark" aria-hidden="true">

  <div class="shell">
    <div class="eyebrow rv">ACTO 07 · OPORTUNIDAD DE ENTRADA TEMPRANA</div>
    <h2 class="act-title rv rv-d1">El mejor momento para entrar a un medio en despegue es antes de que todos quieran estar ahí</h2>
    <div class="section-rule rv rv-d1"></div>
    <p class="act-lead rv rv-d2">
      La etapa de relanzamiento de <strong>Somos La Lupa News</strong> abre una ventana única con inventario genuinamente limitado, tarifas preferenciales de primer ocupante y conversación directa con la Dirección General.
    </p>

    <div class="pioneer-grid rv rv-d2">
      <article class="pioneer-card pioneer-card--hot">
        <span class="pioneer-quota">1 Único Cupo Disponible</span>
        <h3>Patrocinador Exclusivo Widget TRM</h3>
        <p>100% <em>Share of Voice</em> sobre la utilidad financiera más consultada del portal (escritorio y móvil), blindado frente a competidores de tu industria durante toda la vigencia.</p>
      </article>

      <article class="pioneer-card">
        <span class="pioneer-quota">Máximo 5 Marcas Fundadoras</span>
        <h3>Exclusividad por Vertical Editorial</h3>
        <p>Un solo patrocinador ancla por categoría (Deportes, Economía, Actualidad, Estilo de Vida y Tecnología) con condiciones preferenciales de lanzamiento y reporte mensual.</p>
      </article>

      <article class="pioneer-card">
        <span class="pioneer-quota">Mesa Ejecutiva Acotada</span>
        <h3>Aliados Estratégicos de Capital</h3>
        <p>Participación temprana sobre una plataforma editorial ya construida (4.583 historias + prueba de marcas), destinando el capital 100% a crecimiento y monetización.</p>
      </article>
    </div>

    <div class="closing-card rv rv-d3">
      <div>
        <div class="closing-brand-row">
          <img src="__LOGO_NAVY__" alt="Somos La Lupa News">
          <span class="ceo-badge">Dirección General · Contacto Directo</span>
        </div>
        <h3 class="closing-ceo-name">Javier Fernández Franco</h3>
        <div class="closing-ceo-role">CEO — Somos La Lupa News</div>
        <blockquote class="closing-quote">
          «Construimos un medio con rigor, cercanía y voz propia en Colombia. Hoy abrimos las puertas a las marcas y aliados visionarios que quieren crecer con nosotros desde el primer día de esta nueva etapa.»
        </blockquote>
        <div class="contact-meta">
          <div><strong>Portal Oficial:</strong> <a href="https://somoslalupanews.com" target="_blank" rel="noopener noreferrer">https://somoslalupanews.com</a></div>
          <div><strong>Sede:</strong> Calle 127 #16A-76, oficina 402, Bogotá, Colombia</div>
          <div><strong>Correo Comercial:</strong> <a href="mailto:lalupanewsco@gmail.com">lalupanewsco@gmail.com</a></div>
        </div>
      </div>

      <div class="closing-actions">
        <h4 class="only-marca">Reserva tu espacio de lanzamiento</h4>
        <h4 class="only-inversor">Agenda sesión ejecutiva de inversión</h4>
        <p class="only-marca">Recibe una propuesta personalizada con disponibilidad de fechas para el Patrocinio TRM o cupo de Marca Fundadora.</p>
        <p class="only-inversor">Solicita reunión directa con Javier Fernández Franco para revisar proyecciones detalladas y estructura de participación.</p>

        <a href="mailto:lalupanewsco@gmail.com?subject=Inter%C3%A9s%20Comercial%20%E2%80%94%20Somos%20La%20Lupa%20News" class="cta-btn cta-btn--navy" id="cta-mailto">
          <span class="only-marca-inline">Reservar Reunión Comercial por Correo</span>
          <span class="only-inversor-inline">Solicitar Sesión de Inversión por Correo</span>
        </a>

        <button type="button" class="cta-btn cta-btn--olive" id="btn-open-modal">
          Preparar Mensaje Directo / WhatsApp
        </button>

        <button type="button" class="cta-btn" style="background:#FFFFFF;border-color:var(--border);color:var(--navy);" id="btn-copy-closing">
          Copiar Resumen de Mi Simulación
        </button>
      </div>
    </div>

    <footer class="pitch-footer rv rv-d4">
      <span>© 2026 Somos La Lupa News · Bogotá, Colombia · Portal Oficial: somoslalupanews.com</span>
      <span>Presentación Comercial y de Inversión · Versión Ejecutiva 2026</span>
    </footer>
  </div>
</section>

</main>
</div>

<!-- Barra Inferior de Modo Presentación -->
<div class="deckbar" id="deckbar" role="region" aria-label="Controles de presentación">
  <button type="button" class="deck-nav-btn" id="dprev" aria-label="Diapositiva anterior" title="Anterior (←)">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M15.41 7.41 14 6l-6 6 6 6 1.41-1.41L10.83 12z"/></svg>
  </button>
  <button type="button" class="deck-nav-btn" id="dnext" aria-label="Diapositiva siguiente" title="Siguiente (→)">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M10 6 8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>
  </button>
  <div class="deck-title" id="dtitle">01 · APERTURA DE ALTO IMPACTO · SOMOS LA LUPA NEWS</div>
  <div class="deck-count" id="dcount">01 / 07</div>
</div>

<!-- Modal de Mensaje Directo / Agenda -->
<div class="modal-backdrop" id="contact-modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <div class="modal-dialog">
    <div class="modal-head">
      <h3 id="modal-title">Mensaje listo para enviar a Somos La Lupa News</h3>
      <button type="button" class="modal-close" id="modal-close" aria-label="Cerrar ventana">×</button>
    </div>
    <p style="font-size:0.86rem;color:var(--slate);margin:0 0 12px;">
      Personaliza o copia este resumen con tu escenario seleccionado para enviarlo por correo o WhatsApp al equipo de <strong>Javier Fernández Franco</strong>:
    </p>
    <textarea class="modal-summary" id="modal-textarea" aria-label="Resumen listo para enviar"></textarea>
    <div class="modal-actions">
      <button type="button" class="cta-btn" style="background:var(--surface);border-color:var(--border);color:var(--ink);padding:10px 16px;" id="modal-copy">
        Copiar Texto
      </button>
      <a href="mailto:lalupanewsco@gmail.com" class="cta-btn cta-btn--navy" style="padding:10px 16px;" id="modal-email-link">
        Abrir en Correo
      </a>
    </div>
  </div>
</div>

<div id="toast" role="status" aria-live="polite">Resumen copiado al portapapeles</div>

<script>
(function () {
  'use strict';

  var body = document.body;
  var track = document.getElementById('track');
  var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  var railDots = Array.prototype.slice.call(document.querySelectorAll('#rail button'));
  var prog = document.getElementById('prog');
  var deckBtn = document.getElementById('btn-deck');
  var printBtn = document.getElementById('btn-print');
  var dprev = document.getElementById('dprev');
  var dnext = document.getElementById('dnext');
  var dtitle = document.getElementById('dtitle');
  var dcount = document.getElementById('dcount');
  var toastEl = document.getElementById('toast');
  var RM = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var currentSlide = 0;
  var toastTimer = null;

  function showToast(msg) {
    toastEl.textContent = msg;
    toastEl.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      toastEl.classList.remove('show');
    }, 2600);
  }

  function formatCOP(millions) {
    var val = Math.round(millions * 1000000);
    return '$' + val.toLocaleString('es-CO');
  }

  function formatInt(n) {
    return Math.round(n).toLocaleString('es-CO');
  }

  /* ======================================================================
     1. SELECTOR DUAL DE PERFIL (MARCA / ANUNCIANTE <-> INVERSIONISTA)
     ====================================================================== */
  var swMarca = document.getElementById('sw-marca');
  var swInversor = document.getElementById('sw-inversor');
  var heroBtnMarca = document.getElementById('hero-btn-marca');
  var heroBtnInversor = document.getElementById('hero-btn-inversor');
  var simTabMarca = document.getElementById('sim-tab-marca');
  var simTabInversor = document.getElementById('sim-tab-inversor');

  function setProfile(profile, silent) {
    var isInv = profile === 'inversor';
    body.setAttribute('data-profile', isInv ? 'inversor' : 'marca');

    swMarca.setAttribute('aria-pressed', isInv ? 'false' : 'true');
    swInversor.setAttribute('aria-pressed', isInv ? 'true' : 'false');

    if (simTabMarca && simTabInversor) {
      simTabMarca.setAttribute('aria-selected', isInv ? 'false' : 'true');
      simTabInversor.setAttribute('aria-selected', isInv ? 'true' : 'false');
    }

    if (heroBtnMarca && heroBtnInversor) {
      heroBtnMarca.className = isInv ? 'cta-btn cta-btn--ghost-light' : 'cta-btn cta-btn--olive cta-btn--active-route';
      heroBtnInversor.className = isInv ? 'cta-btn cta-btn--olive cta-btn--active-route' : 'cta-btn cta-btn--ghost-light';
    }

    updateMailtoLink();
    if (!silent) {
      showToast(isInv ? 'Vista adaptada para Inversionista' : 'Vista adaptada para Marca / Anunciante');
    }
  }

  document.querySelectorAll('[data-set-profile]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var targetProfile = btn.getAttribute('data-set-profile');
      setProfile(targetProfile, false);
      var scrollTarget = btn.getAttribute('data-scroll-next');
      if (scrollTarget) {
        if (body.classList.contains('deck')) {
          goToSlide(1);
        } else {
          var el = document.querySelector(scrollTarget);
          if (el) el.scrollIntoView({ behavior: RM ? 'auto' : 'smooth', block: 'start' });
        }
      }
    });
  });

  /* ======================================================================
     2. ANIMACIÓN COUNT-UP KPIs Y BARRAS DE MERCADO
     ====================================================================== */
  function animateCountUps() {
    document.querySelectorAll('.count-up').forEach(function (el) {
      if (el.getAttribute('data-done') === '1') return;
      el.setAttribute('data-done', '1');
      var target = parseFloat(el.getAttribute('data-target'));
      var fmt = el.getAttribute('data-format');
      if (RM) {
        el.textContent = fmt === 'dec2' ? target.toFixed(2).replace('.', ',') : formatInt(target);
        return;
      }
      var dur = 1100;
      var start = performance.now();
      function step(now) {
        var t = Math.min(1, (now - start) / dur);
        var ease = 1 - Math.pow(1 - t, 3);
        var cur = target * ease;
        el.textContent = fmt === 'dec2' ? cur.toFixed(2).replace('.', ',') : formatInt(cur);
        if (t < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }

  function animateMarketBars() {
    document.querySelectorAll('#market-chart .bar-fill').forEach(function (bar) {
      bar.style.width = bar.getAttribute('data-w') || '50%';
    });
  }

  /* ======================================================================
     3. ACTO 3 — COMPARADOR INTERACTIVO ANTES / DESPUÉS
     ====================================================================== */
  var compareData = {
    before: {
      score: '32 / 100',
      width: '32%',
      color: '#AA5959',
      pillars: [
        {
          title: 'Propiedad de la Audiencia',
          body: 'Terreno alquilado: dependes de cambios de algoritmo y si la plataforma limita el alcance, tu visibilidad cae de inmediato.',
          metric: 'Audiencia prestada'
        },
        {
          title: 'Seguridad de Marca',
          body: 'Tu anuncio aparece en medio de ruido, polarización o contenido no verificado, debilitando la percepción de marca.',
          metric: 'Solo 25% confianza en redes'
        },
        {
          title: 'Atención y Recordación',
          body: 'Publicaciones con vida útil de pocas horas compitiendo contra miles de videos y anuncios que el usuario omite en 1 segundo.',
          metric: 'CTR estándar 0,05%–0,10%'
        },
        {
          title: 'Hábito Diario (TRM)',
          body: 'Sin herramientas propias de consulta cotidiana: cada impacto requiere volver a pagar por interrumpir al usuario.',
          metric: 'Impacto efímero de 24h'
        },
        {
          title: 'Medición Transparente',
          body: 'Métricas superficiales ("alcance aproximado" o vistas fugaces) difíciles de conectar con decisiones reales de compra.',
          metric: 'Retorno difuso'
        }
      ]
    },
    after: {
      score: '94 / 100',
      width: '94%',
      color: '#052962',
      pillars: [
        {
          title: 'Propiedad de la Audiencia',
          body: 'Audiencia propia en somoslalupanews.com respaldada por Google, Google Discover (67,5% del tráfico móvil) y comunidad directa en WhatsApp/Boletín.',
          metric: 'Activo propio blindado'
        },
        {
          title: 'Seguridad de Marca',
          body: 'Entorno editorial limpio, ordenado y curado por periodistas. Tu marca transfiere confianza institucional a lectores de valor.',
          metric: '+9% afinidad de marca'
        },
        {
          title: 'Atención y Recordación',
          body: 'Formatos nativos, patrocinios de sección y notas patrocinadas leídas con atención real y sin saturación.',
          metric: '+53% atención · hasta 86% recuerdo'
        },
        {
          title: 'Hábito Diario (TRM)',
          body: 'Utilidad financiera consultada todos los días por empresarios, viajeros e importadores: un motivo real para volver cada mañana.',
          metric: '100% exclusividad diaria'
        },
        {
          title: 'Medición Transparente',
          body: 'Trazabilidad exacta de cada clic por espacio, reimpacto inteligente a lectores interesados y reporte ejecutivo mensual.',
          metric: 'Cero "pauta a ciegas"'
        }
      ]
    }
  };

  var cmpBeforeBtn = document.getElementById('cmp-before');
  var cmpAfterBtn = document.getElementById('cmp-after');
  var cmpFill = document.getElementById('cmp-meter-fill');
  var cmpScore = document.getElementById('cmp-meter-score');
  var pillarCards = Array.prototype.slice.call(document.querySelectorAll('#pillars-grid .pillar-card'));

  function setCompareState(mode) {
    var data = compareData[mode];
    var isBefore = mode === 'before';
    cmpBeforeBtn.setAttribute('aria-pressed', isBefore ? 'true' : 'false');
    cmpAfterBtn.setAttribute('aria-pressed', isBefore ? 'false' : 'true');
    cmpFill.style.width = data.width;
    cmpFill.style.background = data.color;
    cmpScore.textContent = data.score;
    cmpScore.style.color = data.color;

    pillarCards.forEach(function (card, i) {
      var item = data.pillars[i];
      card.classList.toggle('state-before', isBefore);
      card.classList.toggle('state-after', !isBefore);
      card.querySelector('h3').textContent = item.title;
      card.querySelector('.pillar-body').textContent = item.body;
      card.querySelector('.pillar-metric').textContent = item.metric;
    });
  }

  cmpBeforeBtn.addEventListener('click', function () { setCompareState('before'); });
  cmpAfterBtn.addEventListener('click', function () { setCompareState('after'); });

  /* ======================================================================
     4. ACTO 4 — VITRINA VIVA CON HOTSPOTS CLICABLES + SIMULADOR TRM
     ====================================================================== */
  var hotspots = {
    h1: {
      view: 'desktop',
      short: 'H1 · Cabecera',
      kicker: 'ZONA H1 · PRESENCIA INSTITUCIONAL',
      title: 'Cabecera Editorial & Navegación de Verticales',
      desc: 'Arquitectura de prensa digital sobria y confiable que organiza 20 verticales de interés nacional (Colombia, Política, Deportes, Mundo, Historias, Música y Opinión) más acceso directo a transmisiones En Vivo.',
      benefit: 'Transferencia inmediata de autoridad editorial desde el primer segundo en pantalla.',
      ideal: 'Marcas corporativas, consumo masivo, finanzas, entretenimiento y lanzamientos nacionales.',
      impact: '100% visibilidad inicial en el primer pantallazo (escritorio y móvil).',
      proof: 'Evidencia real: 4.583 publicaciones en archivo y navegación multi-sección operativa hoy.'
    },
    h2: {
      view: 'desktop',
      short: 'H2 · Joya TRM',
      kicker: 'ZONA H2 · PATROCINIO EXCLUSIVO DIARIO',
      title: 'Widget TRM Diario — Utilidad Financiera Viva',
      desc: 'Ubicado en posición de máximo privilegio justo bajo el menú principal, mostrando el valor actualizado del dólar cada día ($3,327 COP al 19 nov 2026). Es el imán más fuerte de visitas recurrentes del portal.',
      benefit: 'Exclusividad absoluta de categoría («Presentado por Tu Marca») sin compartir espacio con competidores.',
      ideal: 'Bancos, Fintechs, Remesadoras, Casas de Cambio, Aerolíneas, Aseguradoras y Comercio Exterior.',
      impact: 'Cero ceguera de banner: el lector busca activamente la cifra cada mañana.',
      proof: 'Evidencia real: Widget en vivo y actualizado diariamente en escritorio y móvil.'
    },
    h3: {
      view: 'desktop',
      short: 'H3 · Leaderboard',
      kicker: 'ZONA H3 · MEGA LEADERBOARD SUPERIOR',
      title: 'Banner Premium de Portada (Validado con Súper Astro)',
      desc: 'Franja horizontal panorámica inmediatamente debajo del indicador TRM y encima del titular principal. Garantiza impacto masivo inmediato apenas abre la portada.',
      benefit: 'Alta recordación visual en lanzamientos, promociones estacionales y campañas de posicionamiento.',
      ideal: 'Consumo masivo, entretenimiento, retail, telecomunicaciones y eventos nacionales.',
      impact: '100% visibilidad above-the-fold sin necesidad de hacer scroll.',
      proof: 'Evidencia real: Posición ya comercializada y activa con Súper Astro WEB.'
    },
    h3b: {
      view: 'desktop',
      short: 'H4 · Destacadas',
      kicker: 'ZONA DESTACADAS · INTEGRACIÓN NATIVA',
      title: 'Portada Principal & Columna Editorial Destacadas',
      desc: 'Zona de mayor tiempo de permanencia en portada donde conviven el titular del día y la curaduría de noticias destacadas — ideal para insertar contenido nativo integrado al diseño editorial.',
      benefit: '3x a 10x más clics que un banner estándar y +53% mayor tiempo de atención visual.',
      ideal: 'Empresas de servicios, educación, tecnología, salud, gastronomía y marcas con historia por contar.',
      impact: 'Integración natural que respeta la lectura y eleva +20,6% el brand lift.',
      proof: 'Evidencia real: Flujo editorial probado con cobertura nacional diaria.'
    },
    h4: {
      view: 'article',
      short: 'H4 · Patrocinio Sección',
      kicker: 'ZONA H4 · CASO REAL CAFÉ ÁGUILA ROJA',
      title: 'Patrocinio de Sección Editorial («Patrocinado por...»)',
      desc: 'Sello de marca integrado directamente en la cabecera de todos los artículos de una vertical estratégica (ejemplo real en producción: Café Águila Roja acompañando la cobertura de Deportes y Selección Colombia).',
      benefit: 'Asociación directa y repetida de tu marca con la pasión o tema favorito del lector.',
      ideal: 'Bebidas, café, alimentos, automotor, finanzas (Economía) y consumo masivo (Deportes).',
      impact: 'Presencia constante en cada artículo leído y compartido por WhatsApp o redes.',
      proof: 'Evidencia real: Sello «Patrocinado por Café Águila Roja» visible en somoslalupanews.com.'
    },
    h5: {
      view: 'article',
      short: 'H5 · Branded Content',
      kicker: 'ZONA H5 · FORMATO +90,5% EN COLOMBIA',
      title: 'Branded Content & Nota Patrocinada Editorial',
      desc: 'Artículos, crónicas y entrevistas elaboradas con estándar periodístico para explicar en profundidad tu propuesta de valor, lanzamiento o liderazgo sectorial, permaneciendo indexados en buscadores.',
      benefit: 'Construye credibilidad y educa al cliente antes de la venta con alto tiempo de lectura.',
      ideal: 'B2B, banca, inmobiliarias, salud, universidades, tecnología y reputación corporativa.',
      impact: 'Hasta 86% de recuerdo espontáneo y +15% a +18% en intención de compra.',
      proof: 'Formato de mayor crecimiento en Colombia según IAB (+90,5% YoY en Q2 2026).'
    },
    h6: {
      view: 'article',
      short: 'H6 · Lectura & Sidebar',
      kicker: 'ZONA H6 · LECTURA PROFUNDA SIN FRICCIÓN',
      title: 'Espacios Mid-Article & Columna Tendencias',
      desc: 'Ubicaciones estratégicas dentro del cuerpo del artículo y en la barra lateral de Últimas Noticias / Tendencias que acompañan al lector mientras consume la historia completa.',
      benefit: 'Captura atención en el punto de mayor concentración del usuario, con enlaces trazables.',
      ideal: 'Campañas de generación de contactos, reimpacto inteligente y recordación de marca.',
      impact: 'Alta visibilidad durante lectura activa y navegación entre artículos relacionados.',
      proof: 'Evidencia real: Plantilla de artículo limpia con botones de compartir en WhatsApp, X, FB y LinkedIn.'
    },
    h7a: {
      view: 'mobile',
      short: '7A · TRM Móvil',
      kicker: 'ZONA MÓVIL 7A · 75% DE LECTORES EN COLOMBIA',
      title: 'Widget TRM Responsivo en 3 Columnas Claras',
      desc: 'En smartphone, el indicador diario del dólar se adapta limpiamente sin cortes ni desbordamientos, conservando el protagonismo del primer pantallazo móvil.',
      benefit: 'Tu patrocinio exclusivo acompaña al usuario directamente en la palma de su mano cada mañana.',
      ideal: 'Fintechs móviles, billeteras digitales, remesadoras, bancos y agencias de viaje.',
      impact: 'Máxima legibilidad en el dispositivo donde el 75% de Colombia consulta noticias.',
      proof: 'Evidencia real: Captura móvil real verificada a 390px sin obstrucciones.'
    },
    h7b: {
      view: 'mobile',
      short: '7B · Banner Móvil',
      kicker: 'ZONA MÓVIL 7B · IMPACTO INMEDIATO',
      title: 'Banner Superior Móvil Above-the-Fold',
      desc: 'Formato panorámico optimizado para celular justo entre la TRM y el titular principal, logrando impacto instantáneo sin tapar el texto ni generar ventanas invasivas.',
      benefit: 'Experiencia amigable que evita rechazos y maximiza clics genuinos desde celular.',
      ideal: 'Lanzamientos masivos, comercio electrónico, apps y campañas con botón directo a WhatsApp.',
      impact: '100% visible al abrir cualquier enlace compartido por WhatsApp o Instagram.',
      proof: 'Evidencia real: Creativo móvil activo y legible en somoslalupanews.com.'
    },
    h7c: {
      view: 'mobile',
      short: '7C · Lectura Móvil',
      kicker: 'ZONA MÓVIL 7C · EXPERIENCIA LIMPIA',
      title: 'Lectura Fluida para Tráfico Social y Discover',
      desc: 'Diseño editorial pensado para quienes llegan desde WhatsApp, Reels o Google Discover: tipografía clara, fotografía protagonista y transición ágil hacia nuevas historias.',
      benefit: 'Mayor permanencia en página y mejor desempeño para notas patrocinadas en celular.',
      ideal: 'Marcas que invierten en video vertical y desean convertir curiosidad en lectura profunda.',
      impact: 'Alineado con el 67,5% de tráfico móvil de noticias proveniente de descubrimiento editorial.',
      proof: 'Evidencia real: Interfaz móvil limpia y ordenada verificada en producción.'
    },
    h8: {
      view: 'full',
      short: 'H8 · Half-Page 300×600',
      kicker: 'ZONA H8 · INVENTARIO DISPLAY MULTI-POSICIÓN',
      title: 'Grilla Display & Half-Page Lateral (300×600)',
      desc: 'Espacio vertical de gran formato junto al bloque de Deportes y actualidad, complementado por franjas horizontales de separación entre secciones para campañas de cobertura sostenida.',
      benefit: 'Gran lienzo creativo para destacar producto, oferta visual y llamado a la acción claro.',
      ideal: 'Inmobiliarias, vehículos, retail, educación superior y marcas de consumo masivo.',
      impact: 'Uno de los formatos display con mayor tasa de visibilidad sostenida durante el desplazamiento.',
      proof: 'Evidencia real: 6 posiciones display verificadas en la portada completa.'
    },
    h9: {
      view: 'full',
      short: 'H9 · Encuesta & Video',
      kicker: 'ZONA H9 · PARTICIPACIÓN Y AUDIOVISUAL',
      title: 'Encuesta «Tu Mirada» & Vitrina YouTube en Portada',
      desc: 'Módulos dedicados a la interacción directa del lector (encuestas de coyuntura patrocinables) y exhibición audiovisual integrada con los contenidos en video del medio y programas en vivo.',
      benefit: 'Conecta tu marca con formatos participativos y el formato digital #1 en inversión (Video: 32,1% share).',
      ideal: 'Marcas que buscan interacción, sondeos de opinión, patrocinio de entrevistas o podcasts.',
      impact: 'Combina lectura web + participación interactiva + exposición audiovisual en una sola campaña.',
      proof: 'Evidencia real: Módulos «Tu Mirada en La Lupa News» y «La Lupa News en YouTube» ya presentes.'
    }
  };

  var viewHotspotMap = {
    desktop: ['h1', 'h2', 'h3', 'h3b'],
    article: ['h4', 'h5', 'h6'],
    mobile: ['h7a', 'h7b', 'h7c'],
    full: ['h8', 'h9']
  };

  var viewUrlMap = {
    desktop: 'https://somoslalupanews.com/  ·  Vista Escritorio',
    article: 'https://somoslalupanews.com/deportes/seleccion-colombia-mundial-2026/',
    mobile: 'https://somoslalupanews.com/  ·  Vista Smartphone (390px)',
    full: 'https://somoslalupanews.com/  ·  Arquitectura Completa de Portada'
  };

  var hsPillsEl = document.getElementById('hs-pills');
  var hsKicker = document.getElementById('hs-kicker');
  var hsTitle = document.getElementById('hs-title');
  var hsDesc = document.getElementById('hs-desc');
  var hsBenefit = document.getElementById('hs-benefit');
  var hsIdeal = document.getElementById('hs-ideal');
  var hsImpact = document.getElementById('hs-impact');
  var hsProof = document.getElementById('hs-proof');
  var browserUrlEl = document.getElementById('browser-url');

  function selectHotspot(hsId) {
    var data = hotspots[hsId];
    if (!data) return;

    hsKicker.textContent = data.kicker;
    hsTitle.textContent = data.title;
    hsDesc.textContent = data.desc;
    hsBenefit.textContent = data.benefit;
    hsIdeal.textContent = data.ideal;
    hsImpact.textContent = data.impact;
    hsProof.textContent = data.proof;

    document.querySelectorAll('.hs-pin').forEach(function (pin) {
      pin.classList.toggle('active', pin.getAttribute('data-hs') === hsId);
    });
    document.querySelectorAll('.hs-chip').forEach(function (chip) {
      chip.classList.toggle('active', chip.getAttribute('data-hs') === hsId);
    });
  }

  function renderViewChips(viewKey, activeHs) {
    var list = viewHotspotMap[viewKey] || [];
    hsPillsEl.innerHTML = '';
    list.forEach(function (id) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'hs-chip' + (id === activeHs ? ' active' : '');
      btn.setAttribute('data-hs', id);
      btn.textContent = hotspots[id].short;
      btn.addEventListener('click', function () { selectHotspot(id); });
      hsPillsEl.appendChild(btn);
    });
  }

  function switchView(viewKey) {
    document.querySelectorAll('.view-tab').forEach(function (t) {
      t.setAttribute('aria-selected', t.getAttribute('data-view') === viewKey ? 'true' : 'false');
    });
    document.querySelectorAll('.view-pane').forEach(function (p) {
      p.hidden = p.id !== 'pane-' + viewKey;
    });
    browserUrlEl.textContent = viewUrlMap[viewKey] || 'https://somoslalupanews.com/';
    var firstHs = viewHotspotMap[viewKey][0];
    renderViewChips(viewKey, firstHs);
    selectHotspot(firstHs);
  }

  document.querySelectorAll('.view-tab').forEach(function (tab) {
    tab.addEventListener('click', function () {
      switchView(tab.getAttribute('data-view'));
    });
  });

  document.querySelectorAll('.hs-pin').forEach(function (pin) {
    pin.addEventListener('click', function () {
      selectHotspot(pin.getAttribute('data-hs'));
    });
  });

  var fullScroll = document.getElementById('fullpage-scroll');
  document.querySelectorAll('.jump-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      if (!fullScroll) return;
      var frac = parseFloat(btn.getAttribute('data-jump') || '0');
      fullScroll.scrollTo({
        top: Math.round(fullScroll.scrollHeight * frac),
        behavior: RM ? 'auto' : 'smooth'
      });
      var selHs = btn.getAttribute('data-select-hs');
      if (selHs) selectHotspot(selHs);
    });
  });

  // Inicializar chips de vista 1
  renderViewChips('desktop', 'h1');

  // Simulador interactivo de Co-Branding TRM
  var trmBrandOut = document.getElementById('trm-brand-output');
  var trmCtaOut = document.getElementById('trm-cta-output');
  var trmInput = document.getElementById('trm-brand-input');
  var trmPresets = Array.prototype.slice.call(document.querySelectorAll('.trm-preset'));

  trmPresets.forEach(function (btn) {
    btn.addEventListener('click', function () {
      trmPresets.forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      trmBrandOut.textContent = btn.getAttribute('data-brand');
      trmCtaOut.textContent = btn.getAttribute('data-cta');
      if (trmInput) trmInput.value = '';
    });
  });

  if (trmInput) {
    trmInput.addEventListener('input', function () {
      var val = trmInput.value.trim();
      trmPresets.forEach(function (b) { b.classList.remove('active'); });
      if (val.length > 0) {
        trmBrandOut.textContent = val;
        var shortBrand = val.length > 28 ? val.slice(0, 27).trim() + '…' : val;
        trmCtaOut.textContent = 'Conoce más en ' + shortBrand + ' →';
      } else {
        trmBrandOut.textContent = 'Tu Banco / Fintech';
        trmCtaOut.textContent = 'Cotiza dólar hoy →';
        if (trmPresets[0]) trmPresets[0].classList.add('active');
      }
    });
  }

  /* ======================================================================
     5. ACTO 5 — HOJA DE RUTA INTERACTIVA 90 DÍAS
     ====================================================================== */
  var roadmapPhases = [
    {
      items: [
        'Reactivación del ritmo editorial diario con foco en Colombia, Deportes, Economía y actualidad.',
        'Sincronización completa de las 6 redes sociales hacia somoslalupanews.com y refuerzo de identidad ejecutiva.',
        'Puesta en marcha del tablero comercial de medición transparente y lanzamiento junto a Javier Fernández Franco.'
      ],
      deliverable: 'Portal renovado, ecosistema social unificado y primer reporte base de audiencia verificada para anunciantes pioneros.'
    },
    {
      items: [
        'Despliegue de campaña inteligente de captación de lectores calificados en Colombia.',
        'Lanzamiento del Canal Oficial de WhatsApp y del Boletín Ejecutivo Diario para construir audiencia propia.',
        'Producción constante de video vertical (fórmula 1 noticia = 6 formatos) y activación de primeros patrocinadores fundadores.'
      ],
      deliverable: 'Crecimiento medible de visitas web, comunidad recurrente en WhatsApp y patrocinio activo del indicador TRM / secciones.'
    },
    {
      items: [
        'Activación de audiencias de reimpacto inteligente para elevar la conversión de las marcas anunciantes.',
        'Comercialización de paquetes integrados 360° (Portal Web + Video + Redes + Comunidad Propia).',
        'Optimización comercial de las verticales de mayor retorno (Deportes, Economía y Actualidad Nacional).'
      ],
      deliverable: 'Tablero ejecutivo de retorno por anunciante, renovaciones recurrentes y proyecciones financieras validadas con datos reales.'
    }
  ];

  var roadBtns = Array.prototype.slice.call(document.querySelectorAll('.road-btn'));
  var roadList = document.getElementById('road-list');
  var roadDeliv = document.getElementById('road-deliv');

  roadBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var idx = parseInt(btn.getAttribute('data-phase'), 10);
      var phase = roadmapPhases[idx];
      if (!phase) return;
      roadBtns.forEach(function (b) { b.setAttribute('aria-selected', b === btn ? 'true' : 'false'); });
      roadList.innerHTML = '';
      phase.items.forEach(function (t) {
        var li = document.createElement('li');
        li.textContent = t;
        roadList.appendChild(li);
      });
      roadDeliv.textContent = phase.deliverable;
    });
  });

  /* ======================================================================
     6. ACTO 6 — SIMULADOR INTERACTIVO DUAL
     ====================================================================== */
  var slBudget = document.getElementById('sl-budget');
  var slMonths = document.getElementById('sl-months');
  var valBudget = document.getElementById('val-budget');
  var valMonths = document.getElementById('val-months');
  var pkgChecks = Array.prototype.slice.call(document.querySelectorAll('#pkg-grid input[type="checkbox"]'));

  var resMarcaTitle = document.getElementById('res-marca-title');
  var resImpr = document.getElementById('res-impr');
  var resClicks = document.getElementById('res-clicks');
  var resCtr = document.getElementById('res-ctr');
  var resLift = document.getElementById('res-lift');
  var resTotal = document.getElementById('res-total');
  var resBonif = document.getElementById('res-bonif');
  var resDelivs = document.getElementById('res-deliverables');
  var mBar1 = document.getElementById('m-bar1');
  var mBar2 = document.getElementById('m-bar2');
  var mBar3 = document.getElementById('m-bar3');
  var mBar1v = document.getElementById('m-bar1-v');
  var mBar2v = document.getElementById('m-bar2-v');
  var mBar3v = document.getElementById('m-bar3-v');

  var lastMarcaSummary = '';
  var lastInversorSummary = '';

  function calcMarca() {
    var budgetM = parseInt(slBudget.value, 10);
    var months = parseInt(slMonths.value, 10);
    var selected = [];
    pkgChecks.forEach(function (cb) {
      var lbl = cb.closest('.pkg-opt');
      if (cb.checked) {
        selected.push(cb.value);
        if (lbl) lbl.classList.add('checked');
      } else {
        if (lbl) lbl.classList.remove('checked');
      }
    });

    if (selected.length === 0) {
      pkgChecks[0].checked = true;
      pkgChecks[0].closest('.pkg-opt').classList.add('checked');
      selected.push('trm');
    }

    valBudget.textContent = formatCOP(budgetM) + ' COP';
    valMonths.textContent = months + (months === 1 ? ' mes' : ' meses');

    var hasTrm = selected.indexOf('trm') >= 0;
    var hasBranded = selected.indexOf('branded') >= 0;
    var hasDisplay = selected.indexOf('display') >= 0;
    var hasVideo = selected.indexOf('video') >= 0;

    // Benchmarks ilustrativos Colombia 2025-2026 (~$16k-$24k COP CPM efectivo integrado según mezcla)
    var imprLow = budgetM * months * 13500;
    var imprHigh = budgetM * months * 20500;
    if (hasDisplay) { imprLow *= 1.18; imprHigh *= 1.22; }

    var ctrLow = 0.0045;
    var ctrHigh = 0.0085;
    if (hasBranded || hasTrm) { ctrLow = 0.0062; ctrHigh = 0.0108; }
    if (hasVideo) { ctrLow += 0.0008; ctrHigh += 0.0012; }

    var clicksLow = imprLow * ctrLow;
    var clicksHigh = imprHigh * ctrHigh;

    var liftText = hasBranded ? '+24% a +86%' : (hasTrm ? '+22% a +58%' : '+15% a +38%');
    var totalM = budgetM * months;
    var bonifText = months >= 6 ? 'Incluye prioridad anual + bonificación de lanzamiento'
      : (months >= 3 ? 'Tarifa preferencial de relanzamiento incluida' : 'Formato piloto medible desde el mes 1');

    var pPortal = hasTrm || hasBranded ? 52 : 40;
    var pSocial = hasVideo || hasDisplay ? 32 : 28;
    var pRetarget = 100 - pPortal - pSocial;

    mBar1.style.width = pPortal + '%'; mBar1v.textContent = pPortal + '%';
    mBar2.style.width = pSocial + '%'; mBar2v.textContent = pSocial + '%';
    mBar3.style.width = pRetarget + '%'; mBar3v.textContent = pRetarget + '%';

    var planLabel = selected.length >= 3 ? 'Campaña Integral 360°'
      : (hasTrm && hasBranded ? 'Plan Combinado TRM + Editorial'
        : (hasTrm ? 'Patrocinio Exclusivo Widget TRM'
          : (hasBranded ? 'Branded Content & Patrocinio de Sección' : 'Campaña Display & Amplificación')));

    resMarcaTitle.textContent = planLabel + ' · ' + months + (months === 1 ? ' Mes' : ' Meses');
    resImpr.textContent = formatInt(imprLow) + ' – ' + formatInt(imprHigh);
    resClicks.textContent = formatInt(clicksLow) + ' – ' + formatInt(clicksHigh);
    resCtr.textContent = 'CTR ref. ' + (ctrLow * 100).toFixed(2).replace('.', ',') + '%–' + (ctrHigh * 100).toFixed(2).replace('.', ',') + '% (3x–10x vs. banner)';
    resLift.textContent = liftText;
    resTotal.textContent = formatCOP(totalM);
    resBonif.textContent = bonifText;

    var pills = ['✓ Reporte ejecutivo mensual', '✓ Trazabilidad exacta de clics'];
    if (hasTrm) pills.push('✓ 100% Exclusividad Widget TRM');
    if (hasBranded) pills.push('✓ Producción Branded Content');
    if (hasDisplay || hasVideo) pills.push('✓ Amplificación Multicanal');
    pills.push('✓ Reimpacto inteligente');
    resDelivs.innerHTML = pills.map(function (p) { return '<span class="deliv-pill">' + p + '</span>'; }).join('');

    lastMarcaSummary = 'Hola equipo de Somos La Lupa News,\n\n'
      + 'Acabo de explorar el Pitch Comercial como Marca/Anunciante con el siguiente escenario de interés:\n'
      + '• Enfoque: ' + planLabel + '\n'
      + '• Presupuesto mensual estimado: ' + formatCOP(budgetM) + ' COP\n'
      + '• Duración: ' + months + (months === 1 ? ' mes' : ' meses') + ' (Total estimado: ' + formatCOP(totalM) + ' COP)\n'
      + '• Exposición ilustrativa: ' + formatInt(imprLow) + ' – ' + formatInt(imprHigh) + ' impresiones\n\n'
      + 'Me gustaría agendar una reunión con Javier Fernández Franco para revisar disponibilidad de cupos de lanzamiento.';

    updateMailtoLink();
  }

  pkgChecks.forEach(function (cb) { cb.addEventListener('change', calcMarca); });
  slBudget.addEventListener('input', calcMarca);
  slMonths.addEventListener('input', calcMarca);

  // Simulador Inversionista
  var slCap = document.getElementById('sl-cap');
  var slHorizon = document.getElementById('sl-horizon');
  var valCap = document.getElementById('val-cap');
  var valHorizon = document.getElementById('val-horizon');
  var scenBtns = Array.prototype.slice.call(document.querySelectorAll('.scen-btn'));
  var activeScen = 'base';

  var scenConfig = {
    conservador: { label: 'Conservador', mult: 0.24, mix: [36, 26, 24, 14], clients: '4 a 6 marcas' },
    base:        { label: 'Base Recomendado', mult: 0.34, mix: [30, 32, 23, 15], clients: '6 a 9 marcas' },
    acelerado:   { label: 'Acelerado', mult: 0.45, mix: [24, 38, 22, 16], clients: '9 a 14 marcas' }
  };

  function calcInversor() {
    var capM = parseInt(slCap.value, 10);
    var horizon = parseInt(slHorizon.value, 10);
    var cfg = scenConfig[activeScen];

    valCap.textContent = formatCOP(capM) + ' COP';
    valHorizon.textContent = horizon + ' meses';

    document.getElementById('cap-35').textContent = '$' + (capM * 0.35).toFixed(1).replace('.', ',') + 'M';
    document.getElementById('cap-30').textContent = '$' + (capM * 0.30).toFixed(1).replace('.', ',') + 'M';
    document.getElementById('cap-20').textContent = '$' + (capM * 0.20).toFixed(1).replace('.', ',') + 'M';
    document.getElementById('cap-15').textContent = '$' + (capM * 0.15).toFixed(1).replace('.', ',') + 'M';

    var ramp = 0.45 + (horizon / 12) * 0.55;
    var revLow = Math.round(capM * cfg.mult * ramp * 0.85);
    var revHigh = Math.round(capM * cfg.mult * ramp * 1.18);

    document.getElementById('res-inv-title').textContent = 'Escenario ' + cfg.label + ' · ' + horizon + ' Meses';
    document.getElementById('res-inv-rev').textContent = '$' + revLow + 'M – $' + revHigh + 'M';
    document.getElementById('res-inv-clients').textContent = cfg.clients;

    // Actualizar gráfico SVG donut
    var m = cfg.mix;
    var offset = 25;
    var ids = ['seg-trm', 'seg-bc', 'seg-sec', 'seg-disp'];
    var legs = ['leg-trm', 'leg-bc', 'leg-sec', 'leg-disp'];
    for (var i = 0; i < 4; i++) {
      var seg = document.getElementById(ids[i]);
      if (seg) {
        seg.setAttribute('stroke-dasharray', m[i] + ' ' + (100 - m[i]));
        seg.setAttribute('stroke-dashoffset', String(offset));
        offset -= m[i];
      }
      var leg = document.getElementById(legs[i]);
      if (leg) leg.textContent = m[i] + '%';
    }

    lastInversorSummary = 'Hola Javier Fernández Franco y equipo de Somos La Lupa News,\n\n'
      + 'Acabo de revisar la Tesis de Inversión y escalamiento con el siguiente escenario:\n'
      + '• Escenario: ' + cfg.label + '\n'
      + '• Inyección de capital analizada: ' + formatCOP(capM) + ' COP\n'
      + '• Horizonte de escalamiento: ' + horizon + ' meses\n'
      + '• Ritmo ilustrativo de ingresos al cierre: $' + revLow + 'M – $' + revHigh + 'M COP/mes\n\n'
      + 'Me gustaría agendar una sesión ejecutiva para conocer las proyecciones detalladas y estructura de participación.';

    updateMailtoLink();
  }

  scenBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      activeScen = btn.getAttribute('data-scen');
      scenBtns.forEach(function (b) { b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
      calcInversor();
    });
  });
  slCap.addEventListener('input', calcInversor);
  slHorizon.addEventListener('input', calcInversor);

  function getActiveSummary() {
    return body.getAttribute('data-profile') === 'inversor' ? lastInversorSummary : lastMarcaSummary;
  }

  function updateMailtoLink() {
    var isInv = body.getAttribute('data-profile') === 'inversor';
    var subject = isInv
      ? 'Sesión de Inversión — Somos La Lupa News'
      : 'Propuesta Comercial / Patrocinio — Somos La Lupa News';
    var href = 'mailto:lalupanewsco@gmail.com?subject=' + encodeURIComponent(subject)
      + '&body=' + encodeURIComponent(getActiveSummary());
    var ctaMailto = document.getElementById('cta-mailto');
    var modalMail = document.getElementById('modal-email-link');
    if (ctaMailto) ctaMailto.setAttribute('href', href);
    if (modalMail) modalMail.setAttribute('href', href);
  }

  function copySummary(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () {
        showToast('Resumen copiado al portapapeles ✓');
      }).catch(function () {
        showToast('Abre el modal para copiar manualmente');
      });
    } else {
      showToast('Abre el modal para copiar manualmente');
    }
  }

  document.getElementById('btn-copy-sim-marca').addEventListener('click', function () { copySummary(lastMarcaSummary); });
  document.getElementById('btn-copy-sim-inversor').addEventListener('click', function () { copySummary(lastInversorSummary); });
  document.getElementById('btn-copy-closing').addEventListener('click', function () { copySummary(getActiveSummary()); });

  /* ======================================================================
     7. MODAL DE CONTACTO DIRECTO
     ====================================================================== */
  var modal = document.getElementById('contact-modal');
  var modalText = document.getElementById('modal-textarea');

  function openModal() {
    modalText.value = getActiveSummary();
    modal.classList.add('open');
  }
  function closeModal() {
    modal.classList.remove('open');
  }

  document.getElementById('btn-open-modal').addEventListener('click', openModal);
  document.getElementById('modal-close').addEventListener('click', closeModal);
  document.getElementById('modal-copy').addEventListener('click', function () {
    copySummary(modalText.value);
  });
  modal.addEventListener('click', function (e) {
    if (e.target === modal) closeModal();
  });

  /* ======================================================================
     8. SCROLL REVEAL, SCROLL SPY & MODO PRESENTACIÓN (F)
     ====================================================================== */
  if ('IntersectionObserver' in window) {
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('on');
          if (entry.target.id === 'market-chart' || entry.target.closest('#act-2')) {
            animateMarketBars();
          }
          obs.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    document.querySelectorAll('.rv').forEach(function (el) { obs.observe(el); });
  } else {
    document.querySelectorAll('.rv').forEach(function (el) { el.classList.add('on'); });
    animateMarketBars();
  }

  // Acto 1 visible de inmediato
  document.querySelectorAll('#act-1 .rv').forEach(function (el) { el.classList.add('on'); });
  animateCountUps();

  function renderDeck() {
    track.style.setProperty('--i', String(currentSlide));
    railDots.forEach(function (d, i) { d.setAttribute('aria-current', i === currentSlide ? 'true' : 'false'); });
    dtitle.textContent = slides[currentSlide].getAttribute('data-t') || '';
    dcount.textContent = String(currentSlide + 1).padStart(2, '0') + ' / ' + String(slides.length).padStart(2, '0');
    prog.style.width = ((currentSlide + 1) / slides.length * 100) + '%';
    if (currentSlide === 1) animateMarketBars();
  }

  function goToSlide(idx) {
    currentSlide = Math.max(0, Math.min(slides.length - 1, idx));
    if (body.classList.contains('deck')) {
      renderDeck();
    } else {
      slides[currentSlide].scrollIntoView({ behavior: RM ? 'auto' : 'smooth', block: 'start' });
    }
  }

  function setDeckMode(on) {
    if (on) {
      var mid = window.scrollY + window.innerHeight * 0.4;
      var cur = 0;
      slides.forEach(function (s, i) {
        if (s.getBoundingClientRect().top + window.scrollY <= mid) cur = i;
      });
      currentSlide = cur;
    }
    body.classList.toggle('deck', on);
    deckBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
    deckBtn.innerHTML = on
      ? '<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3 5v14h18V5H3zm16 12H5V7h14v10z"/></svg> <span class="btn-txt-hide">Lectura</span> [Esc]'
      : '<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H8V4h12v12z"/></svg> <span class="btn-txt-hide">Presentación</span> [F]';

    if (on) {
      renderDeck();
      animateMarketBars();
    } else {
      track.style.removeProperty('--i');
      setTimeout(function () {
        slides[currentSlide].scrollIntoView({ block: 'start' });
        onScroll();
      }, 30);
    }
  }

  deckBtn.addEventListener('click', function () { setDeckMode(!body.classList.contains('deck')); });
  dprev.addEventListener('click', function () { goToSlide(currentSlide - 1); });
  dnext.addEventListener('click', function () { goToSlide(currentSlide + 1); });

  railDots.forEach(function (dot) {
    dot.addEventListener('click', function () {
      goToSlide(parseInt(dot.getAttribute('data-idx'), 10));
    });
  });

  function onScroll() {
    if (body.classList.contains('deck')) return;
    var max = document.documentElement.scrollHeight - window.innerHeight;
    prog.style.width = (max > 0 ? (window.scrollY / max * 100) : 0) + '%';
    var mid = window.scrollY + window.innerHeight * 0.4;
    var cur = 0;
    slides.forEach(function (s, i) {
      if (s.getBoundingClientRect().top + window.scrollY <= mid) cur = i;
    });
    currentSlide = cur;
    railDots.forEach(function (d, i) { d.setAttribute('aria-current', i === cur ? 'true' : 'false'); });
  }

  var scrollTick = false;
  window.addEventListener('scroll', function () {
    if (scrollTick) return;
    scrollTick = true;
    requestAnimationFrame(function () {
      onScroll();
      scrollTick = false;
    });
  }, { passive: true });

  // Teclado (F, Flechas, Esc)
  document.addEventListener('keydown', function (e) {
    var t = e.target;
    if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;

    if (e.key === 'Escape' && modal.classList.contains('open')) {
      closeModal();
      return;
    }
    if (e.key === 'f' || e.key === 'F') {
      e.preventDefault();
      setDeckMode(!body.classList.contains('deck'));
      return;
    }
    if (!body.classList.contains('deck')) return;

    if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {
      e.preventDefault();
      goToSlide(currentSlide + 1);
    } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
      e.preventDefault();
      goToSlide(currentSlide - 1);
    } else if (e.key === 'Home') {
      e.preventDefault();
      goToSlide(0);
    } else if (e.key === 'End') {
      e.preventDefault();
      goToSlide(slides.length - 1);
    } else if (e.key === 'Escape') {
      e.preventDefault();
      setDeckMode(false);
    }
  });

  // Swipe táctil en Modo Presentación
  var sx = 0, sy = 0;
  document.addEventListener('touchstart', function (e) {
    sx = e.touches[0].clientX;
    sy = e.touches[0].clientY;
  }, { passive: true });
  document.addEventListener('touchend', function (e) {
    if (!body.classList.contains('deck')) return;
    var dx = e.changedTouches[0].clientX - sx;
    var dy = e.changedTouches[0].clientY - sy;
    if (Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy) * 1.4) {
      goToSlide(currentSlide + (dx < 0 ? 1 : -1));
    }
  }, { passive: true });

  // Exportar PDF
  printBtn.addEventListener('click', function () {
    if (body.classList.contains('deck')) setDeckMode(false);
    document.querySelectorAll('.rv').forEach(function (n) { n.classList.add('on'); });
    animateMarketBars();
    setTimeout(function () { window.print(); }, 260);
  });

  // Inicialización de cálculos
  calcMarca();
  calcInversor();
  setProfile('marca', true);
  onScroll();
})();
</script>
</body>
</html>
"""


FORBIDDEN_PATTERNS = [
    r"homo\s*ludens",
    r"huizinga",
    r"teor[ií]a\s+del\s+juego",
    r"gamificaci[oó]n",
    r"gamification",
    r"circle\s+of\s+play",
    r"c[ií]rculo\s+m[aá]gico",
    r"cialdini",
    r"wordpress",
    r"elementor",
    r"json-ld",
    r"\bdns\b",
    r"\brdap\b",
    r"litespeed",
    r"scraping",
    r"p[ií]xel",
    r"\butm",
    r"cookie",
    r"dropcatch",
    r"localhost",
    r"daniel\s+moncada",
    r"g[eé]nesis\s+legal",
    r"#1a3a5c",
    r"#2d124d",
    r"#b8842a",
    r"nomack",
]


def verify_output(html: str) -> None:
    unresolved = re.findall(r"__[A-Z0-9_]+__", html)
    if unresolved:
        raise RuntimeError(f"Unresolved template placeholders found: {set(unresolved)}")

    # Strip base64 data URIs before scanning text so random base64 bytes don't false-positive
    html_no_b64 = re.sub(r"data:image/[a-zA-Z0-9+.-]+;base64,[A-Za-z0-9+/=]+", "DATA_URI", html)
    violations = []
    for pat in FORBIDDEN_PATTERNS:
        m = re.search(pat, html_no_b64, flags=re.IGNORECASE)
        if m:
            violations.append((pat, m.group(0)))
    if violations:
        raise RuntimeError(f"Forbidden content detected in generated HTML: {violations}")


def main() -> int:
    assets = build_assets()
    html = HTML_TEMPLATE
    for key, val in assets.items():
        html = html.replace(f"__{key}__", val)

    verify_output(html)

    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(html, encoding="utf-8")
    size_bytes = OUT_HTML.stat().st_size
    print(f"\n[OK] Built standalone Pitch HTML:")
    print(f"     Path: {OUT_HTML}")
    print(f"     Size: {size_bytes:,} bytes ({size_bytes / (1024 * 1024):.2f} MB)")
    print(f"     Compliance check: PASSED (0 forbidden strings, 0 unresolved placeholders)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
