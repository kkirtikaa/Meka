import React from 'react';
import './Login.css';

function Signup({ show, onClose }) {
  const [signupData, setSignupData] = React.useState({
    firstName: '',
    lastName: '',
    email: '',
    password: ''
  });
const [successMessage, setSuccessMessage] = React.useState('');
  const handleSignupChange = (e) => {
    setSignupData({
      ...signupData,
      [e.target.name]: e.target.value
    });
    setSuccessMessage('');
    
  };

  const handleSignupSubmit = (e) => {
    e.preventDefault();
   
    setSuccessMessage('Sign-up successfully!');
    setTimeout(() => {
      onClose(); // Close the modal after success message is displayed
    }, 2000);
    
    
    
  };

  if (!show) return null; // don't render if not shown

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Sign Up</h2>
        <form onSubmit={handleSignupSubmit}>
          <input
            className='input-field'
            type="text"
            name="firstName"
            placeholder="First Name"
            value={signupData.firstName}
            onChange={handleSignupChange}
            required
          />
          <input
            className='input-field'
            type="text"
            name="lastName"
            placeholder="Last Name"
            value={signupData.lastName}
            onChange={handleSignupChange}
            required
          />
          <input
            className='input-field'
            type="email"
            name="email"
            placeholder="Enter your email"
            value={signupData.email}
            onChange={handleSignupChange}
            required
          />
          <input
            className='input-field'
            type="password"
            name="password"
            placeholder="Enter Password"
            value={signupData.password}
            onChange={handleSignupChange}
            required
          />

{successMessage && (
            <div className="success-message-container">
              <p className="success-message">{successMessage}</p>
            </div>
          )}

          <button className="close-btn" type="button" onClick={onClose}>Close</button>
          <button className="close-btn" type="submit">Submit</button>
        </form>
      </div>
    </div>
  );
}

export default Signup;
