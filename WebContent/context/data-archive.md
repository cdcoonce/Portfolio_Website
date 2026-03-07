# Google Analytics Data Archive

## Classification

- **Type:** Independent
- **Status:** Complete
- **Featured:** No

## Summary

A data preservation project where Charles designed and deployed Python scripts to export, validate, and anonymize historical Google Analytics 3 data from 70 web properties before Google's deprecation deadline. Completed during his internship at OneAmerica Financial, this project preserved over 10 years of web analytics data that would have otherwise been permanently lost.

## Business Problem

Google announced that Universal Analytics (GA3) would be permanently deprecated on July 1, 2024, after which all historical data would become inaccessible. OneAmerica Financial had 70 web properties with years of analytics history that stakeholders relied on for trend analysis and reporting. Manually exporting this data through the Google Analytics dashboard was impractical given the volume and the tight one-month deadline.

## Approach

Charles developed a Python-based automation pipeline consisting of three scripts. The first script authenticated with the Google Analytics API and iterated through all 70 properties, extracting data monthly and yearly as CSV files and saving them to an enterprise server. The second script performed automated validation — scanning each exported file to verify record counts, date ranges, and expected column headers, while flagging anomalies or missing values for manual review. The third script anonymized sensitive property names using a token mapping system, replacing identifying attributes with unique IDs before sharing or archiving the files.

Before writing any code, Charles collaborated with stakeholders to define and finalize a data dictionary specifying exactly which metrics and dimensions each CSV would contain.

## Key Results & Insights

- Successfully archived all historical analytics data from 70 properties before the deprecation deadline.
- Automated validation caught data discrepancies early, preserving data integrity across the entire archive.
- The token-based anonymization system protected sensitive property names while maintaining data usability.
- The automated approach reduced what would have been weeks of manual export work to a manageable timeline.
- Validation reports (both summary and detailed) provided stakeholders with confidence in the completeness and accuracy of the archived data.

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
