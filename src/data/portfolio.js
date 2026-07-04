// @ts-check
/**
 * Portfolio content model for the tabbed homepage.
 * Copy is sourced from the Claude Design comp; images map to assets already
 * shipped in /public/assets so we reuse the same source art.
 */

/** @typedef {{ title: string, date: string, description: string, image?: string, imageContain?: boolean, slug?: string, tags: string[], href: string, featured?: boolean, hideFromGallery?: boolean, ctaLabel?: string }} Project */

/** @type {Project[]} */
export const projects = [
  {
    title: 'AFK — Autonomous Coding-Agent System',
    date: 'Jul 2026',
    description:
      'A sovereign, human-gated pipeline that files, executes, and merges coding work through autonomous agents — with a live-ops cockpit tracking PR outcomes, safety quarantines as signal (not failure), and API-equivalent cost per model tier.',
    slug: 'afk',
    tags: ['Python', 'Data Pipelines', 'Analytics Dashboards'],
    href: '/afk-cockpit/',
    featured: true,
    ctaLabel: 'View live cockpit',
  },
  {
    title: 'claude-workflow — Claude Code Plugin',
    date: 'Jul 2026',
    description:
      'A templated Claude Code plugin that auto-installs development skills, domain agents, methodology docs, and hooks into any project — collapsing repeated manual setup into a single command, with project presets and personas for every workflow.',
    slug: 'claude-workflow',
    tags: ['Python', 'AI Tooling'],
    href: 'https://github.com/cdcoonce/claude-workflow',
    featured: true,
  },
  {
    title: 'National Parks Dashboard',
    date: 'Sep 2024',
    description:
      'Interactive Shiny dashboard exploring NPS visitation trends across parks, states, and time periods.',
    image: '/assets/projects/national-parks-dashboard.png',
    imageContain: false,
    tags: ['R', 'Shiny', 'Analytics Dashboards'],
    href: 'https://iuq9gs-charles-coonce.shinyapps.io/visitation/',
  },
  {
    title: 'Oura Ring Health Pipeline',
    date: 'Mar 2026',
    description:
      'A self-hosted ELT pipeline pulling daily Oura Ring health metrics via OAuth2 into Snowflake, transformed with dbt and orchestrated by Dagster across daily, weekly, and monthly schedules.',
    slug: 'oura',
    tags: ['Python', 'ETL/ELT', 'Data Pipelines'],
    href: 'https://github.com/cdcoonce/Oura-Pipeline',
    featured: true,
  },
  {
    title: 'my-brain — Second-Brain Knowledge System',
    date: 'Jul 2026',
    description:
      'A graph-first Obsidian vault wired to a Claude Code automation layer — interlinked notes and wikilinks spanning every life domain, auto-committed and synced across two machines by a session hook, with custom skills, agents, and hooks doing the upkeep.',
    slug: 'my-brain',
    tags: ['Obsidian', 'AI Tooling'],
    href: 'https://github.com/cdcoonce/second-brain',
    featured: true,
    hideFromGallery: true,
    ctaLabel: 'Use this template',
  },
  {
    title: 'Housing Affordability & Commute',
    date: 'Dec 2025',
    description:
      'DAT 490 capstone: a reproducible pipeline integrating ACS income, Zillow rent, and OpenStreetMap transit data across four U.S. metros to model rent-burden and commute tradeoffs with ETL, regression, and spatial visualization.',
    image: '/assets/projects/housing-commute.png',
    imageContain: false,
    tags: ['Python', 'Machine Learning', 'Data Visualization'],
    href: 'https://github.com/cdcoonce/housing-commute-analysis',
  },
  {
    title: 'Wine Quality Analysis',
    date: 'Nov 2024',
    description:
      'Predicts wine quality ratings in Python, comparing logistic regression, decision trees, and random forests on physicochemical properties.',
    image: '/assets/projects/wine-quality.png',
    imageContain: true,
    tags: ['Python', 'Machine Learning'],
    href: 'https://github.com/cdcoonce/Wine-Quality',
  },
  {
    title: 'Global CO₂ Emissions',
    date: 'Feb 2025',
    description:
      'Tableau dashboard tracking global CO₂ emissions by country and sector from 1750–2020, spotlighting the largest emitters and per-capita disparities.',
    image: '/assets/projects/global-co2.png',
    imageContain: true,
    tags: ['Tableau', 'Analytics Dashboards'],
    href: 'https://github.com/cdcoonce/Global_CO2_Emissions',
  },
  {
    title: 'Electricity Consumption',
    date: 'Feb 2025',
    description:
      'Analyzes U.S. electricity consumption by sector and source, transforming raw EIA data into stacked area charts with a Python ETL pipeline.',
    image: '/assets/projects/electricity.png',
    imageContain: false,
    tags: ['Python', 'ETL/ELT', 'Data Visualization'],
    href: 'https://github.com/cdcoonce/Electricity_Consumption_Analysis',
  },
  {
    title: 'Weather-Adjusted Generation Analytics',
    date: 'May 2026',
    description:
      'A production-grade ELT pipeline for weather-normalized renewable-asset performance — dlt ingestion into Snowflake, dbt transformations through a semantic layer, and Polars analytics, all orchestrated by Dagster.',
    slug: 'waga',
    tags: ['Python', 'ETL/ELT', 'Data Pipelines'],
    href: 'https://waga-dashboard.pages.dev',
    featured: true,
  },
  {
    title: 'Ames Housing Model Comparison',
    date: 'Oct 2025',
    description:
      'Compares Linear Regression, k-Nearest Neighbors, and a TensorFlow neural network on the Ames Housing dataset, with preprocessing pipelines, cross-validation, and bias–variance visualization.',
    image: '/assets/projects/ames-housing.png',
    imageContain: true,
    tags: ['Python', 'Machine Learning'],
    href: 'https://github.com/cdcoonce/Ames_Housing_Model_Comparison',
  },
  {
    title: 'Spaceship Titanic Classification',
    date: 'May 2025',
    description:
      'Builds and evaluates binary classification models for the Spaceship Titanic Kaggle competition, optimizing ROC-AUC and precision–recall tradeoffs with ensemble methods.',
    image: '/assets/projects/spaceship-titanic.png',
    imageContain: true,
    tags: ['Python', 'Machine Learning'],
    href: 'https://github.com/cdcoonce/Spaceship_Titanic',
  },
  {
    title: 'Restaurant Order Analysis',
    date: 'Mar 2025',
    description:
      'Uses SQL joins and aggregations to analyze restaurant order data, revealing peak ordering windows, top menu items, and revenue concentration by category.',
    image: '/assets/projects/restaurant-orders.png',
    imageContain: true,
    tags: ['SQL', 'Business Intelligence'],
    href: 'https://github.com/cdcoonce/Restaurant_Order_Analysis',
  },
  {
    title: 'Motor Vehicle Thefts',
    date: 'Mar 2025',
    description:
      "Combines SQL and Excel to analyze motor vehicle theft patterns by make, model year, location, and time of day across New Zealand's national dataset.",
    image: '/assets/projects/motor-vehicle-thefts.png',
    imageContain: false,
    tags: ['SQL', 'Excel', 'Data Visualization'],
    href: 'https://github.com/cdcoonce/Motor_Vehicle_Thefts',
  },
  {
    title: 'Baby Names Analysis',
    date: 'Mar 2025',
    description:
      'Queries 140 years of U.S. baby name data with SQL to track generational naming trends, pop-culture influences, and regional popularity shifts.',
    image: '/assets/projects/baby-names.png',
    imageContain: true,
    tags: ['SQL', 'Statistical Analysis'],
    href: 'https://github.com/cdcoonce/Baby_Names_Analysis',
  },
  {
    title: 'Manufacturing Downtime Analysis',
    date: 'Feb 2025',
    description:
      'Identifies root causes of production downtime with an Excel BI dashboard tracking machine failures, shift patterns, and operator performance metrics.',
    image: '/assets/projects/manufacturing-downtime.png',
    imageContain: true,
    tags: ['Excel', 'Business Intelligence', 'Analytics Dashboards'],
    href: 'https://github.com/cdcoonce/Manufacturing_Downtime_Analysis',
  },
  {
    title: 'NYC Collision Analysis',
    date: 'Feb 2025',
    description:
      'Analyzes 1.8M+ NYC traffic collisions in Excel to surface the most dangerous contributing factors, high-risk boroughs, and peak collision time windows.',
    image: '/assets/projects/nyc-collision.png',
    imageContain: false,
    tags: ['Excel', 'Business Intelligence', 'Data Visualization'],
    href: 'https://github.com/cdcoonce/NYC_Traffic_Accidents',
  },
  {
    title: 'AirBnB Listing Analysis',
    date: 'Feb 2025',
    description:
      'Analyzes Airbnb listing data with Python to uncover pricing drivers, occupancy patterns, and neighborhood-level revenue trends across major markets.',
    image: '/assets/projects/airbnb.png',
    imageContain: false,
    tags: ['Python', 'ETL/ELT', 'Statistical Analysis'],
    href: 'https://github.com/cdcoonce/Airbnb_Listing_Analysis',
  },
  {
    title: 'Sleep Deprivation Analysis',
    date: 'Feb 2025',
    description:
      'Investigates the relationship between sleep deprivation and high-stress reaction times using Python, identifying statistically significant performance thresholds.',
    image: '/assets/projects/sleep-deprivation.png',
    imageContain: false,
    tags: ['Python', 'Statistical Analysis'],
    href: 'https://github.com/cdcoonce/Sleep_Deprivation',
  },
  {
    title: 'Data Archive',
    date: 'Dec 2024',
    description:
      'Automates extraction and archiving of Google Analytics data with Python, preserving historical web metrics in a structured, queryable format for long-term analysis.',
    image: '/assets/projects/data-archive.png',
    imageContain: true,
    tags: ['Python', 'ETL/ELT', 'Data Pipelines'],
    href: 'https://github.com/cdcoonce/Google_Analytics_Data_Archive',
  },
  {
    title: 'World Happiness Dashboard',
    date: 'Sep 2024',
    description:
      'Interactive Shiny dashboard exploring World Happiness Report data, letting users compare GDP, social support, and freedom scores across 150+ countries.',
    image: '/assets/projects/world-happiness.png',
    imageContain: false,
    tags: ['R', 'Shiny', 'Analytics Dashboards'],
    href: 'https://iuq9gs-charles-coonce.shinyapps.io/whrcharlescoonce/',
  },
  {
    title: 'National Parks Analysis',
    date: 'Aug 2024',
    description:
      "Explores 20+ years of NPS visitation data with R, uncovering seasonal trends, regional disparities, and the pandemic's measurable impact on park attendance.",
    image: '/assets/projects/national-parks-analysis.png',
    imageContain: false,
    tags: ['R', 'Data Visualization', 'Statistical Analysis'],
    href: 'https://github.com/cdcoonce/National_Parks_Project/wiki',
  },
  {
    title: 'Portfolio Website',
    date: 'Aug 2024',
    description:
      'Responsive personal portfolio built with vanilla HTML, CSS, and JavaScript, featuring a filterable project gallery, testimonial carousel, and mobile-friendly navigation.',
    image: '/assets/projects/portfolio-website.png',
    imageContain: true,
    tags: ['HTML', 'CSS', 'JavaScript'],
    href: 'https://github.com/cdcoonce/Portfolio_Website',
  },
];

export const skills = [
  { name: 'Languages', tags: ['Python', 'SQL', 'R'] },
  {
    name: 'Data Engineering',
    tags: ['dbt', 'Dagster', 'Polars', 'Snowflake', 'DuckDB', 'dlt', 'ETL/ELT', 'Data Modeling'],
  },
  {
    name: 'Tools & Platforms',
    tags: [
      'Hex',
      'Streamlit',
      'Snowflake Cortex',
      'Tableau',
      'Git',
      'GitHub Actions',
      'AWS Lambda',
    ],
  },
  {
    name: 'Focus Areas',
    tags: [
      'Data Pipelines',
      'Analytics Dashboards',
      'Data Visualization',
      'Business Intelligence',
      'Machine Learning',
    ],
  },
];

export const metrics = [
  { value: '20+', label: 'Projects shipped' },
  { value: '5+', label: 'Data pipelines built' },
  { value: '18', label: 'Languages & tools' },
  { value: '1.8M+', label: 'Records processed' },
];

export const contactMethods = [
  { label: 'Email', value: 'CharlesCoonce@Gmail.com', href: 'mailto:CharlesCoonce@Gmail.com' },
  {
    label: 'LinkedIn',
    value: '/in/charlesdcoonce',
    href: 'https://www.linkedin.com/in/charlesdcoonce/',
  },
  { label: 'GitHub', value: '/cdcoonce', href: 'https://github.com/cdcoonce' },
  { label: 'Resume', value: 'Download PDF', href: '/assets/CharlesCoonce_Resume.pdf' },
];

export const experience = [
  {
    period: '2025 — Present',
    role: 'Analyst, Analytics Engineer, Solutions Architect',
    org: 'Clearway Energy',
    note: 'Build scalable data pipelines and decision-ready dashboards supporting renewable-energy operations and reporting.',
  },
  {
    period: '2023',
    role: 'IT / Business Analysis Intern',
    org: 'OneAmerica Financial',
    note: 'Supported business-analysis initiatives — recognized for exceptional people skills and thorough, well-planned execution.',
  },
  {
    period: 'Prior',
    role: 'Senior Instructor & Asst. Director',
    org: 'Montana Electrical Training Center',
    note: 'Led apprenticeship training and program operations before transitioning into data and analytics.',
  },
];

/**
 * @typedef {Object} Testimonial
 * @property {string} quote
 * @property {string} author
 * @property {string} job
 * @property {string} company
 * @property {string} [linkedin] - Profile URL; when set, the avatar links to it.
 * @property {string} [photo] - Locally-hosted headshot path (e.g. /assets/testimonials/aaron.jpg);
 *   falls back to initials when absent. LinkedIn CDN URLs are NOT usable — they expire.
 */

/** @type {Testimonial[]} */
export const testimonials = [
  {
    quote:
      'During his time as an IT intern at OneAmerica Financial, he demonstrated exceptional people skills, a strong work ethic, and a genuine passion for technology.',
    author: 'Aaron Wallen',
    job: 'Director of Business Analysis',
    company: 'OneAmerica Financial',
    linkedin: 'https://www.linkedin.com/in/aaronwallen/',
    photo: '/assets/testimonials/aaron-wallen.png',
  },
  {
    quote:
      "Charles' approach was thorough, well planned, and inclusive of his team. His demeanor while leading difficult project meetings was positive and encouraging, and showed both polish and empathy.",
    author: 'Kevin Brennan',
    job: 'IT Business Planning Consultant',
    company: 'OneAmerica Financial',
    linkedin: 'https://www.linkedin.com/in/kpbrennan2/',
    photo: '/assets/testimonials/kevin-brennan.jpeg',
  },
  {
    quote:
      'He collaborated and communicated well, focused on what his stakeholders wanted, and demonstrated interpersonal savviness and adaptability.',
    author: 'Katie Marks',
    job: 'Business Relationship Management Director',
    company: 'OneAmerica Financial',
    linkedin: 'https://www.linkedin.com/in/katie-marks-88a408239/',
    photo: '',
  },
  {
    quote:
      'He consistently sought out new challenges and opportunities to learn, which is a testament to his passion.',
    author: 'Chris McGowan',
    job: 'Training Director',
    company: 'Montana Electrical Training Center',
    linkedin: 'https://www.linkedin.com/in/chris-mcgowan-aa898389/',
    photo: '/assets/testimonials/chris-mcgowan.jpeg',
  },
  {
    quote:
      'Working under pressure is an attribute most common with Charles. When things need to be done at the eleventh hour, he is the perfect fit for the job — a practical person who relates theory to real-life situations, and a professional with the absolute objective of recording success.',
    author: 'Chris Allard',
    job: 'Project Manager',
    company: 'Mechanical Technologies Inc.',
    linkedin: 'https://www.linkedin.com/in/chris-allard-1b618714/',
    photo: '/assets/testimonials/chris-allard.jpeg',
  },
];

export const presetGroups = [
  {
    category: 'Projects',
    items: ['What projects use Python?', 'What dashboards has Charles built?'],
  },
  {
    category: 'Pipelines',
    items: ['Tell me about the data pipelines', 'What tools power the ELT stack?'],
  },
  {
    category: 'About Charles',
    items: ["What's Charles's current role?", 'What tools does Charles use?'],
  },
];

export const navItems = [
  { label: 'Overview', key: 'overview' },
  { label: 'Work', key: 'work' },
  { label: 'Experience', key: 'experience' },
  { label: 'Testimonials', key: 'testimonials' },
  { label: 'Ask AI', key: 'ai' },
  { label: 'Contact', key: 'contact' },
];
