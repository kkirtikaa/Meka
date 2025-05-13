
import React from 'react';
import './Login.css';
function Forgotpass({show,onClose}) {
     const [ForgotpassData, setForgotpassData] = React.useState({
        email: '',
        newpassword: '',
        confirmpassword: ''
      });
      const [errorMessages, setErrorMessages] = React.useState([]);  
      const [successMessage, setSuccessMessage] = React.useState('');
      React.useEffect(() => {
        if (show) {

          setForgotpassData({
            email: '',  
            newpassword: '',

            confirmpassword: ''
          });
          setErrorMessages([]); // clear errors on modal open
          setSuccessMessage(''); // clear success message on modal open
        }
      }, [show]);
      const handleForgotpassChange = (e) => {
        setForgotpassData({
          ...ForgotpassData,
          [e.target.name]: e.target.value
        });
        setErrorMessages([]); // clear errors on input change
        setSuccessMessage(''); // clear success message on input change
      };
    
    
      const handleForgotpassSubmit = (e) => {
        e.preventDefault();
        const { email, newpassword, confirmpassword } = ForgotpassData;
        let errors = []; 
        if (!email || !newpassword || !confirmpassword) {
            errors.push('Please fill in all fields.');
            
          }
      
          if (newpassword !== confirmpassword) {
            errors.push('Passwords do not match.');
            
          }
          if (errors.length > 0 )  {
            setErrorMessages(errors);  // Update state with error messages
            return;  // Prevent form submission
          }
      
          setErrorMessages([]);
          setSuccessMessage('Password Saved!');
          // Optionally reset form here
          // setForgotpassData({ email: '', newpassword: '', confirmpassword: '' });
          // onClose(); // You can keep this if you want to close modal immediately
      };
    
      if (!show) return null; // don't render if not shown
    
    return(
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>Reset Password</h2>
            <form onSubmit={handleForgotpassSubmit}>

            <input
             className='input-field'
              type="email"
              name="email"
               placeholder="Enter your email" 
               value={ForgotpassData.email} 
               onChange={handleForgotpassChange}
               required />

            <input 
            className='input-field' 
            type="password" 
            name="newpassword"
            placeholder="Enter New Password" 
            value={ForgotpassData.newpassword} 
            onChange={handleForgotpassChange}
            required />

            <input 
            className='input-field' 
            type="password"
            name="confirmpassword"
             placeholder="Confirm Password"
             value={ForgotpassData.confirmpassword} 
             onChange={handleForgotpassChange}
              required />

{(errorMessages.length > 0 || successMessage) && (
    <div className="error-messages">
      {errorMessages.map((msg, index) => (
        <p key={index} className="error-message">{msg}</p>
      ))}
      {successMessage && <p className="success-message">{successMessage}</p>}
    </div>
  )}
            

            <button className="close-btn" onClick={onClose}>Close</button>

            <button className="close-btn" type="submit" >Submit</button>
            </form>
          </div>
          </div>
    );
}
export default Forgotpass;