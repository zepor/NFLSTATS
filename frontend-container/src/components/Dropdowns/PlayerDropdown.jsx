import React, { useState, useEffect } from 'react';
import { Dropdown, FormControl } from 'react-bootstrap';

const PlayerDropdown = ({ onPlayerSelect }) => {
  const [players, setPlayers] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [searchValue, setSearchValue] = useState('');

  useEffect(() => {
    const fetchPlayers = async () => {
      setIsLoading(true);
      try {
        // Replace with your API call
