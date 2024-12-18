// File: /frontend/src/pages/job/JobDetail.jsx
import React from 'react';
import { useParams } from 'react-router-dom';
import 'bootstrap-icons/font/bootstrap-icons.css';

const JobDetail = () => {
  const { jobId } = useParams();

  return (
    <div className="container-fluid">
      <div className="row mb-4">
        <div className="col">
          <h2>Job Details</h2>
          <p className="text-muted">Job ID: {jobId}</p>
        </div>
        <div className="col-auto">
          <button className="btn btn-primary">
            <i className="bi bi-pencil me-2"></i>
            Edit Job
          </button>
        </div>
      </div>

      <div className="row">
        <div className="col-lg-8">
          <div className="card mb-4">
            <div className="card-body">
              <h5 className="card-title mb-4">Job Information</h5>
              <div className="row g-3">
                <div className="col-md-6">
                  <label className="form-label text-muted">Job Number</label>
                  <p className="mb-0">JOB-{jobId}</p>
                </div>
                <div className="col-md-6">
                  <label className="form-label text-muted">Status</label>
                  <p className="mb-0">
                    <span className="badge bg-success">Active</span>
                  </p>
                </div>
                <div className="col-md-6">
                  <label className="form-label text-muted">Start Date</label>
                  <p className="mb-0">March 1, 2024</p>
                </div>
                <div className="col-md-6">
                  <label className="form-label text-muted">End Date</label>
                  <p className="mb-0">Ongoing</p>
                </div>
                <div className="col-md-6">
                  <label className="form-label text-muted">Well Name</label>
                  <p className="mb-0">Well A-123</p>
                </div>
                <div className="col-md-6">
                  <label className="form-label text-muted">Job Type</label>
                  <p className="mb-0">Completion</p>
                </div>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="card-body">
              <h5 className="card-title mb-4">Recent Activity</h5>
              <div className="timeline">
                <div className="timeline-item mb-3 pb-3 border-bottom">
                  <div className="d-flex">
                    <div className="me-3">
                      <i className="bi bi-circle-fill text-primary"></i>
                    </div>
                    <div>
                      <h6 className="mb-1">Job Started</h6>
                      <p className="text-muted mb-0">March 1, 2024 - 09:00 AM</p>
                    </div>
                  </div>
                </div>
                <div className="timeline-item mb-3 pb-3 border-bottom">
                  <div className="d-flex">
                    <div className="me-3">
                      <i className="bi bi-circle-fill text-success"></i>
                    </div>
                    <div>
                      <h6 className="mb-1">Equipment Mobilized</h6>
                      <p className="text-muted mb-0">March 1, 2024 - 10:30 AM</p>
                    </div>
                  </div>
                </div>
                <div className="timeline-item">
                  <div className="d-flex">
                    <div className="me-3">
                      <i className="bi bi-circle-fill text-info"></i>
                    </div>
                    <div>
                      <h6 className="mb-1">Safety Briefing Completed</h6>
                      <p className="text-muted mb-0">March 1, 2024 - 11:00 AM</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-lg-4">
          <div className="card mb-4">
            <div className="card-body">
              <h5 className="card-title mb-4">Key Statistics</h5>
              <div className="mb-3">
                <label className="form-label text-muted">Completion Progress</label>
                <div className="progress">
                  <div 
                    className="progress-bar" 
                    role="progressbar" 
                    style={{width: '45%'}}
                    aria-valuenow="45" 
                    aria-valuemin="0" 
                    aria-valuemax="100"
                  >
                    45%
                  </div>
                </div>
              </div>
              <div className="mb-3">
                <small className="text-muted">Hours Logged</small>
                <h3 className="mb-0">124.5</h3>
              </div>
              <div className="mb-3">
                <small className="text-muted">Cost to Date</small>
                <h3 className="mb-0">$45,320</h3>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="card-body">
              <h5 className="card-title mb-4">Team Members</h5>
              <div className="list-group list-group-flush">
                <div className="list-group-item px-0">
                  <div className="d-flex align-items-center">
                    <div className="me-3">
                      <div className="avatar bg-primary text-white rounded-circle d-flex align-items-center justify-content-center" 
                           style={{width: '40px', height: '40px'}}>
                        JD
                      </div>
                    </div>
                    <div>
                      <h6 className="mb-0">John Doe</h6>
                      <small className="text-muted">Field Engineer</small>
                    </div>
                  </div>
                </div>
                <div className="list-group-item px-0">
                  <div className="d-flex align-items-center">
                    <div className="me-3">
                      <div className="avatar bg-success text-white rounded-circle d-flex align-items-center justify-content-center" 
                           style={{width: '40px', height: '40px'}}>
                        JS
                      </div>
                    </div>
                    <div>
                      <h6 className="mb-0">Jane Smith</h6>
                      <small className="text-muted">Operations Manager</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobDetail;