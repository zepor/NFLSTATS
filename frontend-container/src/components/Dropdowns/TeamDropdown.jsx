import React, { useState, useEffect } from 'react';
import { Dropdown, FormControl, Spinner } from 'react-bootstrap';

const TeamDropdown = ({ selectedYear, selectedSeasonType, onTeamSelect, selectedTeam }) => {
  const [teams, setTeams] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [filter, setFilter] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAndPopulateTeams = async () => {
      if (isLoading) return;
      setIsLoading(true);
      setError(null);

      try {
        const response = await fetch(`/populate-teams?year=${selectedYear}&season_type=${selectedSeasonType}`);
        const data = await response.json();

        if (Object.keys(data).length === 0) {
          console.log('No teams data received for selected year and season type.');
        } else {
          setTeams(Object.values(data).flat()); // Assuming the data structure is suitable
        }
      } catch (error) {
        console.error('Error fetching team data:', error);
        setError(error);
      } finally {
        setIsLoading(false);
      }
    };

    if (selectedYear && selectedSeasonType) {
      fetchAndPopulateTeams();
    }
  }, [selectedYear, selectedSeasonType]);

  // Filter teams based on the filter state
  const filteredTeams = teams.filter((team) => team.name.toLowerCase().includes(filter.toLowerCase()));

  return (
    <Dropdown>
      <Dropdown.Toggle variant="success" id="dropdown-basic">
        {isLoading ? 'Loading...' : selectedTeam?.name || 'Select Team'}
      </Dropdown.Toggle>

      <Dropdown.Menu>
        <FormControl
          autoFocus
          className="mx-3 my-2 w-auto"
          placeholder="Type to filter..."
          onChange={(e) => setFilter(e.target.value)}
          value={filter}
        />
        {error && (
          <Dropdown.Item>
            Error: {error.message}
          </Dropdown.Item>
        )}
        {isLoading ? (
          <Dropdown.Item>
            <Spinner animation="border" size="sm" /> Loading...
          </Dropdown.Item>
        ) : (
          filteredTeams.map((team, index) => (
            <Dropdown.Item
              key={index}
              onClick={() => onTeamSelect(team)}
              active={selectedTeam?.id === team.id}
            >
              <img src={team.imageLink} alt={team.name} style={{ marginRight: '10px' }} />
              {team.name}
            </Dropdown.Item>
          ))
        )}
      </Dropdown.Menu>
    </Dropdown>
  );
};

export default TeamDropdown;
