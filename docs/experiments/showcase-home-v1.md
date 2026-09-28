# Prototype Lab Showcase v1

**Status:** Validated / Production  
**Branch:** `prototype/showcase-home-v1` (merged)  
**Production:** https://design-system-lab-weld.vercel.app/ (**Ready**)  
**Main commit:** `1d2df20` (merge) · content `e9ddc4c`  
**Route:** `/`

## Purpose

Public portfolio homepage for Prototype Lab: design-system → tokens → React → Storybook → AI-assisted prototypes → Vercel → analytics → evidence-driven DS iteration.

## Scope shipped

Header · Hero · Outcome metrics · Prototype cards · Process · Experiment outcomes · About · Footer  
SEO metadata · OG SVG fallback · Light/Dark · responsive layout

## Explicit non-goals

No placeholder public links · no new DS components · no custom Vercel analytics events · no prototype redesigns

## Configuration

Public URLs live in `src/prototype-shell/site-config.ts`. Unconfigured case-study / social hrefs are hidden (not rendered as dead links).

## Open polish (non-blocking)

Final 1200×630 raster OG image — SVG fallback remains wired.
