import React from 'react';
import './Styles/App.css'; // this stays the same (unless you move it too)
import SearchBar from './Components/Searchbar';
import Navbar from './Components/Navigation-menu';


function App() {
  const handleSearch = (query) => {
    console.log('Searching for:', query);
  };

  return (
    <div className="App">
        <header className="App-header">
          <Navbar/>
        <div className='page-container'>
          <h2 className="page-title">Ryder Used Vehicle Inventory</h2>
          <h3 className="page-sub"> Search Used Vehicles </h3>
          <SearchBar onSearch={handleSearch} />
        </div>
        
      </header>
    </div>
  );
}

export default App;


