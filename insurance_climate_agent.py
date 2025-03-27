import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
from collections import defaultdict
from dotenv import load_dotenv
import json
from typing import Dict, List

# Load API key from .env file
load_dotenv()
NEWS_API_KEY = os.getenv('NEWSAPI_KEY')

class InsuranceClimateAgent:
    def __init__(self):
        self.risk_levels = {
            'HIGH': 3,
            'MEDIUM': 2,
            'LOW': 1
        }
        
        self.insurance_sectors = {
            'Property': ['property damage', 'real estate', 'building', 'infrastructure', 'commercial property'],
            'Agriculture': ['crop', 'farming', 'agricultural', 'livestock', 'food production'],
            'Marine': ['shipping', 'port', 'marine', 'coastal', 'ocean', 'sea level'],
            'Energy': ['power plant', 'renewable energy', 'oil', 'gas', 'energy infrastructure'],
            'Health': ['health impact', 'disease', 'medical', 'healthcare', 'heat stress'],
            'Business': ['business interruption', 'supply chain', 'operational risk', 'commercial']
        }

    def clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text:
            return ""
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def get_article_content(self, url: str) -> str:
        """Get full content from article URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for tag in ['script', 'style', 'nav', 'header', 'footer', 'aside']:
                for element in soup.find_all(tag):
                    element.decompose()
            
            content = soup.find('article') or soup.find('main') or soup.find('body')
            return self.clean_text(content.get_text()) if content else ""
        except Exception as e:
            print(f"Error scraping content: {str(e)}")
            return ""

    def assess_risk_level(self, text: str) -> Dict:
        """Enhanced risk level assessment with sentiment and numerical analysis"""
        text = text.lower()
        
        # Enhanced risk indicators with weights
        risk_indicators = {
            'HIGH': {
                'keywords': ['severe', 'catastrophic', 'extreme', 'critical', 'urgent'],
                'weight': 3,
                'numerical_indicators': ['million', 'billion', 'thousands', 'massive', 'huge'],
                'temporal_indicators': ['immediate', 'urgent', 'now', 'critical']
            },
            'MEDIUM': {
                'keywords': ['moderate', 'potential', 'concerning', 'challenge'],
                'weight': 2,
                'numerical_indicators': ['hundreds', 'significant', 'substantial'],
                'temporal_indicators': ['ongoing', 'developing', 'growing']
            },
            'LOW': {
                'keywords': ['minor', 'minimal', 'small', 'limited'],
                'weight': 1,
                'numerical_indicators': ['small', 'minor', 'limited'],
                'temporal_indicators': ['future', 'potential', 'long-term']
            }
        }
        
        risk_scores = {level: 0 for level in risk_indicators.keys()}
        
        for level, indicators in risk_indicators.items():
            # Keyword matching
            keyword_score = sum(1 for keyword in indicators['keywords'] if keyword in text)
            
            # Numerical indicator matching
            numerical_score = sum(1 for indicator in indicators['numerical_indicators'] if indicator in text)
            
            # Temporal context matching
            temporal_score = sum(1 for indicator in indicators['temporal_indicators'] if indicator in text)
            
            # Calculate weighted score
            risk_scores[level] = (
                keyword_score * indicators['weight'] +
                numerical_score * (indicators['weight'] * 1.5) +
                temporal_score * (indicators['weight'] * 0.8)
            )
        
        # Determine overall risk level with confidence score
        max_score = max(risk_scores.values())
        total_score = sum(risk_scores.values())
        
        if max_score == 0:
            return {'level': 'UNDEFINED', 'score': 0, 'confidence': 0, 'details': risk_scores}
        
        risk_level = max(risk_scores.items(), key=lambda x: x[1])[0]
        confidence = max_score / total_score if total_score > 0 else 0
        
        return {
            'level': risk_level,
            'score': self.risk_levels[risk_level],
            'confidence': confidence,
            'details': risk_scores
        }

    def identify_affected_sectors(self, text: str) -> List[str]:
        """Identify insurance sectors affected by the risk"""
        text = text.lower()
        affected_sectors = []
        
        for sector, keywords in self.insurance_sectors.items():
            if any(keyword in text for keyword in keywords):
                affected_sectors.append(sector)
        
        return affected_sectors

    def analyze_impact(self, text: str) -> Dict:
        """Analyze potential impact on insurance business"""
        text = text.lower()
        
        impact_areas = {
            'Financial': [
                'loss', 'cost', 'premium', 'payment', 'claim', 'financial',
                'revenue', 'profit', 'market', 'investment'
            ],
            'Operational': [
                'operation', 'process', 'service', 'business interruption',
                'workflow', 'management', 'infrastructure'
            ],
            'Regulatory': [
                'regulation', 'compliance', 'policy', 'requirement', 'law',
                'standard', 'guideline', 'framework'
            ],
            'Reputational': [
                'reputation', 'brand', 'customer', 'public', 'trust',
                'confidence', 'relationship'
            ]
        }
        
        impacts = {}
        for area, keywords in impact_areas.items():
            matches = sum(1 for keyword in keywords if keyword in text)
            impacts[area] = {
                'level': 'HIGH' if matches >= 3 else 'MEDIUM' if matches >= 1 else 'LOW',
                'matches': matches
            }
        
        return impacts

    def get_insurance_climate_news(self) -> Dict:
        """Fetch and analyze climate news relevant to insurance"""
        base_url = "https://newsapi.org/v2/everything"
        
        # Get news from last 7 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        # Search parameters focused on insurance and climate risk
        params = {
            'apiKey': NEWS_API_KEY,
            'q': '(climate risk OR climate change OR natural disaster) AND (insurance OR reinsurance OR risk assessment)',
            'language': 'en',
            'from': start_date.strftime('%Y-%m-%d'),
            'to': end_date.strftime('%Y-%m-%d'),
            'sortBy': 'relevancy',
            'pageSize': 100
        }
        
        try:
            print("Fetching insurance-relevant climate news...")
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            news_data = response.json()
            
            if news_data.get('status') != 'ok':
                print(f"Error from NewsAPI: {news_data.get('message', 'Unknown error')}")
                return {}
            
            articles = news_data.get('articles', [])
            print(f"Found {len(articles)} articles")
            
            analyzed_articles = []
            processed_urls = set()
            
            for article in articles:
                if article['url'] in processed_urls:
                    continue
                
                # Get and combine all available content
                content = article.get('content', '') or article.get('description', '')
                full_content = self.get_article_content(article['url'])
                if full_content:
                    content = f"{content} {full_content}"
                
                # Analyze the content
                risk_assessment = self.assess_risk_level(content)
                affected_sectors = self.identify_affected_sectors(content)
                impact_analysis = self.analyze_impact(content)
                
                # Only include articles with clear insurance relevance
                if affected_sectors or risk_assessment['level'] != 'UNDEFINED':
                    analyzed_article = {
                        'title': article['title'],
                        'source': article['source']['name'],
                        'url': article['url'],
                        'date': article['publishedAt'],
                        'risk_assessment': risk_assessment,
                        'affected_sectors': affected_sectors,
                        'impact_analysis': impact_analysis,
                        'preview': self.clean_text(content)[:300] + "..."
                    }
                    analyzed_articles.append(analyzed_article)
                
                processed_urls.add(article['url'])
            
            # Group articles by risk level
            risk_categorized = defaultdict(list)
            for article in analyzed_articles:
                risk_level = article['risk_assessment']['level']
                risk_categorized[risk_level].append(article)
            
            # Print analysis results
            print("\nInsurance Climate Risk Analysis:")
            print("=" * 80)
            
            for risk_level in ['HIGH', 'MEDIUM', 'LOW', 'UNDEFINED']:
                if risk_level in risk_categorized:
                    articles = risk_categorized[risk_level]
                    print(f"\nRISK LEVEL: {risk_level}")
                    print(f"Found {len(articles)} articles\n")
                    
                    for i, article in enumerate(articles, 1):
                        print(f"{i}. {article['title']}")
                        print(f"Source: {article['source']}")
                        print(f"Date: {article['date']}")
                        print(f"Risk Score: {article['risk_assessment']['score']}")
                        print(f"Affected Sectors: {', '.join(article['affected_sectors'])}")
                        print("\nImpact Analysis:")
                        for area, impact in article['impact_analysis'].items():
                            print(f"- {area}: {impact['level']} (matches: {impact['matches']})")
                        print(f"\nURL: {article['url']}")
                        print(f"Preview: {article['preview']}")
                        print("-" * 80 + "\n")
            
            return dict(risk_categorized)
                
        except Exception as e:
            print(f"Error analyzing news: {str(e)}")
            return {}

    def save_analysis(self, analysis: Dict, filename: str = "insurance_climate_analysis.json"):
        """Save the analysis results to a JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(analysis, f, indent=2)
            print(f"\nAnalysis saved to {filename}")
        except Exception as e:
            print(f"Error saving analysis: {str(e)}")

def main():
    agent = InsuranceClimateAgent()
    analysis = agent.get_insurance_climate_news()
    agent.save_analysis(analysis)

if __name__ == "__main__":
    main() 