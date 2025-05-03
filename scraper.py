import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def scrape_shl_assessments():
    url = "https://www.shl.com/solutions/products/product-catalog/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    assessments = []
    
    # Find all assessment cards (this selector might need adjustment)
    cards = soup.select('.assessment-card')  
    
    for card in cards:
        try:
            name = card.select_one('.assessment-name').text.strip()
            url = "https://www.shl.com" + card.find('a')['href']
            
            # Extract other details (these selectors are hypothetical)
            remote_testing = card.select_one('.remote-testing').text.strip() == 'Yes'
            adaptive = card.select_one('.adaptive').text.strip() == 'Yes'
            duration = card.select_one('.duration').text.strip()
            test_type = card.select_one('.test-type').text.strip()
            
            assessments.append({
                'name': name,
                'url': url,
                'remote_testing': remote_testing,
                'adaptive': adaptive,
                'duration': duration,
                'test_type': test_type,
                'description': f"{name}. {test_type} test. Duration: {duration}. {'Remote testing available.' if remote_testing else ''} {'Adaptive/IRT supported.' if adaptive else ''}"
            })
        except Exception as e:
            print(f"Error processing card: {e}")
            continue
    
    # Save to JSON and CSV
    with open('assessments.json', 'w') as f:
        json.dump(assessments, f)
    
    pd.DataFrame(assessments).to_csv('assessments.csv', index=False)
    return assessments

if __name__ == "__main__":
    assessments = scrape_shl_assessments()
    print(f"Scraped {len(assessments)} assessments")