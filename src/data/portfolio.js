// @ts-check
/**
 * Portfolio content model for the tabbed homepage.
 * Copy is sourced from the Claude Design comp; images map to assets already
 * shipped in /public/assets so we reuse the same source art.
 */

/** @typedef {{ title: string, date: string, description: string, image: string, imageContain?: boolean, tags: string[], href: string }} Project */

/** @type {Project[]} */
export const projects = [
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
      'ELT pipeline extracting Oura data via API into Snowflake, transformed with dbt and orchestrated by Dagster with daily partitions.',
    image: '/assets/projects/oura-pipeline.svg',
    imageContain: true,
    tags: ['Python', 'ETL/ELT', 'Data Pipelines'],
    href: 'https://github.com/cdcoonce/Oura-Pipeline',
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
  { value: '6', label: 'Data projects shipped' },
  { value: '1.8M+', label: 'Records analyzed' },
  { value: '150+', label: 'Countries covered' },
  { value: '270yr', label: 'CO₂ history modeled' },
];

export const experience = [
  {
    period: '2024 — Present',
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

export const testimonials = [
  {
    quote:
      'During his time as an IT intern at OneAmerica Financial, he demonstrated exceptional people skills, a strong work ethic, and a genuine passion for technology.',
    author: 'Aaron Wallen',
    job: 'Director of Business Analysis',
    company: 'OneAmerica Financial',
  },
  {
    quote:
      "Charles' approach was thorough, well planned, and inclusive of his team. His demeanor while leading difficult project meetings was positive and encouraging, and showed both polish and empathy.",
    author: 'Kevin Brennan',
    job: 'IT Business Planning Consultant',
    company: 'OneAmerica Financial',
  },
  {
    quote:
      'He collaborated and communicated well, focused on what his stakeholders wanted, and demonstrated interpersonal savviness and adaptability.',
    author: 'Katie Marks',
    job: 'Business Relationship Management Director',
    company: 'OneAmerica Financial',
  },
  {
    quote:
      'He consistently sought out new challenges and opportunities to learn, which is a testament to his passion.',
    author: 'Chris McGowan',
    job: 'Training Director',
    company: 'Montana Electrical Training Center',
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
