import React, { useState } from 'react';
import './Login.css';
import { Link } from 'react-router-dom';
import pic1 from '../asset/pic1.jpg';
import pic2 from '../asset/pic2.jpg';
import pic3 from '../asset/pic3.jpg';
import pic4 from '../asset/pic4.jpg';
import Signup from './Signup';
import Forgotpass from './Forgotpass';

function Login() {
  const [showForgotModal, setShowForgotModal] = useState(false);
  const [showSignupModal, setShowSignupModal] = useState(false);
 

  return (
    <>
      <div className={`login-page ${showForgotModal || showSignupModal ? 'blurred' : ''}`}>
        <div className='right-side'>
          <img src={pic1} alt="pic1" className="right-img" />
          <img src={pic2} alt="pic2" className="right-img" />
          <img src={pic3} alt="pic3" className="right-img" />
          <img src={pic4} alt="pic4" className="right-img" />
        </div>

        <div className='left-side'>
          <h1 style={{ color: '#d492d8' }}>Meka</h1>
          <h1 style={{ color: 'black', fontSize: '1.7rem' }}>Welcome to Meka!</h1>
          <h2 style={{ color: 'black' }}>Snap. Caption. Share.</h2>
          <p style={{ color: 'gray' }}>
            Capture moments and get instant, creative captions powered by AI.
          </p>

          <form>
            <input className='input-field' type="email" placeholder="Email" required />
            <input className='input-field' type="password" placeholder="Password" required />

            <div className='forgot-container'>
              <span className='forgot-link' onClick={() => setShowForgotModal(true)}>
                Forgot password?
              </span>
            </div>

            <button className='button' type="submit">Login</button>

            <div className="signup-container">
              Don’t have an account?{' '}
              <span className="signup-link" onClick={() => setShowSignupModal(true)}>
                Signup
              </span>  
            </div>
          </form>
        </div>
      </div>

      {/* Forgot Password Modal */}
      {/* {showForgotModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>Reset Password</h2>
            <input className='input-field' type="email" placeholder="Enter your email" required />
            <input className='input-field' type="password" placeholder="Enter New Password" required />
            <input className='input-field' type="password" placeholder="Confirm Password" required />
            <button className="close-btn" onClick={() => setShowForgotModal(false)}>Close</button>
            <button className="close-btn" type="submit" onClick={() => alert("Password saved!")}>Submit</button>
          </div>
        </div>
      )} */}
      <Forgotpass show={showForgotModal} onClose={() => setShowForgotModal(false)} />
      {/* Signup Modal */}
      {/* {showSignupModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>Sign Up</h2>
            <form onSubmit={handleSignupSubmit}>
              <input className='input-field' type="text" name="firstName" placeholder="First Name" value={signupData.firstName} onChange={handleSignupChange} required />
              <input className='input-field' type="text" name="lastName" placeholder="Last Name" value={signupData.lastName} onChange={handleSignupChange} required />
              <input className='input-field' type="email" name="email" placeholder="Enter your email" value={signupData.email} onChange={handleSignupChange} required />
              <input className='input-field' type="password" name="password" placeholder="Enter Password" value={signupData.password} onChange={handleSignupChange} required />

              <button className="close-btn" type="button" onClick={() => setShowSignupModal(false)}>Close</button>
              <button className="close-btn" type="submit">Submit</button>
            </form>
          </div>
        </div>
      )} */}
      <Signup show={showSignupModal} onClose={() => setShowSignupModal(false)} />
    </>
  );
}

export default Login;
