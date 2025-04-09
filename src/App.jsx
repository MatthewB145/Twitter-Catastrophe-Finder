
import { useState, useEffect } from 'react';  
import InteractiveMap from './InteractiveMap.jsx'

function App() {
  const [disasters, setDisasters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch the disaster data on component mount
  useEffect(() => {
    const apiUrl =import.meta.env.VITE_SERVER; 
    fetch(apiUrl)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        setDisasters(data);  // Set state with the fetched data
        setLoading(false);    // Set loading to false
      })
      .catch((error) => {
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <>
      <InteractiveMap disasterData={disasters}/>
    </>   
  )
}

export default App
