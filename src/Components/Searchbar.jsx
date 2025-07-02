import React, { useState } from 'react';
import '../Styles/App.css';
import searchLogo from '../Logos/search-logo.svg';


function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onSearch) {
      onSearch(query);
    }
  };

  return (
    <form onSubmit={handleSubmit} className='search-bar-form'>
      <div className="search-container">
        <input className='searchbar'
          type="text"
          placeholder="Search for trucks... e.g. '2018 small white refrigerated'"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
  
        <button className="search-button" type="submit">
          Search Vehicles
          <img
            src={searchLogo}
            alt="Search Logo"
            className="search-logo"
          />
        </button>
      </div>
    </form>
  );
}
  

export default SearchBar;
