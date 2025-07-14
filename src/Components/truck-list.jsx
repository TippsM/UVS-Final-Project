import { useState, useEffect } from 'react';
import truckData from '../assets/truck-card-specs.txt';
import TruckCard from './truck-cards';
import '../Styles/App.css';

export default function TruckList() {
  const [allTrucks, setAllTrucks] = useState([]);
  const [currentPage, setCurrentPage] = useState(0);

  const trucksPerPage = 12;
  const maxPage = Math.ceil(allTrucks.length / trucksPerPage) - 1;

  useEffect(() => {
    fetch(truckData)
      .then(response => response.text())
      .then(data => {
        const lines = data.split("\n");
        const parsedTrucks = lines.map(parseTruckLine).filter(t => Object.keys(t).length > 0);
        setAllTrucks(parsedTrucks);
      });
  }, []);

  const paginatedTrucks = allTrucks.slice(
    currentPage * trucksPerPage,
    (currentPage + 1) * trucksPerPage
  );

  return (
    <div>
      <div className="card-container">
        {paginatedTrucks.map((truck) => (
          <TruckCard key={truck["Vehicle ID"]} truck={truck} />
        ))}
      </div>

      <div className='button-container'>
        <button className='back-button'
        onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 0))}
        disabled={currentPage === 0}
        >
        Back
        </button>

        <span className='page-text'>
        Page {currentPage + 1} of {maxPage + 1}
        </span>

        <button className='next-button'
        onClick={() => setCurrentPage((prev) => Math.min(prev + 1, maxPage))}
        disabled={currentPage >= maxPage}
        >
        Next
        </button>
      </div>
    </div>
  );
}

function parseTruckLine(line) {
  const attributes = line.split(',');
  const truck = {};
  attributes.forEach(attribute => {
    const [key, value] = attribute.split(/:(.+)/);
    if (key && value) truck[key.trim()] = value.trim();
  });
  return truck;
}
