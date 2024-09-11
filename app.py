from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
import json
from textblob import TextBlob

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
}

def load_cities():
    """
    Load cities from the cities.json file.
    """
    with open('cities.json', 'r') as file:
        cities_data = json.load(file)
    return [city['City'] for city in cities_data['cities']]

CITIES_LIST = load_cities()

def categorize_by_keywords(text):
    for disaster, keywords in DISASTER_KEYWORDS.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE):
                return disaster
    return 'unknown'

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity < -0.2:
        return 'severe'
    elif polarity < 0.2:
        return 'mild'
    else:
        return 'negligible'

def extract_city_from_text(text):
    """
    Extract city name from the text by matching it against the cities list.
    """
    words = re.findall(r'\b\w+\b', text)
    for word in words:
        if word in CITIES_LIST:
            return word
    return 'unknown'

@app.route('/scrape-disasters', methods=['GET'])
def scrape_disaster_articles():
    def search_articles(api_key, query="disaster", country="in", language="en"):
        url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={query}&country={country}&language={language}"
        response = requests.get(url)
        data = response.json()

        disaster_articles = []
        if data.get('status') == 'success':
            for article in data.get('results', []):
                title = article.get('title', '')
                link = article.get('link', '')
                if re.search(r'emergency|earthquake|flood|hurricane|wildfire|tsunami|landslide|drought|seismic activity', title, re.IGNORECASE):
                    disaster_articles.append({'title': title, 'link': link})
        return disaster_articles

    def scrape_and_classify(article_urls):
        for article in article_urls:
            response = requests.get(article['link'])
            soup = BeautifulSoup(response.text, 'html.parser')

            paragraphs = soup.find_all('p')
            valid_paragraphs = []

            for p in paragraphs:
                text = p.get_text().strip()
                if re.search(r'advertisement|subscribe|related stories|sign up|newsletter|more stories', text, re.IGNORECASE):
                    continue
                valid_paragraphs.append(text)

            full_text = ' '.join(valid_paragraphs) if valid_paragraphs else article['title']

            disaster_type = categorize_by_keywords(full_text + ' ' + article['title'])
            sentiment = analyze_sentiment(full_text)
            location = extract_city_from_text(full_text + ' ' + article['title'])

            summary = valid_paragraphs[0] if valid_paragraphs else 'No summary available'

            article['summary'] = summary
            article['disaster_type'] = disaster_type
            article['sentiment'] = sentiment
            article['location'] = location

    api_key = "pub_5319018a1e56dcf405f9b26c68e7ec6978df0"
    disaster_articles = search_articles(api_key)
    scrape_and_classify(disaster_articles)

    return jsonify(disaster_articles)

if __name__ == '__main__':
    app.run(debug=True)
