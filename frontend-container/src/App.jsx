import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import YearDropdown from './components/Dropdowns/YearDropdown';
import SeasonTypeDropdown from './components/Dropdowns/SeasonTypeDropdown';
import TeamDropdown from './components/Dropdowns/TeamDropdown';
import StatsTable from './components/Tables/StatsTable';
import DataNavigation from './components/Buttons/DataNavigation';
import useApi from './hooks/useApi';

function App() {
  const {
    isLoading,
    error,
    fetchAndPopulateTeams, // Use the correct function name here
    populateSeasons,
  } = useApi();

  const [selectedYear, setSelectedYear] = useState(null);
  const [selectedSeasonType, setSelectedSeasonType] = useState(null);
  const [teams, setTeams] = useState([]);
  const [years, setYears] = useState([]);
  const [seasonTypes, setSeasonTypes] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [selectedPlayer, setSelectedPlayer] = useState(null);

  // Fetch and populate years and season types
  useEffect(() => {
    populateSeasons()
      .then((data) => {
        if (data) {
          const uniqueYears = Array.from(new Set(data.map(season => season.year)));
          const uniqueSeasonTypes = Array.from(new Set(data.map(season => season.season_type)));
          setYears(uniqueYears.sort((a, b) => b - a)); // Sort years in descending order
          setSeasonTypes(uniqueSeasonTypes);
        }
      })
      .catch(err => {
        console.error('Error fetching seasons:', err);
      });
  }, [populateSeasons]);

  // Fetch teams when year and season type are selected
  useEffect(() => {
    if (selectedYear && selectedSeasonType) {
      fetchAndPopulateTeams(selectedYear, selectedSeasonType)
        .then((data) => {
          setTeams(data?.teams || []);
        })
        .catch((err) => {
          console.error('Error fetching teams:', err);
        });
    }
  }, [selectedYear, selectedSeasonType, fetchAndPopulateTeams]);

    // Handlers for the dropdowns
  const handleYearSelect = (year) => {
    setSelectedYear(year);
    setSelectedSeasonType(null); // Reset season type when year changes
    setTeams([]); // Reset teams when year changes
    setSelectedTeam(null); // Also reset selected team when year changes
  };


  const handleSeasonTypeSelect = (type) => {
    setSelectedSeasonType(type);
  };

  
  // ... other handlers and logic

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <div className="App">
      <DataNavigation onToggle={(data) => {/* handle toggle here */}} />
      <YearDropdown years={years} selectedYear={selectedYear} onYearSelect={setSelectedYear} />
      <SeasonTypeDropdown seasonTypes={seasonTypes} selectedSeasonType={selectedSeasonType} onSeasonTypeSelect={setSelectedSeasonType} />
      {/* Assuming TeamDropdown is a separate component that needs to be included */}
      <TeamDropdown selectedTeam={selectedTeam} teams={teams} onTeamSelect={setSelectedTeam} />
      <StatsTable season={selectedYear + ' ' + selectedSeasonType} team={selectedTeam} player={selectedPlayer} />
      {/* More components as needed */}
    </div>
  );
}

export default App;
