import React from 'react';
import { render, fireEvent, waitFor, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';
import useApi from './hooks/useApi';
import { act } from 'react-dom/test-utils';

// Mock data for seasons
const mockSeasonItems = [
  { year: 2023, season_type: 'Regular Season' },
  { year: 2023, season_type: 'Pre-Season' },
  { year: 2022, season_type: 'Playoffs' },
  { year: 2022, season_type: 'Regular Season' }
];

// Mock data for teams
const mockTeamItems = [
  { name: 'All Teams', imageLink: '' },
  { name: 'Arizona Cardinals', imageLink: 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/nfl/500/ARI.png&w=40&h=40&cquality=40&scale=crop&location=origin&transparent=true' },
  { name: 'Atlanta Falcons', imageLink: 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/nfl/500/ATL.png&w=40&h=40&cquality=40&scale=crop&location=origin&transparent=true' },
  { name: 'Baltimore Ravens', imageLink: 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/nfl/500/BAL.png&w=40&h=40&cquality=40&scale=crop&location=origin&transparent=true' }
  // ... other teams
];

const mockTop10Data = {
  offensiveLeaders: [
    {
      rank: 1,
      team: 'Miami Dolphins',
      games_played: 6,
      stat: 498.67,
      img: 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/nfl/500/MIA.png&w=40&h=40&cquality=40&scale=crop&location=origin&transparent=true'
    },
    {
      rank: 2,
      team: 'Kansas City Chiefs',
      games_played: 7,
      stat: 396.71,
      img: 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/nfl/500/KC.png&w=40&h=40&cquality=40&scale=crop&location=origin&transparent=true'
    }
  ],
  defensiveLeaders: [
    {
      rank: 1,
      team: 'Cleveland Browns',
      games_played: 6,
      stat: 243.0,
      img: 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/nfl/500/CLE.png&w=40&h=40&cquality=40&scale=crop&location=origin&transparent=true'
    },
    {
      rank: 2,
      team: 'Baltimore Ravens',
      games_played: 7,
      stat: 271.71,
      img: 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/nfl/500/BAL.png&w=40&h=40&cquality=40&scale=crop&location=origin&transparent=true'
    }
  ]
};

// Mock implementation for useApi hook
jest.mock('./hooks/useApi', () => ({
  __esModule: true,
  default: () => ({
    isLoading: false,
    error: null,
    fetchAndPopulateTeams: jest.fn().mockResolvedValue(mockTeamItems),
    populateSeasons: jest.fn().mockResolvedValue(mockSeasonItems),
    updateData: jest.fn(), // Define the mock implementation if needed
    getTop10Data: jest.fn().mockResolvedValue(mockTop10Data),
    // ...other methods as needed
  }),
}));

beforeEach(() => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve({ /* Mocked response */ }),
    })
  );
});

afterEach(() => {
  jest.restoreAllMocks();
});

describe('App Component', () => {
  it('logs "All Teams" as the default value in the team dropdown', async () => {
    render(<App />);
    await screen.findByRole('button', { name: /Select Team/i }); // Wait for the team dropdown to be in the document
    // Log the entire DOM to see what's being rendered
    screen.debug();

    // Since the dropdown is not expanded, "All Teams" might not be in the document.
    // If you want to check if "All Teams" is an option, you should mock the fetchAndPopulateTeams function 
    // to resolve immediately with the mock data that includes "All Teams", and then expand the dropdown.
  });

  it('logs the selected team after a year is selected', async () => {
    render(<App />);

    // Select a year from the year dropdown
    const yearDropdownButton = screen.getByRole('button', { name: /Select Year/i });
    fireEvent.click(yearDropdownButton);
    const yearOption = await screen.findByText('2023');
    fireEvent.click(yearOption);

    // Log the selected team
    const selectedTeam = await screen.findByRole('button', { name: /Select Team/i });
    console.log(selectedTeam.textContent); // Logs the currently selected team
  });

  it('logs items in the teams dropdown after a season type is selected', async () => {
    render(<App />);
    // Open the season type dropdown to ensure the items are rendered
    fireEvent.click(await screen.findByRole('button', { name: /Select Season Type/i }));
    // Use findByText instead of role since the role might not be 'option'
    const seasonTypeOptions = await screen.findAllByText(/Season/); // Adjust the matcher to match your dropdown item texts
    seasonTypeOptions.forEach(option => console.log(option.textContent)); // Logs each season type
  });

  // ... any additional tests
});
