import React, { useState, useEffect } from 'react';
import useApi from '../../hooks/useApi'; // Adjust the import path as necessary
import DataTable from './DataTable'; 

const StatsTable = ({ season, team }) => {
  const [stats, setStats] = useState([]);
  const [headers, setHeaders] = useState([]);
  const [category, setCategory] = useState('top10'); // Default category, change as per your requirements
  const { getTop10Data, isLoading, error } = useApi(); // Get the required functions from the useApi hook

  useEffect(() => {
    const loadStats = async () => {
      // Check if all necessary information is present
      if (season && team && category) {
        try {
          // Fetch the stats based on the selected season, team, and category
          const data = await getTop10Data(season.year, season.season_type, category, team.name);
          // Assuming the data structure is an array of objects where keys are column names
          setStats(data);
          setHeaders(Object.keys(data[0]).map(key => ({ name: key, width: '7%' })));
        } catch (error) {
          console.error(`Error fetching stats:`, error);
        }
      }
    };

    loadStats();
  }, [season, team, category, getTop10Data]); // Rerun when season, team, or category changes

  const handleCategoryChange = (newCategory) => {
    setCategory(newCategory);
  };

  // Convert the data array into data that DataTable can display
  // The structure could vary based on your data structure.
  const tableData = stats.map((stat) => Object.values(stat));

  if (isLoading) {
    return <div>Loading...</div>; // You can replace this with a spinner or a loading component
  }

  if (error) {
    return <div>Error: {error.message}</div>; // Error handling
  }

  return (
    <>
      {/* Render buttons or dropdowns to change the category */}
      <div>
        {/* Example of category buttons */}
        <button onClick={() => handleCategoryChange('top10')}>Top 10</button>
        <button onClick={() => handleCategoryChange('leaders')}>Leaders</button>
        {/* Add more categories as needed */}
      </div>

      {/* DataTable should be a component that takes headers and data as props and renders a table */}
      <DataTable headers={headers} data={tableData} />
    </>
  );
};

export default StatsTable;
