// File: /frontend/src/store/slices/__tests__/jobsSlice.test.js
import configureMockStore from 'redux-mock-store';
import thunk from 'redux-thunk';
import jobsReducer, {
  fetchJobs,
  fetchActiveJobs,
  createJob,
  updateJob,
  setFilters,
  clearFilters,
  setPagination
} from '../jobsSlice';
import jobService from '../../../services/jobService';

// Mock the job service
jest.mock('../../../services/jobService');

const mockStore = configureMockStore([thunk]);

describe('jobsSlice', () => {
  let store;

  beforeEach(() => {
    store = mockStore({
      jobs: {
        list: [],
        loading: false,
        error: null,
        filters: {},
        pagination: {
          currentPage: 1,
          pageSize: 10,
          totalItems: 0
        }
      }
    });
  });

  describe('reducers', () => {
    test('should handle initial state', () => {
      expect(jobsReducer(undefined, { type: 'unknown' })).toEqual({
        list: [],
        activeJobs: [],
        currentJob: null,
        currentJobTimeSheets: [],
        loading: false,
        error: null,
        filters: {
          status: null,
          search: '',
          dateRange: null,
          wellName: '',
          rigName: ''
        },
        pagination: {
          currentPage: 1,
          pageSize: 10,
          totalItems: 0
        }
      });
    });

    test('should handle setFilters', () => {
      const initialState = {
        filters: {
          status: null,
          search: ''
        }
      };

      const newFilters = {
        status: 'IN_PROGRESS',
        search: 'test'
      };

      expect(
        jobsReducer(initialState, setFilters(newFilters))
      ).toEqual({
        filters: {
          status: 'IN_PROGRESS',
          search: 'test'
        }
      });
    });

    test('should handle clearFilters', () => {
      const initialState = {
        filters: {
          status: 'IN_PROGRESS',
          search: 'test'
        }
      };

      expect(
        jobsReducer(initialState, clearFilters())
      ).toEqual({
        filters: {
          status: null,
          search: '',
          dateRange: null,
          wellName: '',
          rigName: ''
        }
      });
    });
  });

  describe('async thunks', () => {
    test('should handle fetchJobs.fulfilled', async () => {
      const mockJobs = [
        { id: 1, wellName: 'Well-01' },
        { id: 2, wellName: 'Well-02' }
      ];

      jobService.getJobs.mockResolvedValueOnce(mockJobs);

      const dispatchedActions = [];
      await store.dispatch(fetchJobs());

      const actions = store.getActions();
      expect(actions[0].type).toBe(fetchJobs.pending.type);
      expect(actions[1].type).toBe(fetchJobs.fulfilled.type);
      expect(actions[1].payload).toEqual(mockJobs);
    });

    test('should handle fetchJobs.rejected', async () => {
      const error = new Error('Failed to fetch jobs');
      jobService.getJobs.mockRejectedValueOnce(error);

      await store.dispatch(fetchJobs());

      const actions = store.getActions();
      expect(actions[0].type).toBe(fetchJobs.pending.type);
      expect(actions[1].type).toBe(fetchJobs.rejected.type);
    });

    test('should handle createJob.fulfilled', async () => {
      const newJob = {
        wellName: 'New Well',
        rigName: 'New Rig'
      };

      const createdJob = { ...newJob, id: 1 };
      jobService.createJob.mockResolvedValueOnce(createdJob);

      await store.dispatch(createJob(newJob));

      const actions = store.getActions();
      expect(actions[0].type).toBe(createJob.pending.type);
      expect(actions[1].type).toBe(createJob.fulfilled.type);
      expect(actions[1].payload).toEqual(createdJob);
    });

    test('should handle updateJob.fulfilled', async () => {
      const jobUpdate = {
        id: 1,
        wellName: 'Updated Well'
      };

      jobService.updateJob.mockResolvedValueOnce(jobUpdate);

      await store.dispatch(updateJob({ jobId: 1, jobData: jobUpdate }));

      const actions = store.getActions();
      expect(actions[0].type).toBe(updateJob.pending.type);
      expect(actions[1].type).toBe(updateJob.fulfilled.type);
      expect(actions[1].payload).toEqual(jobUpdate);
    });
  });
});