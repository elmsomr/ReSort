// src/components/Contact.js
import React from 'react';
import './Contact.css'; // CSS dosyasını import ediyoruz
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEnvelope } from '@fortawesome/free-solid-svg-icons';

const Contact = () => {
  return (
    <div className="contact-container">
      <h3 style={{ textAlign: "left", marginLeft: "30px" }}>Contact Us</h3>
      <p style={{ textAlign: "left", marginLeft: "30px" }}>
        <FontAwesomeIcon icon={faEnvelope} /> support@resort.com
      </p>
    </div>
  );
};

export default Contact;
