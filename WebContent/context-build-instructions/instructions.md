# Context Document Instructions

Guidelines for creating consistent markdown documents that live in the portfolio website's `context/` folder. These documents serve as the knowledge base for a chat agent on [charleslikesdata.com](https://charleslikesdata.com) that answers questions about Charles Coonce's projects, background, and skills.

---

## Audience

The primary audience is **recruiters and hiring managers**. General visitors and fellow developers may also interact with the agent, but all content should be written with hiring decision-makers in mind.

---

## Tone & Voice

- **Third person** — always refer to "Charles," never "I" or "me"
- **Conversational but professional** — approachable without being casual or stiff
- **Business-first** — lead with the problem solved and the outcome, then mention technologies
- **Honest and self-aware** — distinguish between guided coursework and independent projects; don't oversell

---

## File Structure

All context documents live in a **flat structure** inside the `context/` folder:

```
context/
├── bio.md                          # Background and career narrative
├── skills.md                       # Skills organized by capability area
├── housing-affordability.md        # Project: Housing Affordability & Commute Analysis
├── wine-quality.md                 # Project: Wine Quality Analysis
├── national-parks-dashboard.md     # Project: National Parks Visitation Dashboard
├── manufacturing-downtime.md       # Project: Manufacturing Downtime Analysis
├── renewable-asset-pipeline.md     # Project: Renewable Asset Performance Pipeline
├── synthetic-signal-observatory.md # Project: Synthetic Signal Observatory
├── ames-housing.md                 # Project: Ames Housing Price Prediction
├── electricity-consumption.md      # Project: Electricity Consumption Analysis
├── airbnb-listing.md               # Project: AirBnB Listing Analysis
├── energy-analytics-pipeline.md    # Project: Energy Analytics Pipeline with Dagster
├── spaceship-titanic.md            # Project: Spaceship Titanic Classification
├── motor-vehicle-thefts.md         # Project: Motor Vehicle Thefts Analysis
├── baby-names.md                   # Project: Baby Names Analysis
├── data-archive.md                 # Project: Google Analytics Data Archive
├── restaurant-sales.md             # Project: Restaurant Sales Analysis
├── global-co2-emissions.md         # Project: Global CO2 Emissions Analysis
├── sleep-deprivation.md            # Project: Sleep Deprivation Analysis
├── nyc-collision.md                # Project: NYC Collision Analysis
├── world-happiness.md              # Project: World Happiness Dashboard
├── national-parks-analysis.md      # Project: National Parks Visitation Analysis
└── portfolio-website.md            # Project: Portfolio Website
```

**Naming convention:** lowercase, hyphen-separated, no spaces. Use a short descriptive name that matches how the project is commonly referenced.

---

## Off-Limits Topics

The chat agent should **not** answer questions about:

- **Salary expectations** — deflect politely (e.g., "Charles prefers to discuss compensation directly during the interview process.")
- **Opinions about former employers** — deflect politely (e.g., "Charles values the experience he gained at each role and prefers to keep the focus on skills and outcomes.")

---

## Document Types

There are three document types, each with its own template below.

### 1. Bio (`bio.md`)

A narrative summary of Charles's background, career transition, and current trajectory. This is the document the agent draws from when asked "Tell me about Charles" or "What's his background?"

**What to include:**

- Career transition story: electrical trade → data science (frame it as a strength, not a detour)
- Education: Indiana University (BA Telecommunications), Google Data Analytics Certificate, Arizona State University (BS Data Science, expected Dec 2025), Dean's List Spring 2025
- Professional experience highlights: Clearway Energy Group (Analytics Engineering Intern), OneAmerica Financial (Business Analyst Intern), Montana Electrical Training Center (Assistant Training Director)
- Teaching background and how it connects to communication skills
- The data-driven hiring decision story from the Training Center (demonstrates analytical thinking before formal training)

**What to exclude:**

- Mental health details (ADHD, depression) — do not mention
- Specific GPA numbers
- Salary history or expectations

---

### 2. Skills Overview (`skills.md`)

Organized by **capability area**, not by tool name. Each capability area should list the relevant tools/technologies and reference which projects demonstrate that capability.

**Capability areas to cover:**

| Capability Area | Tools & Technologies | Example Projects |
|---|---|---|
| **Data Engineering & Pipelines** | Python, Dagster, dbt, dlt, Polars, Snowflake, DuckDB | Renewable Asset Pipeline, Housing Affordability, Data Archive |
| **Statistical Analysis & Modeling** | Python, statsmodels, scikit-learn, R | Housing Affordability, Wine Quality, Ames Housing, Sleep Deprivation |
| **Machine Learning** | scikit-learn, TensorFlow/Keras, XGBoost | Ames Housing, Spaceship Titanic, Wine Quality |
| **Data Visualization & Dashboards** | Tableau, R Shiny, Matplotlib, Streamlit | Global CO2 Emissions, National Parks Dashboard, World Happiness, Synthetic Signal Observatory |
| **SQL & Database Analytics** | SQL (MySQL), DuckDB, Snowflake | Restaurant Sales, Baby Names, Motor Vehicle Thefts |
| **Spreadsheet & Business Analysis** | Excel (Pivot Tables, Power Query, VLOOKUP) | Manufacturing Downtime, NYC Collision |
| **Data Wrangling & ETL** | Python, Pandas, Polars, GeoPandas | Housing Affordability, Electricity Consumption, AirBnB Listing, Data Archive |
| **Web Development** | HTML5, CSS3, JavaScript (ES Modules) | Portfolio Website |
| **DevOps & Tooling** | Git, GitHub Actions, CI/CD, uv, pytest, Jest | Portfolio Website, Renewable Asset Pipeline, Housing Affordability |

**Format guidance:** For each capability area, write 2–3 sentences describing Charles's experience at that level, then list the tools and reference the projects. Avoid just listing tools — explain what he does with them.

---

### 3. Project Documents

Every project gets its own markdown file. The depth of content can vary based on how much there is to say, but every project document must follow the same structure.

---

## Project Document Template

```markdown
# [Project Name]

## Classification

- **Type:** [Independent | Guided Coursework | Academic]
- **Status:** [Complete | In Progress]
- **Featured:** [Yes | No] (whether it appears on the homepage)

## Summary

[2–3 sentences. What is this project? What problem does it solve or what question does it
answer? Write this as if a recruiter asked "So what is this project about?" at a career fair.]

## Business Problem

[Describe the real-world problem or scenario that motivated the project. Why does this
analysis or tool matter? Who would benefit from it? This section should be understandable
by a non-technical reader.]

## Approach

[Describe what Charles did at a high level. What was the methodology? What steps did the
analysis or pipeline follow? Keep this accessible — a recruiter should be able to follow it.
Save deep technical details for the Technical Details section.]

## Key Results & Insights

[What did Charles find or build? What were the main takeaways? Use concrete numbers or
outcomes where possible. This is the most important section for recruiters — it answers
"what was the impact?"]

## Technologies Used

[List the tools and technologies, briefly noting what each was used for in this project.
Group by role if helpful (e.g., "Data processing: Polars; Orchestration: Dagster").]

## Challenges & Solutions

[Optional but encouraged. What was hard about this project? What did Charles learn or
figure out? This section demonstrates problem-solving ability and growth.]

## Links

- **GitHub:** [repository URL]
- **Live Demo:** [if applicable — dashboard URL, Tableau Public link, etc.]

## Skills Demonstrated

[Tag the capability areas this project demonstrates. These should map to the capability
areas in skills.md. Example: Data Engineering, Statistical Analysis, Data Visualization]
```

---

## Project Classification Guide

Each project should be classified to give the chat agent honest context:

| Classification | Definition | Examples |
|---|---|---|
| **Independent** | Charles conceived, designed, and built the project on his own | Housing Affordability, Renewable Asset Pipeline, Portfolio Website, Synthetic Signal Observatory, Data Archive |
| **Guided Coursework** | Completed as part of a structured learning experience (e.g., Maven Analytics) with provided datasets and guidance | Manufacturing Downtime, Restaurant Sales, Baby Names, Motor Vehicle Thefts, NYC Collision, AirBnB Listing, Electricity Consumption, Global CO2 Emissions, Sleep Deprivation |
| **Academic** | Completed as part of a university course with defined requirements | Ames Housing, Spaceship Titanic, Wine Quality |

> **How the agent should use this:** When asked about a guided project, the agent should be upfront that it was a structured learning exercise, while still highlighting the skills Charles applied and any ways he went beyond the base assignment. For independent projects, emphasize the end-to-end ownership.

---

## Writing Checklist

Before finalizing any context document, verify:

- [ ] Written in **third person** ("Charles built..." not "I built...")
- [ ] **Business problem and results come first**, technical details follow
- [ ] **Classification is accurate** (Independent / Guided Coursework / Academic)
- [ ] **No mental health details** mentioned
- [ ] **No salary or compensation** information
- [ ] **No opinions about former employers**
- [ ] **Technologies are mentioned in context** — not just listed, but tied to what they were used for
- [ ] **Concrete outcomes** are included where possible (numbers, percentages, counts)
- [ ] **Filename follows naming convention** (lowercase, hyphenated, `.md` extension)
- [ ] File is placed directly in the `context/` folder (flat structure)

---

## Example: Short Project Document

Below is an example of a completed project document for reference.

```markdown
# Manufacturing Downtime Analysis

## Classification

- **Type:** Guided Coursework
- **Status:** Complete
- **Featured:** Yes

## Summary

An Excel-based analysis of production line downtime for a soft drink bottling operation.
Charles calculated line efficiency, identified the top downtime factors using Pareto
analysis, and built an operator-by-factor matrix to pinpoint where targeted training
would have the most impact.

## Business Problem

A production manager inherited a bottling line with no visibility into what was causing
downtime or how efficiently operators were running. Without data-driven insight, the team
couldn't prioritize training or maintenance investments.

## Approach

Charles started by calculating batch-level efficiency — comparing actual production time
to the standard minimum for each product. He then aggregated downtime logs by factor and
applied a Pareto analysis to find the 20% of factors causing 80% of lost time. Finally, he
cross-referenced downtime by operator and factor to create a heat map showing where each
operator was losing the most time.

## Key Results & Insights

- Overall line efficiency was approximately 64%.
- The lowest-performing operator (Mac) ran at 61% efficiency — a clear candidate for
  targeted coaching.
- The top 5 downtime factors accounted for roughly 80% of total downtime.
- Three of those top 5 factors were operator errors, pointing to training as the
  highest-leverage intervention.
- Recommendations included standardized machine adjustment training, batch change coaching
  for specific operators, and a preventative maintenance schedule.

## Technologies Used

- **Excel:** Pivot tables, VLOOKUP, SUMIFS, conditional formatting, combo charts
  (Pareto), and bar charts for efficiency comparison.

## Challenges & Solutions

The main challenge was structuring the raw downtime logs so they could be cross-referenced
with both the productivity data and the operator assignments. Charles used VLOOKUP to map
each downtime entry back to its operator, then SUMIFS to build the operator-by-factor
matrix — a practical exercise in joining data across related tables without a database.

## Links

- **GitHub:** https://github.com/cdcoonce/Manufacturing_Downtime_Analysis

## Skills Demonstrated

Spreadsheet & Business Analysis, Data Visualization
```

---

## Maintenance

When a new project is added to the portfolio website:

1. Create a new `.md` file in `context/` following the project template
2. Classify it accurately (Independent / Guided Coursework / Academic)
3. Update `skills.md` if the project introduces a new capability area or tool
4. Run through the writing checklist before committing
