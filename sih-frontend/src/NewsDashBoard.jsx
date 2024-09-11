import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './DisasterNews.css'; 

const NewsDashBoard = () => {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/scrape-disasters') // Flask API endpoint
      .then(response => {
        setArticles(response.data);
      })
      .catch(error => console.error('Error fetching articles:', error));
  }, []);

  return (
    <div className="container1">
      <h1>Disaster Related News</h1>
      {articles.length > 0 ? (
        articles.map((article, index) => (
          <div key={index} className="news-card">
            <h2>{article.title}</h2>
            <p>{article.summary || 'No summary available.'}</p>
            <p><strong>Disaster Type:</strong> {article.disaster_type || 'Unknown'}</p> {/* Display disaster type */}
            <a href={article.link} target="_blank" rel="noopener noreferrer">Read more</a>
          </div>
        ))
      ) : (
        <p>No articles available</p>
      )}
    </div>
  );
};

export default NewsDashBoard;
