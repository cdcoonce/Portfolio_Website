'use strict';

export const projects = [
  {
    id: 'national-parks-dashboard',
    href: 'https://iuq9gs-charles-coonce.shinyapps.io/visitation/',
    title: 'National Parks Dashboard',
    date: '2024-09',
    description:
      'Interactive Shiny dashboard exploring NPS visitation trends across parks, states, and time periods.',
    image: './WebContent/assets/Shiny_Apps_Assets/VisitationGraphic.png',
    imageAlt: 'National Parks Dashboard',
    tags: ['r', 'shiny', 'analytics-dashboard', 'visualization'],
    featured: true,
  },
  {
    id: 'wine-quality',
    href: 'https://github.com/cdcoonce/Wine-Quality',
    title: 'Wine Quality Analysis',
    date: '2024-11',
    description:
      'Predicts wine quality ratings in Python by comparing logistic regression, decision trees, and random forests on physicochemical properties.',
    image: './WebContent/assets/Wine/White_Wine_Model.png',
    imageAlt: 'Wine Quality',
    imageContain: true,
    tags: ['python', 'machine-learning', 'statistical-analysis'],
    featured: true,
  },
  {
    id: 'electricity-consumption',
    href: 'https://github.com/cdcoonce/Electricity_Consumption_Analysis',
    title: 'Electricity Consumption',
    date: '2025-02',
    description:
      'Analyzes U.S. electricity consumption by sector and source, transforming raw EIA data into stacked area charts with a Python ETL pipeline.',
    image: './WebContent/assets/Electriciy_Consumption/stacked_area.png',
    imageAlt: 'Electricity Consumption',
    tags: ['python', 'etl', 'visualization'],
  },
  {
    id: 'manufacturing-downtime',
    href: 'https://github.com/cdcoonce/Manufacturing_Downtime_Analysis',
    title: 'Manufacturing Downtime Analysis',
    date: '2025-02',
    description:
      'Identifies root causes of production downtime with an Excel BI dashboard tracking machine failures, shift patterns, and operator performance metrics.',
    image: './WebContent/assets/Manufacturing_Downtime_Analysis/Dashboard.png',
    imageAlt: 'Manufacturing Downtime Dashboard',
    imageContain: true,
    tags: ['excel', 'business-intelligence', 'analytics-dashboard'],
  },
  {
    id: 'national-parks-analysis',
    href: 'https://github.com/cdcoonce/National_Parks_Project/wiki',
    title: 'National Parks Analysis',
    date: '2024-08',
    description:
      "Explores 20+ years of NPS visitation data with R, uncovering seasonal trends, regional disparities, and the pandemic's measurable impact on park attendance.",
    image: './WebContent/assets/National_Parks_Project_Assets/NPS_plot5.png',
    imageAlt: 'National Parks Visitation',
    tags: ['r', 'visualization', 'statistical-analysis'],
  },
  {
    id: 'portfolio-website',
    href: 'https://github.com/cdcoonce/Portfolio_Website',
    title: 'Portfolio Website',
    date: '2024-08',
    description:
      'Responsive personal portfolio built with vanilla HTML, CSS, and JavaScript, featuring a filterable project gallery, testimonial carousel, and mobile-friendly navigation.',
    image: './WebContent/assets/Portfolio_Website_Project_Assets/PortfolioCode.png',
    imageAlt: 'Portfolio Website',
    imageContain: true,
    tags: ['html', 'css', 'javascript'],
  },
  {
    id: 'world-happiness-dashboard',
    href: 'https://iuq9gs-charles-coonce.shinyapps.io/whrcharlescoonce/',
    title: 'World Happiness Dashboard',
    date: '2024-09',
    description:
      'Interactive Shiny dashboard exploring World Happiness Report data, letting users compare GDP, social support, and freedom scores across 150+ countries.',
    image: './WebContent/assets/Shiny_Apps_Assets/WorldHappinessGraphic.png',
    imageAlt: 'World Happiness Dashboard',
    tags: ['r', 'shiny', 'analytics-dashboard', 'visualization'],
  },
  {
    id: 'data-archive',
    href: 'https://github.com/cdcoonce/Google_Analytics_Data_Archive',
    title: 'Data Archive',
    date: '2024-12',
    description:
      'Automates extraction and archiving of Google Analytics data with Python, preserving historical web metrics in a structured, queryable format for long-term analysis.',
    image: './WebContent/assets/GA_Project/DetValidationReport.png',
    imageAlt: 'Data Archive',
    imageContain: true,
    tags: ['python', 'etl', 'data-pipelines'],
  },
  {
    id: 'nyc-collision-analysis',
    href: 'https://github.com/cdcoonce/NYC_Traffic_Accidents',
    title: 'NYC Collision Analysis',
    date: '2025-02',
    description:
      'Analyzes 1.8M+ NYC traffic collisions in Excel to surface the most dangerous contributing factors, high-risk boroughs, and peak collision time windows.',
    image: './WebContent/assets/NYC_traffic/top_dangerous_causes.png',
    imageAlt: 'Dangerous Collision Factors',
    tags: ['excel', 'business-intelligence', 'visualization'],
  },
  {
    id: 'global-co2-emissions',
    href: 'https://github.com/cdcoonce/Global_CO2_Emissions',
    title: 'Global CO2 Emissions',
    date: '2025-02',
    description:
      'Tableau dashboard tracking global CO2 emissions by country and sector from 1750\u20132020, spotlighting the largest emitters and per-capita disparities over time.',
    image: './WebContent/assets/Global_CO2_Emissions/Dashboard.png',
    imageAlt: 'Global CO2 Emissions Dashboard',
    imageContain: true,
    tags: ['tableau', 'analytics-dashboard', 'visualization'],
  },
  {
    id: 'airbnb-listing-analysis',
    href: 'https://github.com/cdcoonce/Airbnb_Listing_Analysis',
    title: 'AirBnB Listing Analysis',
    date: '2025-02',
    description:
      'Analyzes Airbnb listing data with Python to uncover pricing drivers, occupancy patterns, and neighborhood-level revenue trends across major markets.',
    image: './WebContent/assets/Airbnb_Listings_Analysis/Final_Viz.png',
    imageAlt: 'AirBnB Listing Analysis Visualization',
    tags: ['python', 'etl', 'statistical-analysis'],
  },
  {
    id: 'sleep-deprivation',
    href: 'https://github.com/cdcoonce/Sleep_Deprivation',
    title: 'Sleep Deprivation Analysis',
    date: '2025-02',
    description:
      'Investigates the relationship between sleep deprivation and high-stress reaction times using Python, identifying statistically significant performance thresholds.',
    image: './WebContent/assets/SleepDeprivation_HighStress_Reactions.png',
    imageAlt: 'Sleep Deprivation High Stress Reactions',
    tags: ['python', 'etl', 'statistical-analysis'],
  },
  {
    id: 'restaurant-order-analysis',
    href: 'https://github.com/cdcoonce/Restaurant_Order_Analysis',
    title: 'Restaurant Order Analysis',
    date: '2025-03',
    description:
      'Uses SQL joins and aggregations to analyze restaurant order data, revealing peak ordering windows, top menu items, and revenue concentration by category.',
    image: './WebContent/assets/Restaurant_Order_Analysis/Table_Joined_Analysis.png',
    imageAlt: 'Restaurant Order Analysis SQL Join',
    imageContain: true,
    tags: ['sql', 'business-intelligence'],
  },
  {
    id: 'motor-vehicle-thefts',
    href: 'https://github.com/cdcoonce/Motor_Vehicle_Thefts',
    title: 'Motor Vehicle Thefts',
    date: '2025-03',
    description:
      "Combines SQL and Excel to analyze motor vehicle theft patterns by make, model year, location, and time of day across New Zealand's national dataset.",
    image: './WebContent/assets/Motor_Vehicle_Thefts/Obj3b_Data_Viz.png',
    imageAlt: 'Motor Vehicle Thefts',
    tags: ['sql', 'excel', 'visualization'],
  },
  {
    id: 'baby-names-analysis',
    href: 'https://github.com/cdcoonce/Baby_Names_Analysis',
    title: 'Baby Names Analysis',
    date: '2025-03',
    description:
      'Queries 140 years of U.S. baby name data with SQL to track generational naming trends, pop culture influences, and regional popularity shifts.',
    image: './WebContent/assets/Baby_Names_Analysis/SQL_Script.png',
    imageAlt: 'Baby Names SQL Script',
    imageContain: true,
    tags: ['sql', 'statistical-analysis'],
  },
  {
    id: 'spaceship-titanic',
    href: 'https://github.com/cdcoonce/Spaceship_Titanic',
    title: 'Spaceship Titanic Classification',
    date: '2025-05',
    description:
      'Builds and evaluates binary classification models for the Spaceship Titanic Kaggle competition, optimizing ROC-AUC and precision-recall tradeoffs with ensemble methods.',
    image: './WebContent/assets/Spaceship_Titanic/ROCPRCGraph.png',
    imageAlt: 'Model Analysis Graphs',
    imageContain: true,
    tags: ['python', 'machine-learning'],
  },
  {
    id: 'oura-pipeline',
    href: 'https://github.com/cdcoonce/Oura-Pipeline',
    title: 'Oura Ring Health Data Pipeline',
    date: '2026-03',
    description:
      'ELT pipeline that extracts Oura Ring health data via API, loads it into Snowflake as semi-structured JSON, and transforms it through dbt into analysis-ready tables \u2014 orchestrated by Dagster with daily partitions.',
    image: './WebContent/assets/Oura_Pipeline/Global_Asset_Lineage.svg',
    imageAlt: 'Oura Ring Health Data Pipeline',
    imageContain: true,
    featured: true,
    tags: ['python', 'etl', 'data-pipelines'],
  },
  {
    id: 'housing-affordability',
    href: 'https://github.com/cdcoonce/housing-commute-analysis',
    title: 'Housing Affordability & Commute Tradeoffs',
    date: '2025-12',
    description:
      'Integrates housing price, income, and commute data across U.S. metros to model affordability tradeoffs using ETL pipelines, machine learning regression, and statistical visualization.',
    image: './WebContent/assets/Housing_Commute_Analysis/rq1_den_scatter.png',
    imageAlt: 'Housing Commute Analysis',
    tags: [
      'python',
      'etl',
      'data-pipelines',
      'machine-learning',
      'statistical-analysis',
      'visualization',
    ],
    featured: true,
  },
];

/**
 * Derived tag registry — the sorted, unique set of every tag used across all projects.
 * This is the single source of truth for filterable tags; filter buttons are generated
 * from this array, making orphan buttons structurally impossible.
 *
 * @type {string[]}
 */
export const tags = [...new Set(projects.flatMap((p) => p.tags))].sort();

/**
 * Human-readable display labels for tags that need special formatting.
 * Tags not listed here are title-cased automatically by the renderer.
 *
 * @type {Record<string, string>}
 */
export const TAG_LABELS = {
  'analytics-dashboard': 'Analytics Dashboards',
  'business-intelligence': 'Business Intelligence',
  'data-pipelines': 'Data Pipelines',
  'machine-learning': 'Machine Learning',
  'statistical-analysis': 'Statistical Analysis',
  css: 'CSS',
  etl: 'ETL/ELT',
  html: 'HTML',
  r: 'R',
  sql: 'SQL',
};
