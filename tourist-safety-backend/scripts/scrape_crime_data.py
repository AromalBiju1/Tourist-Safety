"""
Data Scraper for Crime Statistics
Demonstrates how to scrape crime data from various sources
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import json
import time


class CrimeDataScraper:
    """
    Scraper for collecting crime data from public sources
    Note: Respect robots.txt and rate limits when scraping
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def scrape_ncrb_data(self) -> List[Dict]:
        """
        Scrape crime data from NCRB (National Crime Records Bureau)
        Note: NCRB provides PDF reports, so this is a placeholder
        for demonstration. In practice, use their API or parse PDFs.
        """
        # NCRB Data API endpoint (if available)
        # url = "https://data.gov.in/resource/..."
        
        # For now, return sample structure
        print("📊 NCRB scraping would be implemented here")
        print("   - Visit: https://ncrb.gov.in")
        print("   - Download: Crime in India reports")
        print("   - Parse: PDF/Excel files")
        
        return []
    
    def scrape_state_police(self, state: str) -> Optional[Dict]:
        """
        Scrape crime statistics from state police websites
        Each state has different website structure
        """
        state_police_urls = {
            "Delhi": "https://delhipolice.gov.in",
            "Maharashtra": "https://mahapolice.gov.in",
            "Karnataka": "https://ksp.gov.in",
            "Tamil Nadu": "https://tnpolice.gov.in",
            "Kerala": "https://keralapolice.gov.in",
            "Gujarat": "https://police.gujarat.gov.in",
            "Rajasthan": "https://police.rajasthan.gov.in",
        }
        
        url = state_police_urls.get(state)
        if not url:
            print(f"⚠️ No URL configured for {state}")
            return None
        
        try:
            print(f"🔍 Would scrape: {url}")
            # Actual scraping would be:
            # response = self.session.get(url, timeout=30)
            # soup = BeautifulSoup(response.text, 'lxml')
            # Extract crime statistics tables
            
            return {
                "state": state,
                "source": url,
                "note": "Implement specific parser for this state"
            }
            
        except Exception as e:
            print(f"❌ Error scraping {state}: {e}")
            return None
    
    def scrape_open_data_india(self) -> List[Dict]:
        """
        Scrape crime data from data.gov.in open data portal
        """
        base_url = "https://data.gov.in/resource"
        
        # Example catalog IDs for crime data
        catalogs = [
            "crime-india-2021-ipc-crimes-city-wise",
            "district-wise-crimes-committed-against-women",
            "crime-head-wise-crime-data",
        ]
        
        print("📂 Open Data India resources:")
        for catalog in catalogs:
            print(f"   - {base_url}/{catalog}")
        
        # In practice:
        # 1. Register for API key at data.gov.in
        # 2. Use their API to fetch data
        # 3. Parse JSON/CSV response
        
        return []
    
    def parse_crime_table(self, html: str) -> List[Dict]:
        """
        Generic parser for crime statistics table
        """
        soup = BeautifulSoup(html, 'lxml')
        tables = soup.find_all('table')
        
        data = []
        for table in tables:
            rows = table.find_all('tr')
            headers = [th.get_text(strip=True) for th in rows[0].find_all(['th', 'td'])]
            
            for row in rows[1:]:
                cols = [td.get_text(strip=True) for td in row.find_all('td')]
                if cols:
                    data.append(dict(zip(headers, cols)))
        
        return data
    
    def save_to_json(self, data: List[Dict], filename: str):
        """Save scraped data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved to {filename}")


class OpenCityScraper:
    """
    Scraper for OpenCity urban data platform
    https://opencity.in
    """
    
    def __init__(self):
        self.base_url = "https://opencity.in"
        self.session = requests.Session()
    
    def get_crime_datasets(self) -> List[Dict]:
        """List available crime datasets"""
        # OpenCity provides API access
        # You would need to check their API documentation
        
        datasets = [
            {
                "name": "Crime in India - 2023 - IPC Crimes (City-wise)",
                "years": "2021-2023",
                "source": "NCRB"
            },
            {
                "name": "Crime Against Women - State-wise",
                "years": "2018-2022",
                "source": "NCRB"
            }
        ]
        
        return datasets


def demo_scraping():
    """Demonstrate scraping capabilities"""
    print("=" * 50)
    print("🕷️ Crime Data Scraping Demo")
    print("=" * 50)
    print()
    
    scraper = CrimeDataScraper()
    
    # Show available sources
    print("📌 Available Data Sources:")
    print()
    
    print("1. NCRB (National Crime Records Bureau)")
    scraper.scrape_ncrb_data()
    print()
    
    print("2. State Police Websites")
    for state in ["Delhi", "Maharashtra", "Karnataka"]:
        scraper.scrape_state_police(state)
    print()
    
    print("3. Open Data India")
    scraper.scrape_open_data_india()
    print()
    
    print("4. OpenCity Platform")
    oc = OpenCityScraper()
    datasets = oc.get_crime_datasets()
    for ds in datasets:
        print(f"   📊 {ds['name']} ({ds['years']})")
    
    print()
    print("=" * 50)
    print("💡 To implement actual scraping:")
    print("   1. Check each website's robots.txt")
    print("   2. Implement rate limiting (1 req/sec)")
    print("   3. Parse HTML tables or use APIs")
    print("   4. Save to database")
    print("=" * 50)


if __name__ == "__main__":
    demo_scraping()
