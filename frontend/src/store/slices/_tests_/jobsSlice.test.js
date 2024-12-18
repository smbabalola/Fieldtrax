// File: /frontend/src/store/slices/__tests__/jobsSlice.test.js
import { store } from '../../../store';
import {
  fetchJobs,
  fetchActiveJobs,
  createJob,
  updateJob,
  setFilters,
  clearFilters,
  setPagination
} from '../jobsSlice';

describe('jobsSlice', () => {
  describe('actions and reducers', () => {
    test('should set filters', () => {
      const filters = {
        status: 'IN_PROGRESS',
        search: 'test'
      };

      store.dispatch(setFilters(filters));
      const state = store.getState().jobs;

      expect(state.filters.status).toBe('IN_PROGRESS');
      expect(state.filters.search).toBe('test');
    });

    test('should clear filters', () => {
      store.dispatch(clearFilters());
      const state = store.getState().jobs;

      expect(state.filters.status).toBeNull();
      expect(state.filters.search).toBe('');
      expect(state.filters.dateRange).toBeNull();
    });

    test('should set pagination', () => {
      const pagination = {
        currentPage: 2,
        pageSize: 20
      };

      store.dispatch(setPagination(pagination));
      const state = store.getState().jobs;

      expect(state.pagination.currentPage).toBe(2);
      expect(state.pagination.pageSize).toBe(20);
    });
  });

  describe('async actions', () => {
    test('should fetch jobs', async () => {
      await store.dispatch(fetchJobs());
      const state = store.getState().jobs;

      expect(Array.isArray(state.list)).toBe(true);
      expect(state.loading).toBe(false);
      expect(state.error).toBeNull();
    });

    test('should fetch active jobs', async () => {
      await store.dispatch(fetchActiveJobs());
      const state = store.getState().jobs;

      expect(Array.isArray(state.activeJobs)).toBe(true);
      expect(state.loading).toBe(false);
      expect(state.error).toBeNull();
    });

    test('should create a new job', async () => {
      const newJob = {
        wellName: 'Test Well',
        rigName: 'Test Rig',
        status: 'PLANNED',
        startDate: '2024-01-01',
        jobType: 'COMPLETION'
      };

      const result = await store.dispatch(createJob(newJob));
      expect(result.payload).toHaveProperty('id');
      expect(result.payload.wellName).toBe('Test Well');
    });

    test('should update an existing job', async () => {
      // First, create a job
      const newJob = {
        wellName: 'Update Test Well',
        rigName: 'Test Rig',
        status: 'PLANNED',
        startDate: '2024-01-01',
        jobType: 'COMPLETION'
      };

      const createResult = await store.dispatch(createJob(newJob));
      const jobId = createResult.payload.id;

      // Then update it
      const updateData = {
        ...newJob,
        wellName: 'Updated Well Name'
      };

      const updateResult = await store.dispatch(updateJob({ jobId, jobData: updateData }));
      expect(updateResult.payload.wellName).toBe('Updated Well Name');
    });
  });
});