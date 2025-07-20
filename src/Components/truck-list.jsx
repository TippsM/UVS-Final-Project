import { useState, useEffect } from 'react';
import truckData from '../assets/truck-card-specs.txt';
import TruckCard from './truck-cards';
import '../Styles/App.css';

export default function TruckList( {queries} ) {

  //console.log("All saved queries: ", queries)


  const [allTrucks, setAllTrucks] = useState([]);
  const [currentPage, setCurrentPage] = useState(0);

  const truckCount = 12;
  const maxPage = Math.ceil(allTrucks.length / truckCount) - 1;

  useEffect(() => {
    fetch(truckData)
      .then(response => response.text())
      .then(data => {
        const lines = data.split("\n");
        const parsedTrucks = lines.map(parseTruckLine).filter(t => Object.keys(t).length > 0);
        setAllTrucks(parsedTrucks);
      });
  }, []);

  const trucksPerPage = allTrucks.slice(
    currentPage * truckCount,
    (currentPage + 1) * truckCount
  );

  const priorityList = ['201450', '996769', '222534', '222279', '899258', '200294']

  allTrucks.sort((a, b) => {

    const truckOne = queries.indexOf(a["Vehicle ID"]);
    const truckTwo = queries.indexOf(b["Vehicle ID"]);

    if (truckOne === -1) return 1; // put a after b
    if (truckTwo === -1) return -1; // put b after a

    return truckOne - truckTwo; // both trucks in the priority list (sort by order of list)

  });


  return (
    <div>
      <div className="card-container">
        {trucksPerPage.map((truck) => (
          <TruckCard key={truck["Vehicle ID"]} truck={truck} />
        ))}
      </div>

      <div className='button-container'>

        <button className='first-page-button'
        onClick={() => setCurrentPage((0))}
        disabled={currentPage === 0}
        >
        First
        </button>


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

        <button className='first-page-button'
        onClick={() => setCurrentPage((maxPage))}
        disabled={currentPage === maxPage}
        >
        Last
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
