// DynamicSeasonStats.test.js
import React from 'react';
import { render, fireEvent, waitFor, screen, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import DynamicSeasonStats from './DynamicSeasonStats';
import useApi from './hooks/useApi';

const mockSeasonData = {
  years: ['2021', '2020', '2019'],
  seasonTypes: ['Regular Season', 'Playoffs', 'Preseason'],
  teams
};

jest.mock('./hooks/useApi', () => {
  return jest.fn(() => ({
    default: () => ({
      isLoading: false,
      error: null,
      populateSeasons: jest.fn().mockResolvedValue(mockSeasonData),
      fetchAndPopulateTeams: jest.fn().mockResolvedValue(mockTeamData),
      // ...other mocked functions from the useApi hook
    }),
  }));
});

describe('DynamicSeasonStats Component', () => {
  beforeEach(() => {
    useApi.mockImplementation(() => ({
      isLoading: false,
      error: null,
      populateSeasons: jest.fn().mockResolvedValue(mockSeasonData),
      // ...other mocked functions from the useApi hook
    }));
  });

  it('renders without crashing', async () => {
    await act(async () => {
      render(<DynamicSeasonStats />);
    });
    // Assertions for initial render state
    expect(screen.getByText(/Select Year/i)).toBeInTheDocument();
    expect(screen.getByText(/Select Season Type/i)).toBeInTheDocument();
  });

  it('updates dropdowns and displays stats', async () => {
    await act(async () => {
      render(<DynamicSeasonStats />);
    });
    // Simulate user interactions for selecting year and season type
    const yearDropdown = screen.getByText(/Select Year/i);
    fireEvent.click(yearDropdown);
    const yearOption = await screen.findByText('2021');
    fireEvent.click(yearOption);

    const seasonTypeDropdown = screen.getByText(/Select Season Type/i);
    fireEvent.click(seasonTypeDropdown);
    const seasonTypeOption = await screen.findByText('Regular Season');
    fireEvent.click(seasonTypeOption);

    // Assert that state updates and components render expected output
    // This would depend on how your DynamicSeasonStats component is supposed to behave.
    // For example, if it should display a stats table after selections:
    await waitFor(() => {
      expect(screen.getByRole('table')).toBeInTheDocument();
    });
  });

  // Add more tests as needed to cover all functionality
});
