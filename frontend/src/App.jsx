import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [forecasts, setForecasts] = useState([]);

  useEffect(() => {
    // Fetch forecasts from the FastAPI backend
    axios.get('http://localhost:8000/api/forecasts')
      .then(response => {
        setForecasts(response.data.forecasts);
      })
      .catch(error => {
        console.error("Error fetching data:", error);
      });
  }, []);

  return (
    <div>
      <h1>KFC Sales Forecast System</h1>
      <h2>Found {forecasts.length} forecasts in the database.</h2>
    </div>
  );
}

export default App;