# Google Analytics Data Archive

## Classification

- **Type:** Independent
- **Status:** Complete
- **Featured:** No
- **Date:** Dec 2024

## Summary

A data preservation project where Charles designed and deployed Python scripts to export, validate, and anonymize historical Google Analytics 3 data from 70 web properties before Google's deprecation deadline. Completed during his internship at OneAmerica Financial, this project preserved over 10 years of web analytics data that would have otherwise been permanently lost.

## Business Problem

Google announced that Universal Analytics (GA3) would be permanently deprecated on July 1, 2024, after which all historical data would become inaccessible. OneAmerica Financial had 70 web properties with years of analytics history that stakeholders relied on for trend analysis and reporting. Manually exporting this data through the Google Analytics dashboard was impractical given the volume and the tight one-month deadline.

## Approach

Charles developed a Python-based automation pipeline consisting of three scripts. The first script authenticated with the Google Analytics API and iterated through all 70 properties, extracting data monthly and yearly as CSV files and saving them to an enterprise server. The second script performed automated validation — scanning each exported file to verify record counts, date ranges, and expected column headers, while flagging anomalies or missing values for manual review. The third script anonymized sensitive property names using a token mapping system, replacing identifying attributes with unique IDs before sharing or archiving the files.

Before writing any code, Charles collaborated with stakeholders to define and finalize a data dictionary specifying exactly which metrics and dimensions each CSV would contain.

## Key Results & Insights

### Scale & Scope

- **70 web properties archived** — each with up to 10+ years of monthly and yearly data — extracted, validated, and anonymized within a one-month window before Google's irreversible July 2024 deprecation deadline.
- The automated extraction script eliminated an impractical volume of manual dashboard exports, reducing a weeks-long manual process to a single programmatic pipeline run per property — a concrete demonstration of automation's leverage on data preservation tasks.
- All files were organized on the enterprise server by property, year, and month, preserving the original temporal structure rather than flattening the entire archive into a single export.

### Data Quality & Integrity

- **Automated validation verified record counts, date ranges, and column headers for every exported file** — catching discrepancies that manual spot-checking across hundreds of CSVs would almost certainly have missed.
- The validation pipeline produced both summary reports (property-level pass/fail) and detailed reports (file-level anomaly logs), giving stakeholders confidence in completeness without requiring them to audit every CSV individually.
- The data dictionary, co-designed with stakeholders before a single line of code was written, ensured every file contained exactly the agreed-upon metrics and dimensions — preventing the common pitfall of format mismatches discovered after the migration window closes.

### Privacy & Security

- A **token-based anonymization system replaced sensitive property identifiers** (business unit names, product landing page URLs) with unique IDs, enabling the archive to be shared across teams without exposing identifying business information.
- The token map was maintained separately from the archive itself, so the anonymized CSVs could be distributed to broader audiences while the mapping key stayed restricted to authorized stakeholders.

### Business Impact

- By preserving **over 10 years of historical web analytics** across 70 properties, the project enabled OneAmerica Financial to retain trend analysis and year-over-year benchmarking capabilities that would have been permanently destroyed at the deprecation deadline — data that cannot be regenerated.
- Completing the project as a single developer within a one-month internship demonstrates the kind of high-leverage automation work that scales data preservation efforts without scaling headcount.

## Technologies Used

- **Scripting:** Python
- **API integration:** Google Analytics API (authentication, data extraction)
- **Validation:** Automated Python scripts for record counts, date ranges, column verification
- **Anonymization:** Token mapping system for sensitive property names
- **Data format:** CSV (organized by year and month)

## Challenges & Solutions

The biggest challenge was scale — 70 properties, each with potentially years of monthly data, all needing to be extracted, validated, and anonymized within about a month. Charles addressed this by building the extraction script to iterate through properties programmatically rather than handling each one manually. The validation script was essential for catching issues that would have been invisible in a manual process, such as incomplete date ranges or unexpected column mismatches.

## Links

- **GitHub:** https://github.com/cdcoonce/Google_Analytics_Data_Archive

## Skills Demonstrated

Data Wrangling & ETL, Data Engineering & Pipelines, DevOps & Tooling
