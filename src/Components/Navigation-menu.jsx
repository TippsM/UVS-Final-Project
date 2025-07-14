import React from 'react';
import '../Styles/Navbar.css';
import { FaSearch, FaChevronDown } from 'react-icons/fa';
import ryderLogo from '../assets/logo-ryder.svg';
import usLogo from '../assets/us-flag.svg';



function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <img src={ryderLogo} alt='Ryder-Logo' className='logo-ryder'/>
      </div>

      {/* Menu Items */}
      <ul className="navbar-menu">
        <li>Logistics <FaChevronDown /></li>
        <li>E-commerce <FaChevronDown /></li>
        <li>Lease & Maintenance <FaChevronDown /></li>
        <li>Buy Used Trucks <FaChevronDown /></li>
        <li>Rent Trucks <FaChevronDown /></li>
        <li>All Ryder <FaChevronDown /></li>
        <li>Blogs <FaChevronDown /></li>
      </ul>

      {/* Search Icon*/}
      <div className="navbar-search">
        <img
        src={usLogo}
        alt="US Flag"
        className="flag-icon"
        />
        <FaChevronDown className="flag-arrow" />
        <FaSearch className="search-icon" />
        <button className="contact-button">Contact Sales</button>
      </div>
    </nav>
  );
}

export default Navbar;