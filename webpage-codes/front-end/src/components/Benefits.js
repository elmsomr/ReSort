// src/components/Benefits.js
import React from 'react';
import './Benefits.css'; // CSS dosyasını import ediyoruz
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLeaf, faTint, faRecycle } from '@fortawesome/free-solid-svg-icons';

const Benefits = () => {
  return (
    <div className="benefits-container">
      <h3 style={{ textAlign: "left", marginLeft: "20px" }}>Environmental Benefits</h3>
      <div className="benefits-box">
        <div className="benefit-item pollution">
          <FontAwesomeIcon icon={faLeaf} className="benefit-icon" />
          <h4>Reduced Pollution</h4>
          <p>Less waste in landfills means reduced greenhouse gas emissions.</p>
        </div>
        <div className="benefit-item water">
          <FontAwesomeIcon icon={faTint} className="benefit-icon" />
          <h4>Water Conservation</h4>
          <p>Recycling helps preserve our precious water resources.</p>
        </div>
        <div className="benefit-item resource">
          <FontAwesomeIcon icon={faRecycle} className="benefit-icon" />
          <h4>Resource Conservation</h4>
          <p>Reduces the need for raw material extraction.</p>
        </div>
      </div>
    </div>
  );
};

export default Benefits;
