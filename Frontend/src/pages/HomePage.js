import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/homepage.css';
import { useNavigate } from 'react-router-dom';
import TravelPlanForm from '../components/Travelplanform'; // Adjust the path as needed

const HomePage = () => {
  const navigate = useNavigate();
  const [showDropdown, setShowDropdown] = useState(false);
  const [successMessage, setSuccessMessage] = useState(''); // State for success message

  useEffect(() => {
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      navigate('/login');
    }
  }, [navigate]);

  const handleTravelPlanSubmit = (travelPlanData) => {
    fetch('/api/travel-plans', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`, // Use JWT token for authorization
      },
      body: JSON.stringify(travelPlanData),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      // Handle successful response
      console.log('Travel Plan Created:', data);
      setSuccessMessage('Travel plan created successfully!'); // Set success message

      // Redirect to the dashboard after a brief delay
      setTimeout(() => {
        navigate('/dashboard'); // Redirect to the dashboard
      }, 2000); // Delay of 2 seconds (2000 milliseconds)
    })
    .catch((error) => {
      console.error('Error creating travel plan:', error);
      alert('There was an error creating your travel plan. Please try again.');
    });
  };

  return (
    <div className="homepage">
      <header className="d-flex justify-content-between align-items-center px-4 py-2">
        <img src="/assets/images/goplanlogo.png" alt="GoPlan Logo" className="logo" />
        <div className="profile-icon" onClick={() => setShowDropdown(!showDropdown)} style={{ cursor: 'pointer' }}>
          <img src="/assets/images/maleuser.png" alt="Profile" />
          {showDropdown && (
            <div className="dropdown-menu">
              <div className="dropdown-item" onClick={() => navigate('/profile')}>Your Profile</div>
              <div className="dropdown-item" onClick={() => navigate('/dashboard')}>Dashboard</div>
              <div className="dropdown-item" onClick={() => {
                localStorage.removeItem('access_token');
                navigate('/login');
              }}>Logout</div>
            </div>
          )}
        </div>
      </header>

      {successMessage && ( // Move success message rendering here
        <div className="alert alert-success text-center mt-3" role="alert">
          {successMessage}
        </div>
      )}

      <main className="d-flex flex-column align-items-center justify-content-center text-center">
        <h1 className="text-success">Plan Travel</h1>
        <TravelPlanForm onSubmit={handleTravelPlanSubmit} /> {/* Pass the submit handler to the TravelPlanForm */}
      </main>
    </div>
  );
};

export default HomePage;
