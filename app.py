#make sure to display that the news articles are relevant disaster related information from the last 48 hours
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
    def search_articles(api_key, query="disaster", country="in", language="en"):
        url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={query}&country={country}&language={language}"
        response = requests.get(url)
        data = response.json()

        disaster_articles = []
        if data.get('status') == 'success':
            for article in data.get('results', []):
                title = article.get('title', '')
                link = article.get('link', '')
                # Match titles with potential disaster keywords
                if re.search(r'emergency|earthquake|flood|hurricane|wildfire|tsunami|landslide|drought|seismic activity', title, re.IGNORECASE):
                    disaster_articles.append({'title': title, 'link': link})
        return disaster_articles

    # Function to extract textual content from the HTML and classify disaster type
    def scrape_and_classify(article_urls):
        for article in article_urls:
            response = requests.get(article['link'])
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the textual content from the HTML
            paragraphs = soup.find_all('p')
            valid_paragraphs = []
            
            # Filter out irrelevant paragraphs (ads, sidebars, etc.)
            for p in paragraphs:
                text = p.get_text().strip()
                # Skip paragraphs with ads or unrelated content (commonly found patterns)
                if re.search(r'advertisement|subscribe|related stories|sign up|newsletter|more stories', text, re.IGNORECASE):
                    continue
                valid_paragraphs.append(text)

            # Join valid paragraphs as the full article text
            full_text = ' '.join(valid_paragraphs)

            if not full_text:  # Fallback if no paragraphs are found
                full_text = article['title']

            # Try to classify the disaster type using keyword matching
            disaster_type = categorize_by_keywords(full_text)

            # Add the summary (first two paragraphs with disaster-related keywords) and disaster type to the article
            summary = None
            for paragraph in valid_paragraphs:
                if any(re.search(r'\b' + re.escape(keyword) + r'\b', paragraph, re.IGNORECASE) for keyword_list in DISASTER_KEYWORDS.values() for keyword in keyword_list):
                    if summary is None:
                        summary = paragraph  # First valid paragraph with a keyword
                    else:
                        summary += ' ' + paragraph  # Add second valid paragraph
                    if summary.count(' ') > 30:  # Limit summary length to around two sentences
                        break

            # If no summary could be extracted, default to 'no summary available'
            if not summary:
                summary = 'No summary available'

            article['summary'] = summary
            article['disaster_type'] = disaster_type

    api_key = "pub_5319018a1e56dcf405f9b26c68e7ec6978df0"
    disaster_articles = search_articles(api_key)
    scrape_and_classify(disaster_articles)

    return jsonify(disaster_articles)

if __name__ == '__main__':
    app.run(debug=True)
