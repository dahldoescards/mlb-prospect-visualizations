# MLB Prospect Success Rate Visualizations

Interactive visualizations showing Career WAR vs Career Length for each MLB prospect card release from 2009-2025.

## Overview

This repository contains HTML visualizations for 48 different Bowman releases, plotting each player's career WAR against their career length. Only players who have debuted and achieved positive WAR are displayed.

## Features

- **Interactive Scatter Plots**: Each release has its own visualization showing player performance
- **Tabbed Navigation**: Easy browsing through all releases via tabs
- **Player Labels**: Each point is labeled with the player's name
- **Hover Details**: Hover over any point to see detailed information

## How to View

1. Visit the GitHub Pages URL (once deployed)
2. Use the tabs at the top to navigate between different releases
3. Each release shows a scatter plot with:
   - X-axis: Career WAR (Wins Above Replacement)
   - Y-axis: Career Length (years)
   - Each point represents a player who debuted with positive WAR

## Data Source

The visualizations are based on analysis of over 3,200 prospects across 48 different Bowman releases from 2009 to 2025, tracking their journey from prospect card to major league performance using FanGraphs WAR data.

## Releases Included

- Bowman (2009-2025)
- Bowman Chrome (2010-2025)
- Bowman Draft (2010-2024)

## Notes

- Only players who have debuted and have WAR > 0 are displayed
- Recent releases (2020-2025) may show fewer players as many prospects are still developing
- Career length is calculated from debut year to last active year

## Local Development

To regenerate the HTML files:

```bash
python3 generate_visualizations.py
```

Requires the `mlb_analysis_results.json` file in the Downloads folder.




