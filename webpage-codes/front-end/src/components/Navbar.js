import React from 'react';
import './Navbar.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faRecycle } from '@fortawesome/free-solid-svg-icons';

const Navbar = () => {
    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <FontAwesomeIcon icon={faRecycle} /> 
                <span className="brand-text">ReSort</span>
            </div>
            {/* Navbar links removed */}
        </nav>
    );
};

export default Navbar;
