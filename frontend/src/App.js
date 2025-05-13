import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login'; 
import Forgotpass from './components/Forgotpass';
import Signup from './components/Signup';
import Dashboard from './components/Dashboard'; 
function App() {
  return (
    <div>
        <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/forgotpass" element={<Forgotpass />} />
        <Route path="/signup" element={<Signup /> } />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
    </div>
  );
}

export default App;

