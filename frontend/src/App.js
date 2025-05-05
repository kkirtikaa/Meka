import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login'; // make sure the path is correct
import Forgotpass from './components/Forgotpass';
import Signup from './components/Signup';
function App() {
  return (
    <div>
        <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/forgotpass" element={<Forgotpass />} />
        <Route path="/signup" element={<Signup /> } />
      </Routes>
    </Router>
    </div>
  );
}

export default App;

