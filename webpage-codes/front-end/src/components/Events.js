// src/components/Events.js
import React from 'react';
import './Events.css'; // CSS dosyasını import ediyoruz


const Events = () => {
  return (
    <div className="events-container">
      <h3 style={{ textAlign: "left", marginLeft: "20px" }}>Community Events</h3>
      <div className="events-box">
        <div className="event-item cleanup">
          <h4>Beach Cleanup Drive</h4>
          <p><strong>March 15, 2025</strong> - Join us for our monthly beach cleanup initiative to keep our oceans clean.</p>
        </div>
        <div className="event-item workshop">
          <h4>Recycling Workshop</h4>
          <p><strong>March 22, 2025</strong> - Learn advanced recycling techniques and sustainable living practices.</p>
        </div>
      </div>
    </div>
  );
};

export default Events;
