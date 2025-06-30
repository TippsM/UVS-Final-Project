import './Styles/App.css'; // this stays the same (unless you move it too)
import SearchBar from './Components/Searchbar';
import Navbar from './Components/Navigation-menu';
import React, { useState } from 'react';

function App() {

  const [queries, setQueries] = useState(() => {

    const saved = localStorage.getItem('queries');
    return saved ? JSON.parse(saved) : [];
  });

  const handleSearch = (query) => {

    const existing = JSON.parse(localStorage.getItem('queries')) || [];

    const updatedQueries = [...existing, query];
    setQueries(updatedQueries);
    localStorage.setItem('queries', JSON.stringify(updatedQueries));
    console.log("All saved queries: ", updatedQueries)
  };

  return (
    <div className="App">
        <header className="App-header">
          <Navbar/>
        <div className='page-container'>
          <h2 className="page-title">Ryder Used Vehicle Inventory</h2>
          <h3 className="page-sub"> Search Used Vehicles </h3>
          <SearchBar onSearch={handleSearch} />
          <div className="query-history">
          <h4>Search History:</h4>
            <ul>
              {queries.map((query, index) => (
              <li key={index}>{query}</li>
              ))}
           </ul>
          </div>
        </div> 
      </header>
    </div>
  );
}

export default App;


