# FlexiMart Data Architecture Project

**Student Name:** Raghavi Rajesh
**Student ID:** BITSOM_BA_25072040
**Email:** raghavirajesh7@gmail.com
**Date:** 06 Jan 2026

## Project Overview

This project implements an end-to-end data architecture for the FlexiMart retail system. It includes a Python based ETL pipeline to clean and load transactional data into a relational database, NoSQL operations using MongoDB for product catalog analysis, and a data warehouse designed using a star schema for analytical reporting.


## Repository Structure
├── part1-database-etl/
│   ├── etl_pipeline.py
│   ├── schema_documentation.md
│   ├── business_queries.sql
│   └── data_quality_report.txt
├── part2-nosql/
│   ├── nosql_analysis.md
│   ├── mongodb_operations.js
│   └── products_catalog.json
├── part3-datawarehouse/
│   ├── star_schema_design.md
│   ├── warehouse_schema.sql
│   ├── warehouse_data.sql
│   └── analytics_queries.sql
└── README.md

## Technologies Used

- Python 3.14.0, pandas, mysql-connector-python
- MySQL 8
- MongoDB 6.0

## Setup Instructions

### Database Setup

```bash
# Create databases
mysql -u root -p -e "CREATE DATABASE fleximart;"
mysql -u root -p -e "CREATE DATABASE fleximart_dw;"

# Run Part 1 - ETL Pipeline
python part1-database-etl/etl_pipeline.py

# Run Part 1 - Business Queries
mysql -u root -p fleximart < part1-database-etl/business_queries.sql

# Run Part 3 - Data Warehouse
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_schema.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_data.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/analytics_queries.sql
``` 
### MongoDB Setup

mongosh < part2-nosql/mongodb_operations.js


## Key Learnings

Through this project, I learned how to design and implement an ETL pipeline using Python and pandas while maintaining data integrity across relational tables. I gained hands-on experience in handling missing values, duplicates, and foreign key mappings. Additionally, I understood how NoSQL databases like MongoDB differ from relational systems and how data warehouses support analytical workloads.


## Challenges Faced

1. Handling missing and inconsistent customer and product identifiers during data loading.: This was resolved by creating ID mapping dictionaries to maintain referential integrity.

2. Designing the correct execution order for ETL, database loading, and reporting.: This was solved by structuring the pipeline into clear stages and adding execution flags for flexibility.


