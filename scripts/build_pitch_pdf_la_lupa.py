#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates a museum-grade widescreen vector PDF copy of the interactive pitch deck:
  Input  (READ-ONLY): deliverables/pitch_comercial/Presentacion_Pitch_Comercial_Somos_La_Lupa_News.html
  Output (VECTOR PDF): deliverables/pitch_comercial/Presentacion_Pitch_Comercial_Somos_La_Lupa_News.pdf

Renders via Playwright Chromium in screen media mode (preserving all gradients,
vector typography, SVG charts, shadows, and embedded logos/captures) with
runtime-only DOM/CSS slide composition. The source HTML file is NEVER modified.
"""

import hashlib
import os
import sys
from pathlib import Path

import fitz  # PyMuPDF
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent.parent
SRC_HTML = ROOT / "deliverables" / "pitch_comercial" / "Presentacion_Pitch_Comercial_Somos_La_Lupa_News.html"
OUT_PDF = ROOT / "deliverables" / "pitch_comercial" / "Presentacion_Pitch_Comercial_Somos_La_Lupa_News.pdf"

SLIDE_W = 1440
SLIDE_H = 900


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


PDF_CSS = r"""
@page {
  size: 1440px 900px;
  margin: 0;
}

* {
  -webkit-print-color-adjust: exact !important;
  print-color-adjust: exact !important;
  animation: none !important;
  transition: none !important;
}

html, body {
  width: 1440px !important;
  margin: 0 !important;
  padding: 0 !important;
  background: #041F4A !important;
  overflow: visible !important;
}

/* Hide interactive-only chrome */
.topbar, .rail, .deckbar, .scroll-cue, #toast, .modal-backdrop, .print-banner, .prog {
  display: none !important;
}

#pdf-deck {
  width: 1440px;
  margin: 0;
  padding: 0;
}

.pdf-slide {
  width: 1440px;
  height: 900px;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 28px 54px 24px;
  box-sizing: border-box;
  page-break-after: always;
  break-after: page;
}

.pdf-slide:last-child {
  page-break-after: auto;
  break-after: auto;
}

.pdf-slide--navy {
  background: linear-gradient(155deg, #052962 0%, #041F4A 62%, #02132F 100%);
  color: #FFFFFF;
}

.pdf-slide--paper {
  background: #FFFFFF;
  color: #02132F;
}

.pdf-slide--surface {
  background: #F7F7F7;
  color: #02132F;
}

/* Slide running header & footer */
.pdf-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 12px;
  margin-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.14);
  flex-shrink: 0;
  position: relative;
  z-index: 5;
}

.pdf-slide--paper .pdf-header,
.pdf-slide--surface .pdf-header {
  border-bottom-color: #DEE2E6;
}

.pdf-header-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.pdf-header-brand img {
  height: 28px;
  width: auto;
}

.pdf-header-sep {
  width: 1px;
  height: 18px;
  background: rgba(255, 255, 255, 0.24);
}

.pdf-slide--paper .pdf-header-sep,
.pdf-slide--surface .pdf-header-sep {
  background: #CED4DA;
}

.pdf-header-act {
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #D4C914;
}

.pdf-slide--paper .pdf-header-act,
.pdf-slide--surface .pdf-header-act {
  color: #AA5959;
}

.pdf-header-right {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #9CB4D4;
}

.pdf-slide--paper .pdf-header-right,
.pdf-slide--surface .pdf-header-right {
  color: #69727D;
}

.pdf-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
  z-index: 4;
  min-height: 0;
}

.pdf-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 10px;
  margin-top: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.12);
  font-size: 0.72rem;
  color: #9CB4D4;
  flex-shrink: 0;
  position: relative;
  z-index: 5;
}

.pdf-slide--paper .pdf-footer,
.pdf-slide--surface .pdf-footer {
  border-top-color: #DEE2E6;
  color: #69727D;
}

.pdf-page-num {
  font-weight: 800;
  letter-spacing: 0.1em;
  color: #D4C914;
}

.pdf-slide--paper .pdf-page-num,
.pdf-slide--surface .pdf-page-num {
  color: #052962;
}

/* Force revealed state & lock 1440px desktop grids against print media-query width */
.rv {
  opacity: 1 !important;
  transform: none !important;
}
.pdf-slide .hero-kpis { grid-template-columns: repeat(4, minmax(0, 1fr)) !important; }
.pdf-slide .stat-grid-4 { grid-template-columns: repeat(4, minmax(0, 1fr)) !important; }
.pdf-slide .market-split { grid-template-columns: 1.25fr 1fr !important; }
.pdf-slide .trm-benefits-row { grid-template-columns: repeat(3, minmax(0, 1fr)) !important; }
.pdf-slide .authority-strip { grid-template-columns: repeat(3, minmax(0, 1fr)) !important; }
.pdf-slide .social-grid { grid-template-columns: repeat(4, minmax(0, 1fr)) !important; }
.pdf-slide .founder-spotlight { grid-template-columns: 1.38fr 1fr !important; }
.pdf-slide .founder-metrics { grid-template-columns: 1fr 1fr !important; }
.pdf-slide .guarantees-grid { grid-template-columns: repeat(4, minmax(0, 1fr)) !important; }
.pdf-slide .pioneer-grid { grid-template-columns: repeat(3, minmax(0, 1fr)) !important; }
.pdf-slide .closing-card { grid-template-columns: 1.18fr 1fr !important; }
.pdf-slide .pkg-grid { grid-template-columns: 1fr 1fr !important; }
.pdf-slide .res-kpi-grid { grid-template-columns: 1fr 1fr !important; }

/* Slide 1 cover: omit duplicate small logo in running header */
.pdf-slide[data-pdf-slide="1"] .pdf-header-brand img,
.pdf-slide[data-pdf-slide="1"] .pdf-header-sep {
  display: none;
}

/* Fix inline strong inside paradox-lens so only the title label is block */
.pdf-slide .paradox-lens strong {
  display: inline;
  font-size: inherit;
  letter-spacing: normal;
  text-transform: none;
  margin-bottom: 0;
  color: #FFFFFF;
}
.pdf-slide .paradox-lens > strong:first-child {
  display: block;
  font-size: 0.72rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 4px;
  color: #D4C914;
}

/* Typography tightening for 1440x900 slides */
.pdf-slide .act-title {
  font-size: 2.25rem;
  line-height: 1.12;
  margin: 0 0 10px;
}

.pdf-slide--navy .act-title { color: #FFFFFF; }
.pdf-slide--paper .act-title,
.pdf-slide--surface .act-title { color: #052962; }

.pdf-slide .section-rule {
  width: 58px;
  height: 3px;
  margin: 0 0 14px;
}
.pdf-slide--navy .section-rule { background: #B9AF07; }
.pdf-slide--paper .section-rule,
.pdf-slide--surface .section-rule { background: #AA5959; }

.pdf-slide .act-lead {
  font-size: 1.04rem;
  line-height: 1.5;
  margin: 0 0 20px;
  max-width: 88ch;
}
.pdf-slide--navy .act-lead { color: #D5E2F2; }
.pdf-slide--paper .act-lead,
.pdf-slide--surface .act-lead { color: #2E3C46; }

/* Slide 1: Hero */
.pdf-s1-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 22px;
}
.pdf-s1-top img {
  height: 70px;
  width: auto;
}
.pdf-s1-h1 {
  font-family: var(--ff-display);
  font-weight: 800;
  font-size: 3.1rem;
  line-height: 1.1;
  color: #FFFFFF;
  margin: 0 0 18px;
  max-width: 26ch;
}
.pdf-s1-h1 .hl { color: #D4C914; }
.pdf-dual-strip {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 26px;
}
.pdf-dual-card {
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-left: 4px solid #B9AF07;
  border-radius: 10px;
  padding: 15px 18px;
}
.pdf-dual-card--inv {
  border-left-color: #5AA0D6;
}
.pdf-dual-card .tag {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #D4C914;
  margin-bottom: 5px;
}
.pdf-dual-card--inv .tag { color: #8AC4F2; }
.pdf-dual-card p {
  margin: 0;
  font-family: var(--ff-serif);
  font-size: 0.96rem;
  line-height: 1.48;
  color: #E3EDF8;
}
.pdf-dual-card strong { color: #FFFFFF; }

/* Slide 2: Market */
.pdf-slide[data-pdf-slide="2"] .act-title { font-size: 2rem; margin-bottom: 6px; }
.pdf-slide[data-pdf-slide="2"] .section-rule { margin-bottom: 8px; }
.pdf-slide[data-pdf-slide="2"] .act-lead { font-size: 0.94rem; margin-bottom: 10px; }
.pdf-slide .stat-grid-4 {
  gap: 12px;
  margin-bottom: 10px;
}
.pdf-slide .editorial-card {
  padding: 10px 14px;
}
.pdf-slide .stat-big {
  font-size: 1.88rem;
  margin-bottom: 4px;
}
.pdf-slide .editorial-card h3 { font-size: 0.9rem; margin-bottom: 3px; }
.pdf-slide .editorial-card p { font-size: 0.8rem; line-height: 1.4; }
.pdf-slide .chart-panel { padding: 16px 20px; }
.pdf-slide .chart-panel-head { margin-bottom: 11px; padding-bottom: 8px; }
.pdf-slide .bar-row { margin-bottom: 9px; }
.pdf-slide .bar-sub { font-size: 0.74rem; margin-top: 2px; }
.pdf-slide .paradox-card { padding: 16px 20px; }
.pdf-slide .paradox-card h3 { font-size: 1.22rem; margin-bottom: 8px; }
.pdf-slide .paradox-card p { font-size: 0.83rem; margin-bottom: 10px; line-height: 1.46; }
.pdf-paradox-lenses {
  display: grid;
  gap: 8px;
}
.pdf-slide .paradox-lens {
  display: block !important;
  padding: 9px 12px;
  font-size: 0.79rem;
  line-height: 1.38;
}
.pdf-slide .source-footnote {
  margin-top: 10px;
  padding-top: 7px;
  font-size: 0.71rem;
}

/* Slide 3: Before vs After side-by-side comparison */
.pdf-cmp-banner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 18px;
}
.pdf-cmp-pill {
  border-radius: 10px;
  padding: 12px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.pdf-cmp-pill--before {
  background: #FFF6F6;
  border: 1.5px solid #E5B9B9;
  color: #AA5959;
}
.pdf-cmp-pill--after {
  background: #052962;
  border: 1.5px solid #052962;
  color: #FFFFFF;
}
.pdf-cmp-pill strong {
  font-size: 0.92rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.pdf-cmp-score {
  font-family: var(--ff-display);
  font-size: 1.3rem;
  font-weight: 800;
}
.pdf-cmp-pill--after .pdf-cmp-score { color: #D4C914; }

.pdf-pillars-5 {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 16px;
}
.pdf-pcard {
  background: #FFFFFF;
  border: 1px solid #DEE2E6;
  border-top: 4px solid #052962;
  border-radius: 12px;
  padding: 15px 14px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 8px 22px rgba(2, 19, 47, 0.06);
}
.pdf-pcard-num {
  font-size: 0.66rem;
  font-weight: 800;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #346E9B;
  margin-bottom: 5px;
}
.pdf-pcard h3 {
  font-family: var(--ff-display);
  font-size: 1.02rem;
  line-height: 1.22;
  color: #02132F;
  margin: 0 0 10px;
}
.pdf-pcard-before {
  background: #FFF7F7;
  border-left: 3px solid #AA5959;
  border-radius: 0 6px 6px 0;
  padding: 8px 9px;
  margin-bottom: 10px;
}
.pdf-pcard-before span {
  display: block;
  font-size: 0.64rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #AA5959;
  margin-bottom: 2px;
}
.pdf-pcard-before p {
  margin: 0;
  font-size: 0.76rem;
  line-height: 1.38;
  color: #5C4444;
}
.pdf-pcard-after {
  background: #F4F8FC;
  border-left: 3px solid #052962;
  border-radius: 0 6px 6px 0;
  padding: 9px 10px;
  margin-bottom: 10px;
  flex: 1;
}
.pdf-pcard-after span {
  display: block;
  font-size: 0.64rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #052962;
  margin-bottom: 3px;
}
.pdf-pcard-after p {
  margin: 0;
  font-size: 0.79rem;
  line-height: 1.42;
  color: #02132F;
}
.pdf-pcard-metric {
  padding-top: 8px;
  border-top: 1px solid #DEE2E6;
  font-size: 0.76rem;
  font-weight: 800;
  color: #052962;
}
.pdf-cmp-footer {
  background: #052962;
  color: #FFFFFF;
  border-radius: 10px;
  padding: 13px 20px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  font-size: 0.82rem;
  line-height: 1.45;
}
.pdf-cmp-footer strong { color: #D4C914; }

/* Slide 4: Acto 4A — Portada Desktop + 4 Hotspot Cards */
.pdf-s4-grid {
  display: grid;
  grid-template-columns: 1.45fr 1fr;
  gap: 22px;
  align-items: center;
}
.pdf-hs-legend {
  display: grid;
  gap: 10px;
}
.pdf-hs-card {
  background: #F7F7F7;
  border: 1px solid #DEE2E6;
  border-left: 4px solid #052962;
  border-radius: 8px;
  padding: 11px 14px;
}
.pdf-hs-card--accent {
  border-left-color: #AA5959;
  background: #FFFDFD;
}
.pdf-hs-card-head {
  display: flex;
  align-items: center;
  gap: 9px;
  margin-bottom: 4px;
}
.pdf-hs-num {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #AA5959;
  color: #FFFFFF;
  font-size: 0.72rem;
  font-weight: 800;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.pdf-hs-card--gold .pdf-hs-num {
  background: #B9AF07;
  color: #02132F;
}
.pdf-hs-card-head strong {
  font-family: var(--ff-display);
  font-size: 0.98rem;
  color: #052962;
}
.pdf-hs-card p {
  margin: 0 0 4px;
  font-size: 0.79rem;
  color: #2E3C46;
  line-height: 1.4;
}
.pdf-hs-card small {
  display: block;
  font-size: 0.72rem;
  font-weight: 700;
  color: #346E9B;
}

/* Slide 5: Acto 4B — Article (Café Águila Roja) + Mobile 390px */
.pdf-s5-grid {
  display: grid;
  grid-template-columns: 1.38fr 0.92fr;
  gap: 24px;
  align-items: stretch;
}
.pdf-s5-col {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.pdf-article-crop {
  height: 455px;
  overflow: hidden;
  position: relative;
  background: #FFFFFF;
}
.pdf-article-crop img {
  width: 100%;
  height: auto;
  display: block;
}
.pdf-mobile-stage {
  background: linear-gradient(145deg, #EEF2F6 0%, #DCE5F0 100%);
  border: 2px solid #052962;
  border-radius: 12px;
  padding: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 493px;
}
.pdf-phone-bezel {
  width: 240px;
  background: #0B1424;
  border-radius: 28px;
  padding: 9px;
  box-shadow: 0 18px 36px rgba(2, 19, 47, 0.25);
  border: 2px solid #243857;
}
.pdf-phone-screen {
  border-radius: 20px;
  overflow: hidden;
  height: 444px;
  position: relative;
  background: #FFFFFF;
}
.pdf-phone-screen img {
  width: 100%;
  height: auto;
}
.pdf-mini-notes {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}
.pdf-mini-note {
  background: #F7F7F7;
  border: 1px solid #DEE2E6;
  border-top: 3px solid #052962;
  border-radius: 7px;
  padding: 9px 10px;
}
.pdf-mini-note strong {
  display: block;
  font-size: 0.74rem;
  color: #052962;
  margin-bottom: 3px;
}
.pdf-mini-note span {
  display: block;
  font-size: 0.71rem;
  color: #2E3C46;
  line-height: 1.35;
}

/* Slide 6: Acto 4C — TRM Spotlight + Authority Strip */
.pdf-slide .trm-spotlight {
  padding: 24px 28px;
  margin-bottom: 18px;
}
.pdf-slide .trm-head { margin-bottom: 14px; }
.pdf-slide .trm-head h3 { font-size: 1.78rem; }
.pdf-slide .trm-benefits-row { margin-top: 14px; gap: 14px; }
.pdf-slide .trm-ben { padding: 12px 14px; }
.pdf-slide .trm-ben strong { font-size: 0.84rem; }
.pdf-slide .trm-ben p { font-size: 0.79rem; line-height: 1.42; }
.pdf-slide .trm-ben p strong { display: inline; color: #FFFFFF; font-size: inherit; margin-bottom: 0; }
.pdf-slide .authority-strip { gap: 16px; }
.pdf-slide .auth-card { padding: 15px 18px; gap: 5px; }
.pdf-slide .auth-card strong { font-size: 1rem; }
.pdf-slide .auth-card p { font-size: 0.81rem; line-height: 1.44; }

/* Slide 7: Acto 5A — Social Grid + Founder Spotlight */
.pdf-slide .social-grid {
  gap: 12px;
  margin-bottom: 18px;
}
.pdf-slide .social-card {
  padding: 14px 14px;
  gap: 6px;
}
.pdf-slide .social-card p {
  font-size: 0.77rem;
  line-height: 1.4;
}
.pdf-slide .founder-spotlight {
  padding: 18px 22px;
  margin-bottom: 0;
}
.pdf-slide .founder-spotlight h3 { font-size: 1.28rem; }
.pdf-slide .founder-spotlight p { font-size: 0.86rem; line-height: 1.48; }

/* Slide 8: Acto 5B — 4 Guarantees + 3 Simultaneous Roadmap Phases */
.pdf-slide .guarantees-grid {
  gap: 14px;
  margin-bottom: 22px;
}
.pdf-slide .guarantee-card {
  padding: 16px 16px;
}
.pdf-slide .guarantee-card strong { font-size: 0.92rem; }
.pdf-slide .guarantee-card p { font-size: 0.82rem; line-height: 1.46; }

.pdf-road-3col {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}
.pdf-phase-card {
  background: rgba(2, 19, 47, 0.56);
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-top: 4px solid #B9AF07;
  border-radius: 12px;
  padding: 18px 18px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.pdf-phase-card--2 { border-top-color: #5AA0D6; }
.pdf-phase-card--3 { border-top-color: #AA5959; }
.pdf-phase-tag {
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #D4C914;
  margin-bottom: 4px;
}
.pdf-phase-card--2 .pdf-phase-tag { color: #8AC4F2; }
.pdf-phase-card--3 .pdf-phase-tag { color: #F0A3A3; }
.pdf-phase-card h3 {
  font-family: var(--ff-display);
  font-size: 1.15rem;
  color: #FFFFFF;
  margin: 0 0 10px;
}
.pdf-phase-card ul {
  margin: 0 0 14px;
  padding-left: 16px;
  font-size: 0.81rem;
  line-height: 1.45;
  color: #D5E2F2;
  display: grid;
  gap: 6px;
}
.pdf-phase-deliv {
  background: rgba(52, 110, 155, 0.24);
  border: 1px solid rgba(185, 175, 7, 0.36);
  border-radius: 8px;
  padding: 10px 12px;
}
.pdf-phase-deliv span {
  display: block;
  font-size: 0.65rem;
  font-weight: 800;
  letter-spacing: 0.11em;
  text-transform: uppercase;
  color: #D4C914;
  margin-bottom: 3px;
}
.pdf-phase-deliv p {
  margin: 0;
  font-size: 0.78rem;
  line-height: 1.4;
  color: #FFFFFF;
}

/* Slides 9 & 10: Simulators (Marca & Inversionista) */
.pdf-slide .sim-grid {
  display: grid !important;
  grid-template-columns: 1.05fr 1fr;
  gap: 20px;
  align-items: stretch;
}
.pdf-slide .sim-controls-card,
.pdf-slide .sim-results-card {
  padding: 17px 20px;
}
.pdf-slide .sim-controls-card h3,
.pdf-slide .sim-results-card h3 {
  font-size: 1.16rem;
  margin-bottom: 11px;
}
.pdf-slide .pkg-grid {
  margin-bottom: 12px;
  gap: 8px;
}
.pdf-slide .pkg-opt { padding: 9px 11px; }
.pdf-slide .pkg-opt span { font-size: 0.74rem; }
.pdf-slide .scenario-pills { margin-bottom: 12px; }
.pdf-slide .scen-btn { padding: 8px 8px; }
.pdf-slide .slider-group { margin-bottom: 11px; }
.pdf-slide .slider-head { margin-bottom: 4px; }
.pdf-slide .res-kpi-grid { gap: 9px; margin-bottom: 11px; }
.pdf-slide .res-kpi { padding: 10px 12px; }
.pdf-slide .res-kpi strong { font-size: 1.24rem; }
.pdf-slide .sim-visual-box { padding: 11px 14px; margin-bottom: 10px; }
.pdf-slide .sim-visual-box h4 { margin-bottom: 8px; }
.pdf-slide .alloc-row { margin-bottom: 7px; }
.pdf-slide .deliverables-list { margin-bottom: 0; gap: 6px; }
.pdf-slide .sim-disclaimer {
  margin-top: 10px;
  padding: 9px 13px;
  font-size: 0.72rem;
}
.pdf-slide .sim-hide-btn { display: none !important; }

/* Slide 11: Acto 7 — Closing */
.pdf-slide[data-pdf-slide="11"] .act-title {
  font-size: 1.96rem;
  max-width: 38ch;
  margin-bottom: 8px;
}
.pdf-slide[data-pdf-slide="11"] .section-rule {
  margin-bottom: 10px;
}
.pdf-slide[data-pdf-slide="11"] .act-lead {
  font-size: 0.96rem;
  margin-bottom: 14px;
}
.pdf-slide .pioneer-grid {
  gap: 14px;
  margin-bottom: 15px;
}
.pdf-slide .pioneer-card {
  padding: 15px 18px;
}
.pdf-slide .pioneer-quota { margin-bottom: 7px; }
.pdf-slide .pioneer-card h3 { font-size: 1.1rem; margin-bottom: 5px; }
.pdf-slide .pioneer-card p { font-size: 0.81rem; line-height: 1.42; }
.pdf-slide .closing-card {
  padding: 18px 24px;
  gap: 20px;
}
.pdf-slide .closing-brand-row { margin-bottom: 8px; }
.pdf-slide .closing-brand-row img { height: 34px; }
.pdf-slide .closing-ceo-name { font-size: 1.52rem; }
.pdf-slide .closing-ceo-role { margin-bottom: 8px; font-size: 0.9rem; }
.pdf-slide .closing-quote { font-size: 0.9rem; margin-bottom: 10px; }
.pdf-slide .contact-meta { gap: 4px; font-size: 0.82rem; }
.pdf-slide .closing-actions {
  padding: 15px 18px;
  gap: 8px;
}
.pdf-next-step-list {
  display: grid;
  gap: 8px;
}
.pdf-next-step {
  background: #FFFFFF;
  border: 1px solid #DEE2E6;
  border-left: 4px solid #052962;
  border-radius: 8px;
  padding: 9px 12px;
}
.pdf-next-step--gold { border-left-color: #B9AF07; }
.pdf-next-step--terra { border-left-color: #AA5959; }
.pdf-next-step > strong {
  display: block;
  font-size: 0.82rem;
  color: #052962;
  margin-bottom: 2px;
}
.pdf-next-step span strong {
  display: inline;
  color: #052962;
  font-weight: 700;
}
.pdf-next-step span {
  display: block;
  font-size: 0.76rem;
  color: #2E3C46;
  line-height: 1.38;
}
"""


COMPOSE_JS = r"""
() => {
  // Capture assets already embedded in the original HTML
  const logoWhite = document.querySelector('#act-1 .hero-logo-badge img').src;
  const logoNavy = document.querySelector('#act-7 .closing-brand-row img').src;
  const imagoWhite = document.querySelector('#act-1 .hero-watermark').src;
  const imagoNavy = document.querySelector('#act-6 .sim-watermark').src;
  const capDesktop = document.querySelector('#pane-desktop img').src;
  const capArticle = document.querySelector('#pane-article img').src;
  const capMobile = document.querySelector('#pane-mobile img').src;
  const capTrm = document.querySelector('.trm-live-mockup img').src;

  // Ensure exact final KPI numbers & market bars before cloning
  document.querySelectorAll('.count-up').forEach(el => {
    const t = parseFloat(el.getAttribute('data-target'));
    const fmt = el.getAttribute('data-format');
    el.textContent = fmt === 'dec2' ? t.toFixed(2).replace('.', ',') : Math.round(t).toLocaleString('es-CO');
  });
  document.querySelectorAll('#market-chart .bar-fill').forEach(bar => {
    bar.style.width = bar.getAttribute('data-w') || '50%';
  });

  // Trigger recommended calculator states for Marca & Inversionista
  const simMarcaClone = document.getElementById('sim-marca-wrap').cloneNode(true);
  simMarcaClone.classList.remove('only-marca');
  simMarcaClone.querySelectorAll('button').forEach(b => b.classList.add('sim-hide-btn'));

  // Switch briefly to Base scenario for Inversionista (already default 120M / 12m) and clone
  const simInvClone = document.getElementById('sim-inversor-wrap').cloneNode(true);
  simInvClone.classList.remove('only-inversor');
  simInvClone.querySelectorAll('#btn-copy-sim-inversor').forEach(b => b.classList.add('sim-hide-btn'));

  const totalSlides = 11;

  function makeSlide(num, theme, actTag, headerRight, bodyHtml, extraBgHtml = '') {
    const isDark = theme === 'navy';
    const logo = isDark ? logoWhite : logoNavy;
    const pageStr = String(num).padStart(2, '0') + ' / ' + String(totalSlides).padStart(2, '0');
    return `
      <section class="pdf-slide pdf-slide--${theme}" data-pdf-slide="${num}">
        ${extraBgHtml}
        <header class="pdf-header">
          <div class="pdf-header-brand">
            <img src="${logo}" alt="Somos La Lupa News">
            <span class="pdf-header-sep"></span>
            <span class="pdf-header-act">${actTag}</span>
          </div>
          <div class="pdf-header-right">${headerRight}</div>
        </header>
        <div class="pdf-body">${bodyHtml}</div>
        <footer class="pdf-footer">
          <span>Somos La Lupa News · somoslalupanews.com · Bogotá, Colombia</span>
          <span class="pdf-page-num">${pageStr}</span>
        </footer>
      </section>
    `;
  }

  // Extract reusable fragments directly from the live DOM
  const heroKpisHtml = document.querySelector('#act-1 .hero-kpis').outerHTML;
  const statGrid4Html = document.querySelector('#act-2 .stat-grid-4').outerHTML;
  const marketChartHtml = document.querySelector('#act-2 #market-chart').outerHTML;
  const trmMockupImg = capTrm;
  const authStripHtml = document.querySelector('#act-4 .authority-strip').outerHTML;
  const socialGridHtml = document.querySelector('#act-5 .social-grid').outerHTML;
  const founderHtml = document.querySelector('#act-5 .founder-spotlight').outerHTML;
  const guaranteesHtml = document.querySelector('#act-5 .guarantees-grid').outerHTML;
  const simDisclaimerHtml = document.querySelector('#act-6 .sim-disclaimer').outerHTML;
  const pioneerGridHtml = document.querySelector('#act-7 .pioneer-grid').outerHTML;

  // SLIDE 01 — ACTO 1: PORTADA HERO
  const s1Bg = `
    <div class="hero-grid-bg" aria-hidden="true"></div>
    <div class="hero-glow" aria-hidden="true"></div>
    <img src="${imagoWhite}" alt="" class="hero-watermark" style="width:270px;right:24px;bottom:24px;opacity:0.055;" aria-hidden="true">
  `;
  const s1Body = `
    <div class="pdf-s1-top">
      <img src="${logoWhite}" alt="Somos La Lupa News">
      <div class="live-pill">
        <span class="live-dot"></span>
        Portal Operativo · TRM Viva Hoy ($3,327 COP)
      </div>
    </div>
    <h1 class="pdf-s1-h1">
      El 59% de la pauta en Colombia ya es digital, pero <span class="hl">3 de cada 4 lectores</span> desconfían de las redes. Tu marca merece un medio propio, creíble y medible.
    </h1>
    <div class="pdf-dual-strip">
      <div class="pdf-dual-card">
        <span class="tag">Frente Comercial · Marcas y Anunciantes</span>
        <p><strong>Somos La Lupa News</strong> reactiva su ecosistema informativo con formatos editoriales de alto recuerdo, el <strong>patrocinio exclusivo del indicador diario TRM</strong> y reportes transparentes de resultados reales.</p>
      </div>
      <div class="pdf-dual-card pdf-dual-card--inv">
        <span class="tag">Frente de Capital · Inversionistas y Aliados</span>
        <p>Un <strong>activo mediático colombiano ya construido</strong> —con <strong>4.583 historias publicadas</strong>, marcas reales validadas y liderazgo nacional— listo para acelerar audiencia y monetización directa de alto margen.</p>
      </div>
    </div>
    ${heroKpisHtml}
  `;

  // SLIDE 02 — ACTO 2: PULSO DEL MERCADO COLOMBIA 2025-2026
  const s2Body = `
    <h2 class="act-title">Una audiencia móvil masiva buscando información en la que pueda confiar</h2>
    <div class="section-rule"></div>
    <p class="act-lead">
      Los presupuestos publicitarios en Colombia ya son mayoritariamente digitales y los formatos editoriales viven su mayor aceleración histórica, mientras la caída de confianza en redes abre una ventana extraordinaria para medios propios curados.
    </p>
    ${statGrid4Html}
    <div class="market-split">
      ${marketChartHtml}
      <aside class="paradox-card">
        <div>
          <span class="paradox-badge">LA PARADOJA DE LA CONFIANZA 2026</span>
          <h3>Más presupuesto digital que nunca, pero menos lugares seguros para tu reputación</h3>
          <p>Mientras el 72% descubre temas en redes, 3 de cada 4 lectores desconfían de lo que circula sin curaduría. Las marcas serias migran hacia <strong>portales periodísticos propios</strong> donde su mensaje gana credibilidad.</p>
        </div>
        <div class="pdf-paradox-lenses">
          <div class="paradox-lens">
            <strong>Para Marcas y Anunciantes</strong>
            Entorno seguro que eleva <strong>+9% la afinidad de marca</strong> y multiplica la atención frente a feeds saturados.
          </div>
          <div class="paradox-lens" style="border-left-color:#5AA0D6;">
            <strong style="color:#8AC4F2;">Para Inversionistas</strong>
            La demanda se desplaza hacia los productos de mayor margen de un portal propio: <strong>Branded Content (+90,5%)</strong> y <strong>Display Editorial (+34,4%)</strong>.
          </div>
        </div>
      </aside>
    </div>
    <div class="source-footnote">
      Fuentes verificadas: IAB Colombia (Reporte Anual 2025 y Q1–Q2 2026) · Reuters Institute for the Study of Journalism, Universidad de Oxford (Digital News Report Colombia 2025–2026) · DataReportal &amp; MinTIC Colombia (2026).
    </div>
  `;

  // SLIDE 03 — ACTO 3: SOLO REDES VS PORTAL PROPIO ACTIVADO
  const pillarsData = [
    {
      num: 'Pilar 01',
      title: 'Propiedad de la Audiencia',
      before: 'Terreno alquilado: si el algoritmo cambia, tu visibilidad cae de inmediato.',
      after: 'Audiencia propia en somoslalupanews.com con Google Discover (67,5% tráfico móvil) + WhatsApp y Boletín.',
      metric: 'Activo propio blindado'
    },
    {
      num: 'Pilar 02',
      title: 'Seguridad de Marca',
      before: 'Tu anuncio convive con ruido, polarización o contenido sin verificar (25% confianza).',
      after: 'Entorno editorial limpio y curado por periodistas que transfiere confianza institucional.',
      metric: '+9% afinidad de marca'
    },
    {
      num: 'Pilar 03',
      title: 'Atención y Recordación',
      before: 'Publicaciones efímeras omitidas en 1 segundo (CTR estándar 0,05%–0,10%).',
      after: 'Formatos nativos, patrocinios de sección y notas patrocinadas con lectura profunda real.',
      metric: '+53% atención · hasta 86% recuerdo'
    },
    {
      num: 'Pilar 04',
      title: 'Hábito Diario (TRM)',
      before: 'Sin utilidad cotidiana propia: cada impacto obliga a pagar de nuevo por interrumpir.',
      after: 'Indicador diario del dólar consultado cada mañana por empresarios, viajeros e importadores.',
      metric: '100% exclusividad diaria'
    },
    {
      num: 'Pilar 05',
      title: 'Medición Transparente',
      before: 'Métricas superficiales difíciles de conectar con decisiones reales de negocio.',
      after: 'Trazabilidad exacta por espacio, reimpacto inteligente a lectores y reporte ejecutivo mensual.',
      metric: 'Cero "pauta a ciegas"'
    }
  ];
  const s3Cards = pillarsData.map(p => `
    <article class="pdf-pcard">
      <div>
        <div class="pdf-pcard-num">${p.num}</div>
        <h3>${p.title}</h3>
        <div class="pdf-pcard-before">
          <span>✕ Solo Redes Sociales</span>
          <p>${p.before}</p>
        </div>
        <div class="pdf-pcard-after">
          <span>✓ Portal Propio Activado</span>
          <p>${p.after}</p>
        </div>
      </div>
      <div class="pdf-pcard-metric">${p.metric}</div>
    </article>
  `).join('');

  const s3Body = `
    <h2 class="act-title">Las redes despiertan curiosidad; un portal propio construye autoridad, patrimonio y ventas</h2>
    <div class="section-rule"></div>
    <p class="act-lead">
      Contraste directo entre pautar en terreno alquilado frente a activar un ecosistema editorial propio conectado con buscadores, comunidad directa y trazabilidad verificable.
    </p>
    <div class="pdf-cmp-banner">
      <div class="pdf-cmp-pill pdf-cmp-pill--before">
        <strong>Antes · Pauta Tradicional Solo en Redes</strong>
        <span class="pdf-cmp-score">32 / 100</span>
      </div>
      <div class="pdf-cmp-pill pdf-cmp-pill--after">
        <strong>Después · Ecosistema Activado Somos La Lupa News</strong>
        <span class="pdf-cmp-score">94 / 100</span>
      </div>
    </div>
    <div class="pdf-pillars-5">${s3Cards}</div>
    <div class="pdf-cmp-footer">
      <div><strong>Para Marcas:</strong> Las redes sociales se convierten en autopistas de amplificación que traen lectores calificados hacia tu marca viviendo en <em>somoslalupanews.com</em>.</div>
      <div><strong>Para Inversionistas:</strong> Audiencia propia + venta directa construyen un activo transferible valorado en múltiplos de <strong>6x a 12x+ EBITDA</strong> en medios digitales consolidados.</div>
    </div>
  `;

  // SLIDE 04 — ACTO 4A: VITRINA VIVA PORTADA ESCRITORIO
  const s4Body = `
    <h2 class="act-title">Vitrina Viva: Portada Escritorio &amp; Zonas Comerciales Reales</h2>
    <div class="section-rule"></div>
    <p class="act-lead">
      Captura real de <strong>somoslalupanews.com</strong> en escritorio verificada en producción: cada espacio estratégico está listo para conectar tu marca desde el primer pantallazo.
    </p>
    <div class="pdf-s4-grid">
      <div class="browser-frame">
        <div class="browser-chrome">
          <div class="browser-dots"><i></i><i></i><i></i></div>
          <div class="browser-url">https://somoslalupanews.com/  ·  Vista Escritorio Real</div>
          <div class="browser-hint">4 Zonas Destacadas</div>
        </div>
        <div class="capture-canvas">
          <img src="${capDesktop}" alt="Captura real portada escritorio somoslalupanews.com">
          <span class="hs-pin" style="left:46%;top:16%;">1</span>
          <span class="hs-pin active" style="left:16%;top:32%;">2</span>
          <span class="hs-pin" style="left:55%;top:44%;">3</span>
          <span class="hs-pin" style="left:75%;top:64%;">4</span>
        </div>
      </div>

      <div class="pdf-hs-legend">
        <div class="pdf-hs-card">
          <div class="pdf-hs-card-head">
            <span class="pdf-hs-num">1</span>
            <strong>Cabecera Editorial &amp; 20 Verticales</strong>
          </div>
          <p>Arquitectura sobria de prensa digital (Colombia, Política, Deportes, Mundo, Historias, Música, Opinión y En Vivo) que transfiere autoridad editorial inmediata.</p>
          <small>Visibilidad: 100% primer pantallazo · Archivo real de 4.583 notas</small>
        </div>

        <div class="pdf-hs-card pdf-hs-card--accent pdf-hs-card--gold">
          <div class="pdf-hs-card-head">
            <span class="pdf-hs-num">2</span>
            <strong>Patrocinio Exclusivo Widget TRM Diario</strong>
          </div>
          <p>Utilidad financiera en vivo ($3,327 COP al 19 nov 2026) que crea hábito de visita diaria entre empresarios, viajeros e importadores. 100% exclusividad de categoría.</p>
          <small>Ideal: Bancos, Fintechs, Remesadoras, Aerolíneas y Comercio Exterior</small>
        </div>

        <div class="pdf-hs-card">
          <div class="pdf-hs-card-head">
            <span class="pdf-hs-num">3</span>
            <strong>Mega Leaderboard Premium Superior</strong>
          </div>
          <p>Franja panorámica above-the-fold validada comercialmente con <strong>Súper Astro</strong>. Máxima recordación visual sin necesidad de hacer scroll.</p>
          <small>Ideal: Consumo masivo, entretenimiento, lanzamientos y retail</small>
        </div>

        <div class="pdf-hs-card">
          <div class="pdf-hs-card-head">
            <span class="pdf-hs-num">4</span>
            <strong>Portada Principal &amp; Columna Destacadas</strong>
          </div>
          <p>Integración nativa dentro del flujo editorial con <strong>3x–10x más clics</strong> que un banner común, <strong>+53% atención visual</strong> y <strong>+20,6% brand lift</strong>.</p>
          <small>Ideal: Servicios, educación, tecnología y marcas con historia</small>
        </div>
      </div>
    </div>
  `;

  // SLIDE 05 — ACTO 4B: ARTÍCULO REAL CAFÉ ÁGUILA ROJA + EXPERIENCIA MÓVIL
  const s5Body = `
    <h2 class="act-title">Patrocinio Editorial Probado (Café Águila Roja) &amp; Experiencia Móvil</h2>
    <div class="section-rule"></div>
    <div class="pdf-s5-grid">
      <div class="pdf-s5-col">
        <div class="browser-frame">
          <div class="browser-chrome">
            <div class="browser-dots"><i></i><i></i><i></i></div>
            <div class="browser-url">somoslalupanews.com/deportes/seleccion-colombia-mundial-2026/</div>
            <div class="browser-hint">Caso Real Activo</div>
          </div>
          <div class="pdf-article-crop">
            <img src="${capArticle}" alt="Captura real artículo Deportes patrocinado por Café Águila Roja">
            <span class="hs-pin active" style="left:18%;top:37%;">4</span>
            <span class="hs-pin" style="left:33%;top:58%;">5</span>
            <span class="hs-pin" style="left:79%;top:72%;">6</span>
          </div>
        </div>
        <div class="pdf-mini-notes">
          <div class="pdf-mini-note">
            <strong>4 · Sello de Sección</strong>
            <span>«Patrocinado por Café Águila Roja» visible en todos los artículos de Deportes.</span>
          </div>
          <div class="pdf-mini-note">
            <strong>5 · Branded Content</strong>
            <span>Formato +90,5% en CO: hasta 86% recuerdo y +15%–18% intención de compra.</span>
          </div>
          <div class="pdf-mini-note">
            <strong>6 · Lectura &amp; Sidebar</strong>
            <span>Espacios mid-article y columna Tendencias en el punto de mayor atención.</span>
          </div>
        </div>
      </div>

      <div class="pdf-s5-col">
        <div class="pdf-mobile-stage">
          <div class="pdf-phone-bezel">
            <div class="phone-notch"></div>
            <div class="pdf-phone-screen">
              <img src="${capMobile}" alt="Captura real móvil 390px somoslalupanews.com">
              <span class="hs-pin active" style="left:14%;top:27%;width:26px;height:26px;font-size:0.64rem;">7A</span>
              <span class="hs-pin" style="left:50%;top:40%;width:26px;height:26px;font-size:0.64rem;">7B</span>
              <span class="hs-pin" style="left:50%;top:66%;width:26px;height:26px;font-size:0.64rem;">7C</span>
            </div>
          </div>
        </div>
        <div class="pdf-mini-notes">
          <div class="pdf-mini-note" style="border-top-color:#AA5959;">
            <strong>7A · TRM Móvil</strong>
            <span>3 columnas nítidas en el primer pantallazo celular (75% lectores CO).</span>
          </div>
          <div class="pdf-mini-note" style="border-top-color:#346E9B;">
            <strong>7B · Banner Móvil</strong>
            <span>Impacto inmediato sin tapar el titular ni ventanas invasivas.</span>
          </div>
          <div class="pdf-mini-note" style="border-top-color:#B9AF07;">
            <strong>7C · Lectura Limpia</strong>
            <span>Optimizada para tráfico desde WhatsApp, Reels y Google Discover.</span>
          </div>
        </div>
      </div>
    </div>
  `;

  // SLIDE 06 — ACTO 4C: LA JOYA ESTELAR WIDGET TRM + PRUEBA COMERCIAL
  const s6Body = `
    <div class="trm-spotlight">
      <div class="trm-head">
        <div>
          <span class="eyebrow" style="margin-bottom:4px;">LA JOYA COMERCIAL DEL PORTAL · 1 ÚNICO CUPO EXCLUSIVO</span>
          <h3>Patrocinio Exclusivo del Indicador Diario TRM</h3>
        </div>
        <span class="trm-badge-excl">100% Share of Voice · Cero Competidores</span>
      </div>
      <div class="trm-live-mockup">
        <div class="trm-cobrand-strip">
          <div class="trm-cobrand-left">
            <span class="trm-cobrand-pill">PATROCINIO EXCLUSIVO</span>
            <span class="trm-cobrand-text">TRM del día presentada por <strong>[Tu Marca / Banco / Fintech]</strong></span>
          </div>
          <span class="trm-cobrand-cta">Cotiza dólar hoy →</span>
        </div>
        <img src="${trmMockupImg}" alt="Captura real del Widget TRM de somoslalupanews.com mostrando TRM HOY $3,327 COP">
      </div>
      <div class="trm-benefits-row">
        <div class="trm-ben">
          <strong>Hábito de Consulta Diaria</strong>
          <p>Consultar el dólar es una rutina matutina de empresarios, importadores, viajeros y decisores financieros: visitas repetidas todos los días.</p>
        </div>
        <div class="trm-ben">
          <strong>Cero Ceguera de Banner</strong>
          <p>En el primer pantallazo en escritorio y celular, el lector busca activamente la cifra del día y asocia esa utilidad directamente con tu marca.</p>
        </div>
        <div class="trm-ben">
          <strong>Verticales de Alta Disposición de Pago</strong>
          <p>Vitrina de élite para <strong>Bancos, Fintechs, Remesadoras, Casas de Cambio, Aerolíneas, Aseguradoras y Bienes Raíces</strong> con clics 100% trazables.</p>
        </div>
      </div>
    </div>
    ${authStripHtml}
  `;

  // SLIDE 07 — ACTO 5A: ECOSISTEMA SOCIAL MULTICANAL + FUNDADOR
  const s7Bg = `<img src="${imagoWhite}" alt="" class="hero-watermark" style="left:24px;right:auto;bottom:24px;width:240px;opacity:0.045;" aria-hidden="true">`;
  const s7Body = `
    <h2 class="act-title">Ecosistema Social Multicanal y Amplificación del Fundador</h2>
    <div class="section-rule"></div>
    <p class="act-lead">
      Red oficial ya creada y lista para escalar en sincronía con <strong>somoslalupanews.com</strong>, potenciada por dos nuevos canales de comunidad propia y el respaldo nacional de nuestro CEO.
    </p>
    ${socialGridHtml}
    ${founderHtml}
  `;

  // SLIDE 08 — ACTO 5B: ACTIVACIÓN INTELIGENTE Y HOJA DE RUTA 90 DÍAS
  const s8Bg = `<img src="${imagoWhite}" alt="" class="hero-watermark" style="right:24px;bottom:24px;width:240px;opacity:0.045;" aria-hidden="true">`;
  const s8Body = `
    <h2 class="act-title">Promesa Cero «Caja Negra» y Hoja de Ruta de Activación 90 Días</h2>
    <div class="section-rule"></div>
    <p class="act-lead">
      El portal es el hogar; nuestra campaña inteligente de crecimiento y medición transparente es el motor que atrae lectores calificados y demuestra retorno mes a mes.
    </p>
    ${guaranteesHtml}
    <div class="pdf-road-3col">
      <article class="pdf-phase-card">
        <div>
          <div class="pdf-phase-tag">Fase 1 · Días 1 a 30</div>
          <h3>Puesta a Punto y Despegue</h3>
          <ul>
            <li>Reactivación del ritmo editorial diario con foco en Colombia, Deportes, Economía y actualidad.</li>
            <li>Sincronización completa de las 6 redes sociales hacia <strong>somoslalupanews.com</strong>.</li>
            <li>Activación del tablero comercial de trazabilidad y lanzamiento junto a Javier Fernández Franco.</li>
          </ul>
        </div>
        <div class="pdf-phase-deliv">
          <span>Entregable visible</span>
          <p>Portal renovado, ecosistema social unificado y primer reporte base de audiencia verificada.</p>
        </div>
      </article>

      <article class="pdf-phase-card pdf-phase-card--2">
        <div>
          <div class="pdf-phase-tag">Fase 2 · Días 31 a 60</div>
          <h3>Tracción y Comunidad Propia</h3>
          <ul>
            <li>Despliegue de campaña inteligente de captación de lectores calificados en Colombia.</li>
            <li>Lanzamiento del <strong>Canal Oficial de WhatsApp</strong> y <strong>Boletín Ejecutivo Diario</strong>.</li>
            <li>Producción constante de video vertical (1 noticia = 6 formatos) y primeros patrocinios ancla.</li>
          </ul>
        </div>
        <div class="pdf-phase-deliv">
          <span>Entregable visible</span>
          <p>Crecimiento medible en visitas web, comunidad en WhatsApp y patrocinio TRM / secciones activo.</p>
        </div>
      </article>

      <article class="pdf-phase-card pdf-phase-card--3">
        <div>
          <div class="pdf-phase-tag">Fase 3 · Días 61 a 90</div>
          <h3>Escala y Monetización 360°</h3>
          <ul>
            <li>Activación de audiencias de reimpacto inteligente para elevar conversión de anunciantes.</li>
            <li>Comercialización de paquetes integrados 360° (Portal Web + Video + Redes + Comunidad).</li>
            <li>Optimización comercial de las verticales líderes (Deportes, Economía y Actualidad Nacional).</li>
          </ul>
        </div>
        <div class="pdf-phase-deliv">
          <span>Entregable visible</span>
          <p>Tablero ejecutivo de retorno por marca, renovaciones recurrentes y proyecciones validadas.</p>
        </div>
      </article>
    </div>
  `;

  // SLIDE 09 — ACTO 6A: PROPUESTA Y PROYECCIÓN PARA MARCAS Y ANUNCIANTES
  const s9Bg = `<img src="${imagoNavy}" alt="" class="sim-watermark" style="top:64px;right:36px;width:120px;opacity:0.05;" aria-hidden="true">`;
  const s9Body = `
    <h2 class="act-title">Propuesta Comercial de Referencia — Marcas y Anunciantes</h2>
    <div class="section-rule"></div>
    <p class="act-lead">
      Escenario recomendado de alto impacto combinando el <strong>Patrocinio Exclusivo TRM</strong> y <strong>Branded Content + Patrocinio de Sección</strong> durante 3 meses, con reporte ejecutivo mensual.
    </p>
    ${simMarcaClone.outerHTML}
    ${simDisclaimerHtml}
  `;

  // SLIDE 10 — ACTO 6B: TESIS Y PROYECCIÓN PARA INVERSIONISTAS
  const s10Bg = `<img src="${imagoNavy}" alt="" class="sim-watermark" style="top:64px;right:36px;width:120px;opacity:0.05;" aria-hidden="true">`;
  const s10Body = `
    <h2 class="act-title">Tesis de Escalamiento y Despliegue de Capital — Inversionistas</h2>
    <div class="section-rule"></div>
    <p class="act-lead">
      Escenario <strong>Base Recomendado ($120M COP · 12 meses)</strong> destinando el 100% del capital a tracción, distribución inteligente y cierre de contratos directos sobre una plataforma ya construida.
    </p>
    ${simInvClone.outerHTML}
    ${simDisclaimerHtml}
  `;

  // SLIDE 11 — ACTO 7: VENTANA DE PIONEROS Y CIERRE EJECUTIVO
  const s11Bg = `<img src="${imagoWhite}" alt="" class="hero-watermark" style="right:24px;bottom:24px;width:250px;opacity:0.05;" aria-hidden="true">`;
  const s11Body = `
    <h2 class="act-title">El mejor momento para entrar a un medio en despegue es antes de que todos quieran estar ahí</h2>
    <div class="section-rule"></div>
    <p class="act-lead">
      La etapa de relanzamiento abre una ventana única con inventario genuinamente limitado, condiciones preferenciales de primer ocupante y conversación directa con la Dirección General.
    </p>
    ${pioneerGridHtml}
    <div class="closing-card">
      <div>
        <div class="closing-brand-row">
          <img src="${logoNavy}" alt="Somos La Lupa News">
          <span class="ceo-badge">Dirección General · Contacto Directo</span>
        </div>
        <h3 class="closing-ceo-name">Javier Fernández Franco</h3>
        <div class="closing-ceo-role">CEO — Somos La Lupa News</div>
        <blockquote class="closing-quote">
          «Construimos un medio con rigor, cercanía y voz propia en Colombia. Hoy abrimos las puertas a las marcas y aliados visionarios que quieren crecer con nosotros desde el primer día de esta nueva etapa.»
        </blockquote>
        <div class="contact-meta">
          <div><strong>Portal Oficial:</strong> https://somoslalupanews.com</div>
          <div><strong>Sede:</strong> Calle 127 #16A-76, oficina 402, Bogotá, Colombia</div>
          <div><strong>Correo Comercial:</strong> lalupanewsco@gmail.com</div>
        </div>
      </div>

      <div class="closing-actions">
        <h4>Próximos Pasos Inmediatos</h4>
        <div class="pdf-next-step-list">
          <div class="pdf-next-step pdf-next-step--terra">
            <strong>1. Reserva Exclusiva Widget TRM (1 Cupo)</strong>
            <span>Solicita bloqueo de categoría y propuesta anual preferencial escribiendo a <strong>lalupanewsco@gmail.com</strong>.</span>
          </div>
          <div class="pdf-next-step pdf-next-step--gold">
            <strong>2. Cupo de Marca Fundadora (5 Categorías)</strong>
            <span>Elige tu vertical (Deportes, Economía, Actualidad, Estilo de Vida o Tecnología) con tarifas de lanzamiento.</span>
          </div>
          <div class="pdf-next-step">
            <strong>3. Sesión Ejecutiva de Inversión</strong>
            <span>Agenda reunión directa con <strong>Javier Fernández Franco</strong> para revisar proyecciones y estructura de participación.</span>
          </div>
        </div>
      </div>
    </div>
  `;

  const deckHtml = [
    makeSlide(1, 'navy', 'ACTO 01 · APERTURA DE ALTO IMPACTO', 'PITCH COMERCIAL & INVERSIÓN 2026', s1Body, s1Bg),
    makeSlide(2, 'paper', 'ACTO 02 · PULSO DEL MERCADO COLOMBIA', 'INTELIGENCIA DE MERCADO 2025–2026', s2Body),
    makeSlide(3, 'surface', 'ACTO 03 · REDES VS. PORTAL PROPIO', 'VENTAJA COMPETITIVA DEL ACTIVO PROPIO', s3Body),
    makeSlide(4, 'paper', 'ACTO 04A · VITRINA VIVA ESCRITORIO', 'PRODUCTO REAL VERIFICADO', s4Body),
    makeSlide(5, 'paper', 'ACTO 04B · PATROCINIO REAL & MÓVIL', 'PRUEBA COMERCIAL + 75% LECTURA MÓVIL', s5Body),
    makeSlide(6, 'paper', 'ACTO 04C · LA JOYA COMERCIAL TRM', '1 ÚNICO PATROCINADOR EXCLUSIVO', s6Body),
    makeSlide(7, 'navy', 'ACTO 05A · ECOSISTEMA MULTICANAL', 'RED SOCIAL VERIFICADA & LIDERAZGO', s7Body, s7Bg),
    makeSlide(8, 'navy', 'ACTO 05B · PLAN DE ACTIVACIÓN 90 DÍAS', 'MARKETING INTELIGENTE & RETORNO MEDIBLE', s8Body, s8Bg),
    makeSlide(9, 'paper', 'ACTO 06A · SIMULADOR PARA MARCAS', 'ESCENARIO COMERCIAL DE REFERENCIA', s9Body, s9Bg),
    makeSlide(10, 'paper', 'ACTO 06B · SIMULADOR PARA INVERSIONISTAS', 'TESIS DE ESCALAMIENTO Y CAPITAL', s10Body, s10Bg),
    makeSlide(11, 'navy', 'ACTO 07 · VENTANA DE PIONEROS & CIERRE', 'CONTACTO DIRECTO · DIRECCIÓN GENERAL', s11Body, s11Bg),
  ].join('\n');

  document.body.innerHTML = `<div id="pdf-deck">${deckHtml}</div>`;

  // Audit overflow on every composed slide before exporting
  const metrics = [];
  document.querySelectorAll('.pdf-slide').forEach(slide => {
    const idx = slide.getAttribute('data-pdf-slide');
    const bodyEl = slide.querySelector('.pdf-body');
    const overflowY = slide.scrollHeight - slide.clientHeight;
    const overflowX = slide.scrollWidth - slide.clientWidth;
    const bodyOverflowY = bodyEl ? Math.max(0, bodyEl.scrollHeight - bodyEl.clientHeight) : 0;
    metrics.push({
      slide: idx,
      scrollW: slide.scrollWidth,
      scrollH: slide.scrollHeight,
      overflowX,
      overflowY,
      bodyOverflowY
    });
  });
  return metrics;
}
"""


def main() -> int:
    if not SRC_HTML.exists():
        print(f"[ERROR] Source HTML not found: {SRC_HTML}")
        return 1

    hash_before = sha256_file(SRC_HTML)
    print(f"Source HTML SHA-256 (before): {hash_before}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": SLIDE_W, "height": SLIDE_H},
            device_scale_factor=2,
        )
        page = context.new_page()

        # Load the exact untouched standalone HTML via file:// URL
        file_url = SRC_HTML.as_uri()
        page.goto(file_url, wait_until="networkidle", timeout=45000)

        # Wait for Google Fonts & all embedded images
        page.evaluate("() => document.fonts.ready")
        page.evaluate("""() => Promise.all(
            Array.from(document.images).map(img =>
                img.complete ? Promise.resolve() : new Promise(res => { img.onload = img.onerror = res; })
            )
        )""")

        # Keep screen media so all gradients, shadows & exact colors print faithfully
        page.emulate_media(media="screen")
        page.add_style_tag(content=PDF_CSS)

        # Compose the 11 widescreen presentation slides in runtime DOM only
        metrics = page.evaluate(COMPOSE_JS)

        # Wait again for any newly cloned images/fonts to settle
        page.evaluate("() => document.fonts.ready")
        page.evaluate("""() => Promise.all(
            Array.from(document.images).map(img =>
                img.complete ? Promise.resolve() : new Promise(res => { img.onload = img.onerror = res; })
            )
        )""")

        print("\nSlide fit audit (target: 1440x900, 0px overflow):")
        any_overflow = False
        for m in metrics:
            flag = "OK"
            if m["overflowX"] > 0 or m["overflowY"] > 0 or m["bodyOverflowY"] > 0:
                flag = "OVERFLOW!"
                any_overflow = True
            print(
                f"  Slide {int(m['slide']):02d}: {m['scrollW']}x{m['scrollH']} "
                f"(ovX={m['overflowX']}, ovY={m['overflowY']}, bodyOvY={m['bodyOverflowY']}) [{flag}]"
            )

        OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
        page.pdf(
            path=str(OUT_PDF),
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()

    # Verify source HTML was NOT modified
    hash_after = sha256_file(SRC_HTML)
    if hash_before != hash_after:
        raise RuntimeError("CRITICAL: Source HTML hash changed during PDF build!")

    # Verify generated PDF structure with PyMuPDF
    doc = fitz.open(str(OUT_PDF))
    page_count = len(doc)
    first_rect = doc[0].rect
    total_text_chars = sum(len(pg.get_text("text")) for pg in doc)
    doc.close()

    size_bytes = OUT_PDF.stat().st_size
    print(f"\n[OK] Generated widescreen vector PDF:")
    print(f"     Path: {OUT_PDF}")
    print(f"     Pages: {page_count} (page size: {first_rect.width:.1f} x {first_rect.height:.1f} pt)")
    print(f"     Size: {size_bytes:,} bytes ({size_bytes / (1024 * 1024):.2f} MB)")
    print(f"     Selectable vector text: {total_text_chars:,} chars")
    print(f"     Source HTML SHA-256 (after):  {hash_after} (100% UNCHANGED)")

    if any_overflow:
        print("\n[WARNING] One or more slides reported layout overflow! Inspect and tighten spacing.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
