# Insurance-Climate-Agent-

Insurance Climate Risk Analysis Agent

#Overview

This project is a Gen-AI powered agent designed to fetch, analyze, and assess climate-related risks impacting the insurance industry. The agent scrapes real-time news, assesses risk levels, identifies affected insurance sectors, and provides insights into financial, operational, and regulatory impacts.

Features

Web Scraping: Extracts climate and insurance-related news from multiple sources.

Risk Assessment: Evaluates articles using natural language processing (NLP) to classify risk levels (HIGH, MEDIUM, LOW).

Sector Identification: Determines which insurance sectors (e.g., Property, Agriculture, Marine) are affected.

Impact Analysis: Analyzes financial, operational, regulatory, and reputational impacts.

Data Storage: Saves results in a structured JSON file.

Installation

Prerequisites

Ensure you have Python 3.8+ installed.

Clone the Repository

 git clone https://github.com/ShifaNasarV2001/Insurance-Climate-Agent-.git
 cd your-repository

Install Dependencies

pip install -r requirements.txt

Set Up API Keys

Create a .env file in the project root and add your News API key:

NEWSAPI_KEY=your_api_key_here

Usage

Run the script to fetch and analyze climate risk news:

python insurance_climate_agent.py

Output

Console: Displays categorized risk assessments with affected sectors.

JSON File: Saves the structured output to insurance_climate_analysis.json.

Project Structure

├── insurance_climate_agent.py  # Main script
├── requirements.txt            # Dependencies
├── .env                        # API key storage
├── README.md                   # Project documentation

Future Enhancements

Machine Learning Integration for advanced risk prediction.

Interactive Streamlit Dashboard for visualization.

Expanded Data Sources beyond NewsAPI.

