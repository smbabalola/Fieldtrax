// File: /frontend/src/pages/job/__tests__/JobList.test.jsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import { store } from '../../../store';
import JobList from '../JobList';

describe('JobList', () => {
  const renderJobList = () => {
    return render(
      <Provider store={store}>
        <BrowserRouter>
          <JobList />
        </BrowserRouter>
      </Provider>
    );
  };

  test('renders job list component', async () => {
    renderJobList();
    
    // Check if the main elements are rendered
    expect(screen.getByText('Jobs')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Search jobs...')).toBeInTheDocument();
    expect(screen.getByText('Create New Job')).toBeInTheDocument();
  });

  test('handles search input', async () => {
    renderJobList();
    
    const searchInput = screen.getByPlaceholderText('Search jobs...');
    fireEvent.change(searchInput, { target: { value: 'Test Well' } });

    // Wait for the search results
    await waitFor(() => {
      expect(searchInput.value).toBe('Test Well');
    });
  });

  test('handles status filter', async () => {
    renderJobList();
    
    const statusSelect = screen.getByRole('combobox');
    fireEvent.change(statusSelect, { target: { value: 'IN_PROGRESS' } });

    await waitFor(() => {
      expect(statusSelect.value).toBe('IN_PROGRESS');
    });
  });

  test('navigates to create job page', () => {
    renderJobList();
    
    const createButton = screen.getByText('Create New Job');
    fireEvent.click(createButton);

    expect(window.location.pathname).toBe('/jobs/new');
  });
});