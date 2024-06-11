import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Home';
import History from './History'; // Assuming you have a History component
import { SensorProvider } from './contexts/SensorContext';
import './App.css';

function App() {
  return (
    <SensorProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/history" element={<History />} />
        </Routes>
      </Router>
    </SensorProvider>
  );
}

export default App;
