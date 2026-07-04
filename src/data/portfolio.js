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
      'A templated Claude Code plugin that auto-installs development skills, domain agents, methodology docs, and hooks into any project — collapsing repeated manual setup into one command, with 10 project presets and a 93-test suite.',
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
      'A self-hosted ELT pipeline pulling daily Oura Ring health metrics via OAuth2 into Snowflake, transformed through 15 dbt models and orchestrated by Dagster across daily, weekly, and monthly schedules.',
    slug: 'oura',
    tags: ['Python', 'ETL/ELT', 'Data Pipelines'],
    href: 'https://github.com/cdcoonce/Oura-Pipeline',
    featured: true,
  },
  {
    title: 'my-brain — Second-Brain Knowledge System',
    date: 'Jul 2026',
    description:
      'A graph-first Obsidian vault wired to a Claude Code automation layer — 397 interlinked notes and ~4,500 wikilinks across 11 life domains, auto-committed and synced across two machines by a session hook, with 84 custom skills, agents, and hooks doing the upkeep.',
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
      'Integrates housing price, income, and commute data across U.S. metros to model affordability tradeoffs with ETL, regression, and statistical visualization.',
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
];

export const skills = [
  { name: 'Languages', tags: ['Python', 'SQL', 'R'] },
  { name: 'Techniques', tags: ['ETL/ELT', 'Machine Learning', 'Statistical Analysis'] },
  { name: 'Tools & Platforms', tags: ['Tableau', 'Excel', 'Shiny'] },
  { name: 'Focus Areas', tags: ['Data Visualization', 'Analytics Dashboards', 'Data Pipelines'] },
];

export const metrics = [
  { value: '8', label: 'Projects shipped' },
  { value: '4+', label: 'Data pipelines built' },
  { value: '6', label: 'Languages & tools' },
  { value: '1.8M+', label: 'Records processed' },
];

export const experience = [
  {
    period: '2025 — Present',
    role: 'Analyst, Analytics Engineering',
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
