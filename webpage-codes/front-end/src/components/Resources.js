// src/components/Resources.js
import React from 'react';
import './Resources.css'; // CSS dosyasını import ediyoruz
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGlassMartini, faRecycle, faNewspaper, faIndustry } from '@fortawesome/free-solid-svg-icons';

const Resources = () => {
  return (
    <div className="resources-container">
      <h3 style={{ textAlign: "left", marginLeft: "52px" }}>Recycling Resources </h3>
      <div style={{ marginBottom: "50px" }}></div>

      {/* Geri Dönüşüm Malzemeleri Butonları */}
      <div className="resource-buttons">
        <button className="glass" style={{ color: 'rgba(4,118,82,255)' }}>
          <FontAwesomeIcon icon={faGlassMartini} /> Glass
        </button>
        <button className="plastic" style={{ color: 'rgba(43,80,212,255)' }}>
          <FontAwesomeIcon icon={faRecycle} /> Plastic
        </button>
        <button className="paper" style={{ color: 'rgba(197,117,54,255)' }}>
          <FontAwesomeIcon icon={faNewspaper} /> Paper
        </button>
        <button className="metal" style={{ color: 'rgba(122,126,129,255)' }}>
          <FontAwesomeIcon icon={faIndustry} /> Metal
        </button>
      </div>

      {/* Hızlı Geri Dönüşüm İpuçları */}
      <div className="quick-tips">
        <h4 style={{ textAlign: "left", marginLeft: "52px" }}>Quick Tips</h4>
        <ul>
          <li>✅ Rinse containers before recycling</li>
          <li>✅ Remove caps and lids</li>
          <li>✅ Flatten cardboard boxes</li>
        </ul>
      </div>
    </div>
  );
};

export default Resources;
