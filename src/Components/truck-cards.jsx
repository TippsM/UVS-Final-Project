import React from 'react';

const TruckCard = React.memo (function TruckCard({ truck }) {

    if (!truck) return null;

  return (
    <div className="truck-card" >
      <img src={truck["Img Url"]} alt="" className="truck-card-head" />
      <div className="card-body">
        <div className="card-title">
          <h3 className="vehicle_number"> VEH-{truck["Vehicle ID"]} </h3>
          <h3 className="certified"> {truck["Vehicle Condition"]} </h3>
      </div>
        <h3 className="vehicle_brand"> {truck["Make"]} </h3>
        <h3 className="vehicle_model"> {truck["Model"]} </h3>
        <h3 className="vehicle_price"> ${truck["Price"]} USD </h3>
        <div className="card-mid-section">
          <ul className="mid-text">
            <li> Year </li>
            <li> Odometer </li>
            <li> Gross Weight </li>
          </ul>
          <ul className="mid_text-info">
            <li> {truck["Year"]} </li>
            <li> {truck["Miles"]}    Miles </li>
            <li> {truck["Gross Weight"]} Pounds </li>
          </ul>
        </div>
        <div className="vehicle-type-container">
           <div className="vehicle-type-label">
            <p >Rear Axle Type </p>
            <p >Transmission </p>
          </div>
          <div className="vehicle-type-block">
            <p > {truck["Rear Axle Type"]} </p>
            <p> {truck["Transmission Type"]} </p>
          </div>
        </div>
      </div>
      
      
    </div>
  );
});

export default TruckCard;

