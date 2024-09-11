
import React from 'react';
import Map from './Map';
import NewsDashBoard from './NewsDashBoard';
import './Content.css';
import phone from './images/phone.jpg';
import sos from './images/sos.png';

const Content = () => {
  return (
    <div className="container">
      <div className="splitting">
        <div className="map-container">
          <Map />
        </div>
        <div className="news-dashboard-container">
          <NewsDashBoard />
        </div>
      </div>
      <div className='call'>
        <button><img src={phone}></img></button>
        <button><img src={sos}></img></button>
      </div>
    </div>
  );
}

export default Content;