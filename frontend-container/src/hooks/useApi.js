import { useState } from 'react';

const useApi = () => {
  const [isLoading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // General method for fetching data
  const fetchData = async (url, params = {}) => {
    setLoading(true);
    setError(null);
    try {
      // Construct the URL with query parameters
      const queryParams = new URLSearchParams(params).toString();
      const response = await fetch(`${url}?${queryParams}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      return data; // Return the data here
    } catch (e) {
      setError(`Failed to fetch: ${e.message}`);
      console.error(e); // Log the error for debugging purposes
      return null; // Return null to indicate an error occurred
    } finally {
      setLoading(false);
    }
  };

  // Method for populating teams
  const fetchAndPopulateTeams = async (selectedYear, selectedSeasonType) => {
    const teamsData = await fetchData('/populate-teams', { year: selectedYear, season_type: selectedSeasonType });
    if (!teamsData) {
      // You can handle the error state here if needed, like setting a local state or something similar
    }
    return teamsData;
  };

  // Method for populating seasons
  const populateSeasons = async () => {
    const seasonsData = await fetchData('/populate-seasons');
    if (!seasonsData) {
      // You can handle the error state here if needed
    }
    return seasonsData;
  };

  // Method for updating data
  const updateData = async (category, year, seasonType, team) => {
    const updateDataResponse = await fetchData('/update-data', { category, year, season_type: seasonType, team });
    if (!updateDataResponse) {
      // You can handle the error state here if needed
    }
    return updateDataResponse;
  };

  // Method for getting top 10 data or other statistics
  const getTop10Data = async (year, seasonType, statType) => {
    const top10Data = await fetchData('/get-top10-data', { year, season_type: seasonType, stat_type: statType });
    if (!top10Data) {
      // You can handle the error state here if needed
    }
    return top10Data;
  };

  return {
    isLoading,
    error,
    fetchAndPopulateTeams,
    populateSeasons,
    updateData,
    getTop10Data,
  };
};

export default useApi;
