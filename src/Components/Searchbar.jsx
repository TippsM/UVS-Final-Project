import React, { useState } from 'react';
import '../Styles/App.css';
import searchLogo from '../assets/search-logo.svg';

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (onSearch) {
      onSearch(query);
    }

    try {
      const response = await fetch('http://localhost:5000/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });

      const data = await response.json();
      if(data.error){
        console.log('Search results:', data.error);
      }else{
        console.log('Search results:', data.results);

      }

      // Optionally pass results up
      // onSearchResults(data.results);

    } catch (error) {
      console.error('Error fetching from backend:', error);
    }

  };

  return (
    <>
      <form onSubmit={handleSubmit} className='search-bar-form'>
        <div className="search-container">
          <input className='search-bar'
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

    </>
  );
}

export default SearchBar;
