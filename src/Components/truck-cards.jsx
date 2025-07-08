function TruckCard({ img, certified, vehicle_number, vehicle_brand, vehicle_model, price}) {

  return (
    <div className="truck-card" >
      <img src={img} alt={vehicle_number} className="truck-card-head" />
      <div className="card-body">
        <div className="card-title">
          <h3 className="vehicle_number"> {vehicle_number} </h3>
          <h3 className="certified"> {certified} </h3>
      </div>
        <h3 className="vehicle_brand"> {vehicle_brand} </h3>
        <h3 className="vehicle_model"> {vehicle_model} </h3>
        <h3 className="vehicle_price"> {price} </h3>
        <div className="card-mid-section">
          <ul className="text">
            <li> Year </li>
            <li> Odometer </li>
            <li> Gross Weight </li>
          </ul>

        </div>
      </div>
      
      
    </div>
  );
}

export default TruckCard;