function TruckCard({ img, vehicle_tag, vehicle_number, vehicle_brand, vehicle_model, price, 
  year, odometer, gross_weight, rear_axle_type, transmission}) {

  return (
    <div className="truck-card" >
      <img src={img} alt={vehicle_number} className="truck-card-head" />
      <div className="card-body">
        <div className="card-title">
          <h3 className="vehicle_number"> VEH-{vehicle_number} </h3>
          <h3 className="certified"> {vehicle_tag} </h3>
      </div>
        <h3 className="vehicle_brand"> {vehicle_brand} </h3>
        <h3 className="vehicle_model"> {vehicle_model} </h3>
        <h3 className="vehicle_price"> {price} </h3>
        <div className="card-mid-section">
          <ul className="mid-text">
            <li> Year </li>
            <li> Odometer </li>
            <li> Gross Weight </li>
          </ul>
          <ul className="mid_text-info">
            <li> {year} </li>
            <li> {odometer}    Miles </li>
            <li> {gross_weight} Pounds </li>
          </ul>
        </div>
        <div className="vehicle-type-container">
           <div className="vehicle-type-label">
            <p >Rear Axle Type </p>
            <p >Transmission </p>
          </div>
          <div className="vehicle-type-block">
            <p > {rear_axle_type} </p>
            <p> {transmission} </p>
          </div>
        </div>
      </div>
      
      
    </div>
  );
}

export default TruckCard;