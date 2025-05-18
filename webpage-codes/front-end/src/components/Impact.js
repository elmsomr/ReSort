// src/components/Impact.js
import React from 'react';
import './Impact.css'; // CSS dosyasını import ediyoruz
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTrash, faBolt, faTree } from '@fortawesome/free-solid-svg-icons';

const Impact = () => {
  return (

    


<div className="impact-container">
<h3 style={{ textAlign: "left", marginLeft: "20px" }}>Your Recycling Impact</h3>      <div className="impact-box">
        <div className="impact-item waste">
          <FontAwesomeIcon icon={faTrash} className="impact-icon" />
          <h2>247kg</h2>
          <p>Waste Diverted</p>
        </div>
        <div className="impact-item energy">
          <FontAwesomeIcon icon={faBolt} className="impact-icon" />
          <h2>892kWh</h2>
          <p>Energy Saved</p>
        </div>
        <div className="impact-item trees">
          <FontAwesomeIcon icon={faTree} className="impact-icon" />
          <h2>156</h2>
          <p>Trees Preserved</p>
        </div>
      </div>
    </div>

    


    
  );
};

export default Impact;
