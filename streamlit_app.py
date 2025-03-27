
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from insurance_climate_agent import InsuranceClimateAgent
import pandas as pd
from datetime import datetime
from collections import defaultdict

# Set page config
st.set_page_config(
    page_title="Insurance Climate Risk Analyzer",
    page_icon="🌍",
    layout="wide"
)

# Custom CSS for a modern, sleek look
st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f7f9fc;
    }
    .risk-high { color: #ff4b4b; font-weight: bold; }
    .risk-medium { color: #ffa600; font-weight: bold; }
    .risk-low { color: #2ac769; font-weight: bold; }
    .risk-undefined { color: #808495; font-weight: bold; }
    .metric-card {
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        text-align: center;
        background: linear-gradient(135deg, #ffffff, #f0f3f5);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .header-style {
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 15px;
        color: #333333;
    }
    .article-card {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        padding: 15px;
        margin: 10px 0;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Create a pie chart for risk distribution
def create_risk_distribution_chart(analysis):
    """Create a pie chart showing risk level distribution"""
    risk_counts = {
        'High Risk': len(analysis.get('HIGH', [])),
        'Medium Risk': len(analysis.get('MEDIUM', [])),
        'Low Risk': len(analysis.get('LOW', [])),
        'Undefined': len(analysis.get('UNDEFINED', []))
    }

    colors = ['#ff4b4b', '#ffa600', '#2ac769', '#808495']

    fig = go.Figure(data=[go.Pie(
        labels=list(risk_counts.keys()),
        values=list(risk_counts.values()),
        hole=.35,
        marker=dict(colors=colors, line=dict(color='#fff', width=2))
    )])

    fig.update_layout(
        title="Risk Level Distribution",
        showlegend=True,
        height=400
    )

    return fig

# Create a bar chart for sector impact frequency
def create_sector_impact_chart(analysis):
    """Create a bar chart showing sector impact frequency"""
    sector_counts = defaultdict(int)
    total_articles = sum(len(articles) for articles in analysis.values())

    for risk_level, articles in analysis.items():
        for article in articles:
            for sector in article['affected_sectors']:
                sector_counts[sector] += 1

    if total_articles > 0:
        sector_data = {
            'Sector': list(sector_counts.keys()),
            'Impact Frequency (%)': [count / total_articles * 100 for count in sector_counts.values()]
        }

        df = pd.DataFrame(sector_data)
        fig = px.bar(
            df,
            x='Sector',
            y='Impact Frequency (%)',
            title='Sector Impact Analysis',
            color='Impact Frequency (%)',
            color_continuous_scale=['#2ac769', '#ffa600', '#ff4b4b']
        )

        fig.update_layout(
            xaxis_title="Sector",
            yaxis_title="Impact Frequency (%)",
            height=400
        )

        return fig
    return None

# Create a heatmap for impact analysis
def create_impact_heatmap(analysis):
    """Create a heatmap of impact areas across risk levels"""
    impact_data = {
        'Financial': {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0},
        'Operational': {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0},
        'Regulatory': {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0},
        'Reputational': {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
    }

    for risk_level, articles in analysis.items():
        for article in articles:
            for area, impact in article['impact_analysis'].items():
                impact_data[area][impact['level']] += 1

    x_labels = ['HIGH', 'MEDIUM', 'LOW']
    y_labels = list(impact_data.keys())
    z_values = [[impact_data[area][level] for level in x_labels] for area in y_labels]

    fig = go.Figure(data=go.Heatmap(
        z=z_values,
        x=x_labels,
        y=y_labels,
        colorscale=['#2ac769', '#ffa600', '#ff4b4b'],
        hoverongaps=False
    ))

    fig.update_layout(
        title="Impact Analysis Heatmap",
        xaxis_title="Impact Level",
        yaxis_title="Impact Area",
        height=400
    )

    return fig

# Display article in card format
def display_article_card(article):
    """Display an article in a card format"""
    risk_color = {
        'HIGH': 'risk-high',
        'MEDIUM': 'risk-medium',
        'LOW': 'risk-low',
        'UNDEFINED': 'risk-undefined'
    }

    st.markdown(f"""
        <div class="article-card">
            <h4>{article['title']}</h4>
            <p><strong>Source:</strong> {article['source']} | <strong>Date:</strong> {article['date']}</p>
            <p><strong>Risk Level:</strong> <span class="{risk_color[article['risk_assessment']['level']]}">{article['risk_assessment']['level']}</span></p>
            <p><strong>Affected Sectors:</strong> {', '.join(article['affected_sectors'])}</p>
            <p><strong>Impact Analysis:</strong></p>
            <ul>
                {''.join([f"<li>{area}: {impact['level']} (matches: {impact['matches']})</li>" for area, impact in article['impact_analysis'].items()])}
            </ul>
            <p><a href="{article['url']}" target="_blank">Read full article</a></p>
        </div>
    """, unsafe_allow_html=True)

#  application
def main():
    st.title("🌍 Insurance Climate Risk Analyzer")

    # Sidebar for controls
    st.sidebar.header("🔍 Filters & Controls")
    auto_refresh = st.sidebar.checkbox("Auto-refresh data", value=False)
    if auto_refresh:
        st.sidebar.info("Data will refresh every 30 minutes")

    risk_filters = st.sidebar.multiselect(
        "Filter by Risk Level",
        ["HIGH", "MEDIUM", "LOW", "UNDEFINED"],
        default=["HIGH", "MEDIUM", "LOW"]
    )

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🌐 Real-time Climate Risk Analysis")
        with st.spinner("Fetching and analyzing climate news..."):
            agent = InsuranceClimateAgent()
            analysis = agent.get_insurance_climate_news()

    if analysis:
        # Overview metrics
        total_articles = sum(len(articles) for articles in analysis.values())
        high_risk = len(analysis.get('HIGH', []))

        metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)

        with metrics_col1:
            st.metric("📚 Total Articles", total_articles)
        with metrics_col2:
            st.metric("🚨 High Risk Articles", high_risk)
        with metrics_col3:
            st.metric("📅 Coverage Period", "Last 7 days")
        with metrics_col4:
            st.metric("⏰ Last Updated", datetime.now().strftime("%Y-%m-%d %H:%M"))

        # Visualizations
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.plotly_chart(create_risk_distribution_chart(analysis), use_container_width=True)
            st.plotly_chart(create_impact_heatmap(analysis), use_container_width=True)

        with chart_col2:
            sector_chart = create_sector_impact_chart(analysis)
            if sector_chart:
                st.plotly_chart(sector_chart, use_container_width=True)

        # Articles by risk level
        st.markdown("### 📢 Detailed Analysis by Risk Level")

        for risk_level in risk_filters:
            if risk_level in analysis and analysis[risk_level]:
                st.markdown(f"<div class='header-style'>{risk_level} Risk Articles ({len(analysis[risk_level])})</div>", unsafe_allow_html=True)
                for article in analysis[risk_level]:
                    display_article_card(article)
    else:
        st.error("⚠️ No data available. Please check your API key and internet connection.")

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>Powered by NewsAPI and Climate Risk Analysis Engine | © 2025</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
