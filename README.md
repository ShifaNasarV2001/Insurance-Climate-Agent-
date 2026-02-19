# 🌍 Insurance Climate Risk Analysis Agent

## 📌 Overview

The **Insurance Climate Risk Analysis Agent** is a Gen-AI powered system designed to fetch, analyze, and assess climate-related risks impacting the insurance industry.

This agent scrapes real-time news, evaluates climate risks, identifies affected insurance sectors, and provides insights into financial, operational, regulatory, and reputational impacts.

It helps insurers, analysts, and researchers monitor emerging climate threats and understand their potential industry impact.

---

## 🚀 Features

### 🔎 Web Scraping

* Extracts climate and insurance-related news from multiple sources
* Fetches real-time articles using News APIs

### ⚠️ Risk Assessment

* Uses NLP and Gen-AI to classify risk levels:

  * **HIGH**
  * **MEDIUM**
  * **LOW**

### 🏢 Sector Identification

Identifies affected insurance sectors such as:

* Property Insurance
* Agriculture Insurance
* Marine Insurance
* Life & Health Insurance

### 📊 Impact Analysis

Analyzes different impact dimensions:

* Financial impact
* Operational impact
* Regulatory impact
* Reputational impact

### 💾 Data Storage

* Saves analyzed results in structured **JSON format**
* Enables further analytics and reporting

---

## 🛠 Installation

### Prerequisites

Ensure you have installed:

* Python **3.8+**
* pip package manager

### Clone the Repository

```bash
git clone https://github.com/ShifaNasarV2001/Insurance-Climate-Agent-.git
cd Insurance-Climate-Agent-
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set Up API Keys

Create a `.env` file in the project root and add:

```env
NEWSAPI_KEY=your_api_key_here
```

---

## ▶️ Usage

Run the agent:

```bash
python insurance_climate_agent.py
```

---

## 📤 Output

### Console Output

* Displays categorized climate risk assessments
* Shows affected insurance sectors and impact levels

### JSON Output

* Saves structured analysis to:

```
insurance_climate_analysis.json
```

Includes:

* Article title
* Risk level
* Affected sector
* Impact analysis
* Summary insights

---

## 📈 Use Cases

* Climate risk monitoring for insurers
* Insurance market research
* Regulatory and compliance tracking
* Financial risk assessment
* ESG and sustainability analysis

---

## 🔮 Future Enhancements

* Dashboard visualization (Streamlit/React)
* Vector database for semantic search
* Historical risk trend analysis
* Multi-agent workflow integration
* Real-time alerts for high-risk news

---

