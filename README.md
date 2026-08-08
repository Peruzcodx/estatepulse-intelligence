# 🏠 EstatePulse Intelligence

### Real Estate Market Intelligence & Property Monitoring Platform

**EstatePulse Intelligence** is a data-driven real estate intelligence platform designed to collect, analyze, monitor, and visualize property-market data.

The platform combines **web scraping, database management, historical market tracking, change detection, data analysis, visualization, and an interactive Streamlit dashboard** into a single system.

> **From property data collection to actionable market intelligence.**

---

## 🚀 Overview

Real estate organizations often have access to large amounts of property information, but collecting, organizing, monitoring, and analyzing that information consistently can be difficult.

EstatePulse Intelligence was developed to address this problem by creating an automated pipeline that transforms property listings into structured market intelligence.

The system can:

* Collect property listing data automatically
* Store structured property information in SQLite
* Create historical snapshots of listings
* Track property price and availability changes
* Analyze market prices and inventory
* Identify active locations and property types
* Generate market reports
* Provide interactive visualizations
* Present market intelligence through a centralized dashboard

The initial implementation focuses on the **Nigerian real estate market**, while the underlying architecture is designed to be adaptable to other real estate markets.

---

# 🎯 Project Objectives

EstatePulse Intelligence was built around four primary objectives:

### 1. Data Collection

Automatically collect structured property information from supported real estate sources.

### 2. Historical Tracking

Preserve market snapshots so that property information can be compared over time.

### 3. Market Intelligence

Transform raw property listings into meaningful statistics, trends, and insights.

### 4. Decision Support

Provide real estate organizations with a centralized platform for monitoring and understanding market activity.

---

# ⚙️ System Architecture

```text
                  PROPERTY DATA SOURCES
                           │
                           ▼
                  ┌─────────────────┐
                  │  Web Scraper    │
                  │   Playwright    │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  Data Cleaning  │
                  │   & Processing  │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │     SQLite      │
                  │    Database     │
                  └────────┬────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
       Current Market   Historical   Change Detector
          Analysis       Analysis
              │            │            │
              └────────────┼────────────┘
                           ▼
                  ┌─────────────────┐
                  │ Market Analytics│
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Streamlit       │
                  │ Dashboard       │
                  └─────────────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
        Market Trends   Reports      Property Explorer
```

---

# 📊 Core Features

## 🏠 Market Overview

The main dashboard provides a high-level view of the property market, including:

* Total properties
* Average property price
* Highest property price
* Active listings
* Property-type distribution
* Location activity
* Price segmentation
* Market value concentration

---

## 📜 Property History

EstatePulse preserves historical property snapshots rather than only storing the latest version of a listing.

Historical analysis can show:

* Average market price
* Highest recorded price
* Lowest recorded price
* Number of snapshots
* Unique properties tracked
* Historical market activity

This allows the platform to move beyond static property listings toward **time-based market analysis**.

---

## 🔍 Change Detector

The Change Detector identifies changes between property snapshots.

It can detect changes such as:

### 💰 Price Changes

Example:

```text
Previous Price: ₦95,000,000
New Price:      ₦110,000,000
```

### 🏷 Availability Changes

Example:

```text
Previous Status: N/A
New Status:      Available
```

This creates an automated mechanism for monitoring changes in property listings.

---

# 📈 Market Trends

The Market Trends module analyzes historical market data and provides:

* Average property price trends
* Market activity over time
* Daily price ranges
* Historical snapshots
* Tracked properties
* Latest average price
* Price movement percentage
* Historical market data tables

The platform uses interactive Plotly visualizations to make market movement easier to understand.

---

# 📑 Market Reports

EstatePulse can generate market intelligence reports based on the property database.

Reports include:

* Property count
* Average price
* Highest price
* Lowest price
* Availability analysis
* Property-type analysis
* Location analysis
* Filtered property data

Users can filter the dataset before generating or downloading reports.

---

# 🔎 Property Explorer

The Property Explorer allows users to search and filter property records using criteria such as:

* Property type
* Search terms
* Price range
* Location
* Availability

This provides a practical way to move from market-level statistics to individual property records.

---

# 🧠 Market Intelligence

EstatePulse transforms raw property records into higher-level insights.

Examples include:

* Most common property type
* Most active location
* Dominant market segment
* Areas with the highest property-value concentration
* Average price movement
* Historical market activity

The goal is not simply to collect property data, but to turn that data into information that can support real estate decision-making.

---

# 🛠️ Technology Stack

| Technology                    | Purpose                              |
| ----------------------------- | ------------------------------------ |
| **Python**                    | Core programming language            |
| **Playwright**                | Web scraping and browser automation  |
| **SQLite**                    | Property and historical data storage |
| **Pandas**                    | Data processing and analysis         |
| **Plotly**                    | Interactive market visualizations    |
| **Streamlit**                 | Interactive dashboard                |
| **Git**                       | Version control                      |
| **GitHub**                    | Source-code hosting                  |
| **Streamlit Community Cloud** | Application deployment               |

---

# 📁 Project Structure

```text
estatepulse-intelligence/
│
├── analysis/
│   ├── change_detector.py
│   ├── current_market.py
│   ├── data_cleaning.py
│   ├── history_analysis.py
│   ├── market_analysis.py
│   └── price_tracker.py
│
├── dashboard/
│   ├── Home.py
│   ├── assets/
│   │   └── logo.png
│   └── views/
│       ├── dashboard_view.py
│       ├── history_view.py
│       ├── change_view.py
│       ├── market_view.py
│       └── reports_view.py
│
├── database/
│   ├── database.py
│   ├── history.py
│   ├── models.py
│   └── save_data.py
│
├── reports/
│   └── market_summary.py
│
├── scraper/
│   └── scraper.py
│
├── visualization/
│   └── charts.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🔄 Data Pipeline

EstatePulse follows a continuous data pipeline:

```text
Collect
   ↓
Clean
   ↓
Store
   ↓
Snapshot
   ↓
Compare
   ↓
Analyze
   ↓
Visualize
   ↓
Report
```

A major part of the system is the distinction between **current property data** and **historical snapshots**.

When the scraper runs again, existing properties can be compared against newly collected information, allowing EstatePulse to identify changes rather than simply replacing old records.

---

# 🗄️ Historical Data Model

Historical snapshots make it possible to answer questions such as:

* Has a property's price changed?
* Has its availability changed?
* How has the average market price moved?
* How active was the market on a particular date?
* Which properties have been tracked over time?
* Which locations are accumulating the greatest property value?

This historical layer is one of the foundations of EstatePulse's market-intelligence functionality.

---

# 💻 Local Installation

Clone the repository:

```bash
git clone https://github.com/Peruzcodx/estatepulse-intelligence.git
```

Navigate into the project:

```bash
cd estatepulse-intelligence
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Dashboard

From the project root:

```bash
py -m streamlit run dashboard/Home.py
```

The application will then be available through the local Streamlit server.

---

# 🕷️ Running the Scraper

From the project root:

```bash
py scraper/scraper.py
```

The scraper collects supported property information and stores it in the EstatePulse database.

Repeated scraper runs allow the system to build historical market data and detect changes over time.

---

# ☁️ Deployment

The EstatePulse dashboard is deployed using **Streamlit Community Cloud** and the source code is maintained through GitHub.

Live application:

**https://estatepulse-intelligence.streamlit.app/**

Repository:

**https://github.com/Peruzcodx/estatepulse-intelligence**

---

# 🏢 Potential Real Estate Applications

EstatePulse can potentially support real estate organizations with:

* Property market monitoring
* Competitor listing monitoring
* Price monitoring
* Inventory tracking
* Market research
* Location analysis
* Historical market analysis
* Property intelligence
* Automated reporting
* Data-driven decision support

The platform can also be adapted to different property markets and data sources depending on organizational requirements.

---

# 🌍 Scalability

Although the initial implementation uses the Nigerian real estate market as its primary use case, EstatePulse is not fundamentally restricted to Nigeria.

The architecture can be extended to support:

* Additional cities
* Additional regions
* Additional countries
* Multiple property sources
* Different property categories
* Additional market indicators
* Larger databases
* Automated scheduled collection

The long-term objective is to evolve EstatePulse into a broader **real estate intelligence and monitoring system**.

---

# 🗺️ Future Roadmap

Potential future improvements include:

* [ ] Automated scheduled scraping
* [ ] Multi-source property aggregation
* [ ] Advanced price forecasting
* [ ] Interactive location maps
* [ ] Geographic market comparisons
* [ ] Email market alerts
* [ ] Automated weekly/monthly reports
* [ ] More advanced competitor monitoring
* [ ] Cloud database integration
* [ ] User authentication and role management
* [ ] Multi-country market support
* [ ] Advanced market prediction models

---

# ⚠️ Data & Responsible Use

EstatePulse is intended for legitimate market research, analytics, monitoring, and decision-support use.

Data collection should respect:

* Website terms of service
* Applicable laws and regulations
* Robots.txt and access restrictions where relevant
* Rate limits
* Privacy requirements
* Intellectual property rights

The platform should only be used with data sources that permit the intended form of collection and use.

---

# 👨‍💻 Author

**Peruzcodx**

Python Developer | Automation & Data Engineering

📧 **[yeyebusiness123@gmail.com](mailto:yeyebusiness123@gmail.com)**

📱 **+234 815 492 7439**

---

# ⭐ Project Status

**EstatePulse Intelligence is an actively developed real estate market intelligence project.**

The current version includes a working scraping pipeline, SQLite data storage, historical snapshot tracking, change detection, market analytics, reporting functionality, interactive visualizations, and a deployed Streamlit dashboard.

---

## 📌 Built with Python

EstatePulse Intelligence demonstrates how web automation, structured data collection, database systems, analytics, and visualization can be combined to create a practical data-driven application.

**Collect the data.
Track the changes.
Understand the market.**
