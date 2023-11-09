// SeasonTypeDropdown.jsx
import React from 'react';
import { Dropdown } from 'react-bootstrap';

const SeasonTypeDropdown = ({ seasonTypes, selectedSeasonType, onSeasonTypeSelect }) => {
  return (
    <Dropdown>
      <Dropdown.Toggle variant="success" id="season-type-dropdown-toggle">
        {selectedSeasonType || 'Select Season Type'}
      </Dropdown.Toggle>
      <Dropdown.Menu>
        {seasonTypes.map((type, index) => (
          <Dropdown.Item key={index} onClick={() => onSeasonTypeSelect(type)}>
            {type}
          </Dropdown.Item>
        ))}
      </Dropdown.Menu>
    </Dropdown>
  );
};

export default SeasonTypeDropdown;