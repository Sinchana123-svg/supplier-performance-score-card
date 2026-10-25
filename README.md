# DA-32 Supplier Performance Scorecard System

[![Domain](https://img.shields.io/badge/Domain-Supply%20Chain%20%26%20Logistics-blue.svg)](#domain)
[![Tech Stack](https://img.shields.io/badge/Tech%20Stack-SQL%20(SQLite)%20%7C%20Python%20%7C%20Power%20BI-orange.svg)](#tech-stack)
[![Dashboard](https://img.shields.io/badge/Dashboard-localhost%3A8080%2Fdashboard.html-success.svg)](#interactive-dashboard)
[![Status](https://img.shields.io/badge/Status-100%25%20Functional-brightgreen.svg)](#how-to-run)

---

## 📌 Executive Summary & Objective

**Goal:** Identify which suppliers deliver late or defective across enterprise procurement operations.

The **DA-32 Supplier Performance Scorecard** is an enterprise analytics solution built on a reproducible stack (**SQL/SQLite + Python + Power BI**) without external dependencies like XAMPP or complex ML training.

### Key Operational Metrics
- **Total Suppliers:** 50 active industrial vendors across 4 categories and 5 logistics hubs (*Bangalore, Mumbai, Delhi, Chennai, Pune*).
- **Total Orders:** 3,000 purchase orders deploying **₹25.72 Crores** in procurement spend.
- **Global On-Time Delivery Rate:** **72.0%** (840 late deliveries breaching SLA).
- **Global Defect Rate:** **0.96%** (15,901 non-conforming units across 1.66M delivered units).
- **Average Lead Time:** **42.2 Days** (Planned range: 0 to 180 days).

---

## 🛠 Tech Stack & Architecture

| Layer | Component | Description |
| :--- | :--- | :--- |
| **Database** | SQLite 3 (`data/supply_chain.db`) | Relational schema with primary keys, foreign key constraints, indexes, and SQL analytical views |
| **Data Ingestion & Scoring** | Python 3.11 (`pandas`, `openpyxl`, `numpy`) | Synthetic generation (50 suppliers, 3,000 orders), SQL ETL, multi-factor scoring engine, and Power BI package generator |
| **Interactive Dashboard** | Dark Premium UI (`#0F1221`) | Single-page intelligence application inspired by enterprise hotel cancellation intelligence reference; 6 tabs, 5 charts, real-time filters, interactive risk calculator |
| **BI Reporting** | Power BI Desktop (`powerbi/`) | 3-sheet structured workbook (`dashboard_data.xlsx`) + DAX measures (`dax_measures.dax` & `DAX_Measures.txt`) |
| **Hosting** | Native Python HTTP Server (`serve_dashboard.py`) | Serves dashboard directly at `http://localhost:8080/dashboard.html` |

---

## 🗄 Relational Schema Specifications

The SQLite database (`C:\dac\data\supply_chain.db`) contains four primary relational tables:

```
suppliers(id, name, category, location, rating)
    │
    └──< purchase_orders(id, supplier_id, order_date, expected_date, qty, cost)
              │
              └──< deliveries(id, order_id, actual_date, status, delivered_qty)
                        │
                        └──< defects(id, delivery_id, defect_qty, type)
```

- **`suppliers` (50 rows):** `id` (PK, `SUP001`–`SUP050`), `name`, `category`, `location`, `rating`
- **`purchase_orders` (3,000 rows):** `id` (PK, `PO10001`–`PO13000`), `supplier_id` (FK), `order_date`, `expected_date`, `qty`, `cost`
- **`deliveries` (3,000 rows):** `id` (PK, `DEL10001`–`DEL13000`), `order_id` (FK), `actual_date`, `status` (`OnTime` / `Late`), `delivered_qty`
- **`defects` (780 rows):** `id` (PK, `DEF10001`–`DEF10780`), `delivery_id` (FK), `defect_qty`, `type`

*Note: Backward-compatible views (`v_suppliers`, `v_purchase_orders`, `v_deliveries`, `v_defects`) provide column aliasing (`supplier_id`, `quantity`, `delivery_status`, `defect_type`).*

---

## 📐 Scoring & Rating Logic

$$\text{OnTimeRate} = \frac{\text{OnTime Deliveries}}{\text{Total Orders}} \times 100$$

$$\text{DefectRate} = \frac{\sum \text{Defect Qty}}{\sum \text{Delivered Qty}} \times 100$$

$$\text{QualityScore} = \max(0, 100 - (\text{DefectRate} \times 10))$$

$$\text{FinalScore} = (\text{OnTimeRate} \times 0.60) + (\text{QualityScore} \times 0.40)$$

### Rating Tiers
- **Grade A (Score $\ge 90$):** 8 Suppliers (16.0%) &rarr; Star Partners. Long-term multi-year contracts.
- **Grade B (Score $75 - 89$):** 30 Suppliers (60.0%) &rarr; Preferred Vendors. Standard volume allocation.
- **Grade C (Score $60 - 74$):** 10 Suppliers (20.0%) &rarr; At-Risk / Caution. Mandatory Corrective Action Plan (CAP).
- **Grade D (Score $< 60$):** 2 Suppliers (4.0%) &rarr; Chronic Failing (SUP012, SUP044). Active dual-sourcing / phase-out.

---

## 💻 12 Comprehensive SQL Analytical Queries (`python/run_sql.py`)

The analytical engine executes 12 advanced queries demonstrating core SQL capabilities:
1. **Global Executive Metrics:** Multi-table joins (`suppliers`, `purchase_orders`, `deliveries`, `defects`) with `CASE` expressions.
2. **Lead Time Buckets vs Late Risk:** `CASE` bucket classification (`0-7d`, `8-30d`, `31-90d`, `91-180d`) with `GROUP BY`.
3. **Category Vulnerability & Defect Rates:** Cross-category comparisons of on-time rate vs defect exposure.
4. **The Defect Paradox:** Analysis of high-spend categories (Electronics absorbs 57% of capital but has highest defect rate: 1.23%).
5. **Monthly Seasonality Trends:** Time-series aggregations using `strftime('%Y-%m')` and CTEs.
6. **Category Supplier Ranking:** Window Function `DENSE_RANK() OVER (PARTITION BY category ORDER BY on_time_rate DESC)`.
7. **Cumulative Spend Concentration:** Window Function `SUM(spend) OVER (ORDER BY spend DESC)` for Grade A suppliers.
8. **Chronic Failing & High-Risk Vendors:** Multi-criteria filtering identifying Grade C & D vendors.
9. **Defect Types Root Cause:** Window share analysis `SUM(defect_qty) * 100.0 / SUM(SUM(defect_qty)) OVER ()`.
10. **Rolling 3-Month Moving Average:** Window Function `AVG(late_rate) OVER (ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`.
11. **Supplier Volume Segmentation:** High / Medium / Low volume tier disparity analysis using CTE and `CASE`.
12. **Lead Time Anomaly Detection:** Window variance `supplier_avg_lead_time - AVG(supplier_avg_lead_time) OVER (PARTITION BY category)`.

---

## 📊 Interactive Web Dashboard (`dashboard/dashboard.html`)

Hosted locally at **`http://localhost:8080/dashboard.html`** with Dark Premium UI (`#0F1221`):
- **5 Hero KPI Stat Cards:** Total Suppliers (50), Total Orders (3,000), Global On-Time Rate (72.0%), Defect Rate (0.96%), Avg Lead Time (42.2d).
- **5 Core Visualizations:**
  1. *Lead Time vs Late Risk:* Combo bar (volume) + line (late risk %).
  2. *Category Vulnerability:* Dual-color bar comparing On-Time % and Defect %.
  3. *The Defect Paradox:* Horizontal bar contrasting Procurement Spend (₹ Cr) vs Defect Units.
  4. *Monthly Seasonality:* 24-Month line trajectory of delivery SLA performance.
  5. *Scorecard Table:* Interactive table with search, category/grade filters, and color-coded grade badges.
- **6 Functional Tabs:**
  - `Executive Overview`
  - `Why Suppliers Fail` (Root cause breakdowns & failing supplier spotlights)
  - `Insights` (Strategic discoveries & CAP governance framework)
  - `Risk Calculator` (Interactive simulator predicting late risk and buffer days)
  - `Revenue Strategy` (Cost of Poor Quality - COPQ & 3-year savings roadmap)
  - `Data Explorer` (Relational tables explorer with instant CSV export)

---

## 📈 Power BI Integration Package (`powerbi/`)

1. **`dashboard_data.xlsx` (EXACT 3 Sheets):**
   - **Sheet 1: `Supplier_Scorecard`** (50 rows: vendor attributes, orders, spend, SLA rates, defect rate, score, grade).
   - **Sheet 2: `Purchase_Orders`** (3,000 rows: order dates, expected dates, actual delivery dates, lead time, status, cost, defect counts).
   - **Sheet 3: `Monthly_Category_Summary`** (92 rows: monthly category aggregations).
2. **`dax_measures.dax` & `DAX_Measures.txt`:**
   - 30 production DAX measures (Total Spend, Global OnTime%, Defect Rate%, Tier Counts, MoM tracking, HEX conditional formatting colors).

---

## 🚀 How to Run

```powershell
# 1. Install dependencies
python -m pip install pandas openpyxl

# 2. Generate raw datasets (50 suppliers, 3000 orders)
python C:\dac\python\generate_data.py

# 3. Create SQLite schema & ingest data
python C:\dac\python\create_db.py

# 4. Compute scorecard metrics & export 3-sheet Excel
python C:\dac\python\scorecard_logic.py

# 5. Execute 12 advanced SQL queries
python C:\dac\python\run_sql.py

# 6. Export dashboard JSON dataset
python C:\dac\python\export_dashboard_json.py

# 7. Start dashboard server
python C:\dac\serve_dashboard.py
# -> Open browser at http://localhost:8080/dashboard.html
```
