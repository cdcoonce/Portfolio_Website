# Knowledge-Base

<!-- generated:start -->
## Context File Pipeline

```mermaid
flowchart LR
    Files["WebContent/context/*.md"] --> Read["Read & parse files"]
    Read --> Inventory["File inventory table"]
    Inventory --> Wiki["Knowledge-Base.md"]
    Read --> WordCount["Word count per file"]
    WordCount --> Inventory
```

## Knowledge Base Files

These Markdown files are loaded into the Lambda chat agent's context window.

| File | Word Count | Topic |
|---|---|---|
| `airbnb-listing.md` | 490 | AirBnB Listing Analysis |
| `ames-housing.md` | 609 | Ames Housing Price Prediction |
| `baby-names.md` | 564 | Baby Names Analysis |
| `bio.md` | 692 | Bio |
| `data-archive.md` | 749 | Google Analytics Data Archive |
| `electricity-consumption.md` | 534 | Electricity Consumption Analysis |
| `energy-analytics-pipeline.md` | 480 | Energy Analytics Pipeline with Dagster |
| `global-co2-emissions.md` | 550 | Global CO₂ Emissions Analysis |
| `housing-affordability.md` | 1,251 | Housing Affordability & Commute Trade-Off Analysis |
| `manufacturing-downtime.md` | 582 | Manufacturing Downtime Analysis |
| `motor-vehicle-thefts.md` | 540 | Motor Vehicle Thefts Analysis |
| `national-parks-analysis.md` | 653 | National Parks Visitation Analysis |
| `national-parks-dashboard.md` | 494 | National Parks Visitation Dashboard |
| `nyc-collision.md` | 574 | NYC Collision Analysis |
| `oura-pipeline.md` | 858 | Oura Ring Health Data Pipeline |
| `portfolio-website.md` | 730 | Portfolio Website |
| `renewable-asset-pipeline.md` | 659 | Renewable Asset Performance Pipeline |
| `restaurant-sales.md` | 465 | Restaurant Sales Analysis |
| `skills.md` | 721 | Skills Overview |
| `sleep-deprivation.md` | 535 | Sleep Deprivation & Cognitive Performance Analysis |
| `spaceship-titanic.md` | 707 | Spaceship Titanic Classification |
| `synthetic-signal-observatory.md` | 498 | Synthetic Signal Observatory |
| `testimonials.md` | 275 | Testimonials |
| `wine-quality.md` | 683 | Wine Quality Analysis |
| `world-happiness.md` | 583 | World Happiness Dashboard |

**Total:** 25 files · 15,476 words
<!-- generated:end -->
