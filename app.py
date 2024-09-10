from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
CORS(app)

# Disaster keywords for classification
DISASTER_KEYWORDS = {
    'earthquake': ['earthquake', 'seismic activity', 'richter', 'fault line', 'aftershock', 'tremor'],
    'flood': ['flood', 'flooding', 'flash flood', 'overflow', 'water level', 'riverbank'],
    'landslide': ['landslide', 'mudslide', 'avalanche', 'debris flow', 'rockfall', 'erosion'],
    'hurricane': ['hurricane', 'typhoon', 'cyclone', 'storm surge', 'windstorm', 'tropical storm'],
    'wildfire': ['wildfire', 'forest fire', 'bushfire', 'firestorm', 'burn', 'blaze'],
    'tsunami': ['tsunami', 'tidal wave', 'seismic sea wave'],
    'drought': ['drought', 'dry spell', 'water shortage', 'arid', 'desertification'],
    # Add more categories and keywords as needed
}

def categorize_by_keywords(text):
    """
    Categorizes the text based on the presence of disaster-related keywords.
    Returns the disaster type if keywords match, otherwise returns 'unknown'.
    """
    for disaster, keywords in DISASTER_KEYWORDS.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE):
                return disaster
    return 'unknown'  # Default if no keywords are found

@app.route('/scrape-disasters', methods=['GET'])
def scrape_disaster_articles():
    def search_articles(api_key, query="disaster"):
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
        urli = f"https://newsapi.org/v2/everything?q={query}&sources=google-news-in&apiKey=e9746f8506ac4abaa3c846424ae5ad97"
        urlo = f"https://newsapi.org/v2/everything?q={query}&country=in&apiKey={api_key}&language=en"
        response = requests.get(urlo)
        data = response.json()

        disaster_articles = []
        if data.get('status') == 'ok':
            for article in data['articles']:
                title = article['title']
                link = article['url']
                # Match titles with potential disaster keywords
                if re.search(r'emergency|earthquake|flood|hurricane|wildfire|tsunami|landslide|drought|seismic activity', title, re.IGNORECASE) and not re.search(r'consent\.yahoo\.com', link):
                    disaster_articles.append({'title': title, 'link': link})
        return disaster_articles

    # Function to extract textual content from the HTML and classify disaster type
    def scrape_and_classify(article_urls):
        for article in article_urls:
            response = requests.get(article['link'])
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the textual content from the HTML
            paragraphs = soup.find_all('p')
            full_text = ' '.join([p.text for p in paragraphs])

            if not full_text:  # Fallback if no paragraphs are found
                full_text = article['title']

            # Try to classify the disaster type using keyword matching
            disaster_type = categorize_by_keywords(full_text)

            # Add the summary (first two paragraphs) and disaster type to the article
            summary = ' '.join([p.text for p in paragraphs[:2]]) if paragraphs else 'No summary available'
            article['summary'] = summary
            article['disaster_type'] = disaster_type

    api_key = "e9746f8506ac4abaa3c846424ae5ad97"
    disaster_articles = search_articles(api_key)
    scrape_and_classify(disaster_articles)

    return jsonify(disaster_articles)

if __name__ == '__main__':
    app.run(debug=True)
