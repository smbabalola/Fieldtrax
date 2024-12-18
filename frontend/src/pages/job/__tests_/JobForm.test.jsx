// File: /frontend/src/components/job/__tests__/JobForm.test.jsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import { store } from '../../../store';
import JobForm from '../JobForm';

describe('JobForm', () => {
  const mockOnSuccess = jest.fn();

  const renderJobForm = (props = {}) => {
    return render(
      <Provider store={store}>
        <JobForm onSuccess={mockOnSuccess} {...props} />
      </Provider>
    );
  };

  test('renders all form fields', () => {
    renderJobForm();

    expect(screen.getByLabelText(/well name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/rig name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/status/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/start date/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/job type/i)).toBeInTheDocument();
  });

  test('submits form with valid data', async () => {
    renderJobForm();

    // Fill form fields
    fireEvent.change(screen.getByLabelText(/well name/i), {
      target: { value: 'Test Well' }
    });
    fireEvent.change(screen.getByLabelText(/rig name/i), {
      target: { value: 'Test Rig' }
    });
    fireEvent.change(screen.getByLabelText(/start date/i), {
      target: { value: '2024-01-01' }
    });
    fireEvent.change(screen.getByLabelText(/job type/i), {
      target: { value: 'COMPLETION' }
    });

    // Submit form
    fireEvent.click(screen.getByText(/create job/i));

    // Wait for form submission
    await waitFor(() => {
      expect(screen.queryByText(/required/i)).not.toBeInTheDocument();
    });
  });

  test('displays validation errors for empty required fields', async () => {
    renderJobForm();

    // Submit form without filling required fields
    fireEvent.click(screen.getByText(/create job/i));

    // Check for validation messages
    await waitFor(() => {
      expect(screen.getByLabelText(/well name/i)).toBeRequired();
      expect(screen.getByLabelText(/rig name/i)).toBeRequired();
      expect(screen.getByLabelText(/start date/i)).toBeRequired();
    });
  });

  test('pre-fills form with initial data', () => {
    const initialData = {
      wellName: 'Existing Well',
      rigName: 'Existing Rig',
      status: 'PLANNED',
      startDate: '2024-01-01',
      jobType: 'COMPLETION'
    };

    renderJobForm({ initialData });

    expect(screen.getByLabelText(/well name/i)).toHaveValue('Existing Well');
    expect(screen.getByLabelText(/rig name/i)).toHaveValue('Existing Rig');
    expect(screen.getByLabelText(/status/i)).toHaveValue('PLANNED');
    expect(screen.getByLabelText(/start date/i)).toHaveValue('2024-01-01');
    expect(screen.getByLabelText(/job type/i)).toHaveValue('COMPLETION');
  });
});