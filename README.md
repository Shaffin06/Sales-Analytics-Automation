Sales Analytics Automation – Python & SQL

A fully automated Sales Analytics dashboard that extracts data from an SQL database, generates charts, and compiles everything into a professional multi-page PDF report.

Features:
Automated SQL data fetching,
8 professional charts (bar, line, pie, histogram),
Clean two-column visual dashboard layout,
Reference tables included,
Fully modular & extensible code, and
Works with Oracle / MySQL

Tech Stack:
Python,
Pandas,
Matplotlib,
ReportLab,
Oracle SQL, and
Faker (for sample data generation)

Project Structure:

sales_dashboard.py      # Main program + chart/SQL functions

report_generator.py     # PDF builder using ReportLab

config.py               # Database connection file

Project.sql              # Tables + sample seed data

Sales_Report_20251211_181724.pdf       # Example output

Sample Output:
A professionally formatted PDF is generated with
Executive Summary,
2-column chart dashboard,
City + Customer insights,
Product performance charts, and
Reference data tables

Here's how some of the generated charts look like:

<img width="700" height="400" alt="image" src="https://github.com/user-attachments/assets/d2ac1374-ecea-4e25-89dc-527bc51d1f35" />

<img width="600" height="400" alt="image" src="https://github.com/user-attachments/assets/e4f9be45-a2be-4d6b-8810-c6677b656a84" />

<img width="800" height="400" alt="image" src="https://github.com/user-attachments/assets/b28cf057-f12f-4598-93db-e10b87d935ae" />

Running the Project:
Run the following code in your command prompt

python sales_dashboard.py

Select '1 - 6' to generate a specific chart or data.
Select '7' to generate the full PDF.



