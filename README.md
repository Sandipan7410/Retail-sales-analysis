# Retail Sales Analysis using Python & SQL

## 📌 Project Overview

This project analyzes retail sales data using **Python, Pandas, and SQL**.

The project covers data cleaning and transformation using Python, followed by SQL-based analysis to identify important business insights related to products, categories, regions, cities, and monthly sales.

The final analysis was presented through an interactive **Power BI dashboard**.

---

## 🛠️ Tools & Technologies

- Python
- Pandas
- SQL
- SQLite
- Power BI
- Google Colab
- Kaggle Dataset

---

## 🔄 Project Workflow

Kaggle Retail Orders  
↓  
Python & Pandas  
↓  
Data Cleaning & Transformation  
↓  
SQLite Database  
↓  
SQL Analysis  
↓  
Power BI Dashboard

---

## 🧹 Data Preparation

The dataset was cleaned and prepared using Pandas.

Main steps included:

- Imported the retail orders dataset
- Handled missing values
- Checked for duplicate records
- Checked data types
- Standardized column names
- Converted order date into date format
- Created new calculated columns

### Calculated Columns

**Discount**

```text
discount = list_price × discount_percent × 0.01
