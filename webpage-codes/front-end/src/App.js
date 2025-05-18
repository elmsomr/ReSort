// src/App.js
import React from 'react';
import Navbar from './components/Navbar';
import Impact from './components/Impact';
import Benefits from './components/Benefits';
import Events from './components/Events';
import Resources from './components/Resources';
import Contact from './components/Contact'; // Yeni eklenen kısım
import Dashboard from './components/Dashboard';
import LiveData from './components/LiveData';

import './App.css';

function App() {
  return (
    <div className="App">
      <Navbar />
      <Impact />
      <Benefits />
      <Events />
      <Resources />
      <Contact /> {/* Buraya ekledik */}
      <LiveData /> {/* 💡 Veriler burada gösterilecek */}

    </div>
  );
}

export default App;
