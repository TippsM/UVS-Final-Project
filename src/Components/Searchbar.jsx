import React, { useState } from 'react';
import '../Styles/SearchBar.css';
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
    <form className="search-bar" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Search for trucks... e.g. '2018 small white refridgerated'"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button type="submit">Search Vehicles
        <img
        src={searchLogo}
        alt="Search Logo"
        className="search-logo"
        />
      </button>
    </form>
  );
}

export default SearchBar;
