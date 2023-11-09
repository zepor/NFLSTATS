// YearDropdown.jsx
import React from 'react';
import { Dropdown } from 'react-bootstrap';

const YearDropdown = ({ years, selectedYear, onYearSelect }) => {
  return (
    <Dropdown>
      <Dropdown.Toggle variant="success" id="year-dropdown-toggle">
        {selectedYear || 'Select Year'}
      </Dropdown.Toggle>
      <Dropdown.Menu>
        {years.map((year, index) => (
          <Dropdown.Item key={index} onClick={() => onYearSelect(year)}>
            {year}
          </Dropdown.Item>
        ))}
      </Dropdown.Menu>
    </Dropdown>
  );
};
export default YearDropdown;


