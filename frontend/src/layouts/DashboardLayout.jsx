import React, { useEffect } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { Container, Navbar, Nav, Button, Spinner } from 'react-bootstrap';
import Sidebar from './Sidebar';
import JobSidebar from './JobSidebar';
import { 
  fetchSettings, 
  selectSettings, 
  selectIsLoading,
  toggleSidebar 
} from '../store/slices/settingsSlice';
import { logout } from '../store/slices/authSlice';

const DashboardLayout = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  
  const settings = useSelector(selectSettings);
  const isLoading = useSelector(selectIsLoading);
  const { user, isAuthenticated, authLoading } = useSelector(state => state.auth);

  useEffect(() => {
    const initializeDashboard = async () => {
      if (!isAuthenticated && !authLoading) {
        navigate('/login');
        return;
      }

      if (isAuthenticated) {
        try {
          await dispatch(fetchSettings()).unwrap();
        } catch (error) {
          console.warn('Settings fetch error handled by slice');
        }
      }
    };

    initializeDashboard();
  }, [isAuthenticated, authLoading, dispatch, navigate]);

  const handleLogout = () => {
    dispatch(logout());
    navigate('/login');
  };

  if (authLoading || isLoading) {
    return (
      <div className="d-flex justify-content-center align-items-center min-vh-100">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      </div>
    );
  }

  // Safely access display settings with fallback
  const { display = { sidebarOpen: true }, activeJobId } = settings;

  return (
    <div className="d-flex min-vh-100">
      {/* Main Sidebar */}
      <Sidebar 
        isOpen={display.sidebarOpen} 
        className={display.sidebarOpen ? 'sidebar-expanded' : 'sidebar-collapsed'}
      />

      {/* Job Sidebar - Only show if there's an active job */}
      {activeJobId && <JobSidebar />}

      {/* Main Content */}
      <div className={`flex-grow-1 d-flex flex-column transition-all ${
        display.sidebarOpen ? 'margin-left-expanded' : 'margin-left-collapsed'
      } ${activeJobId ? 'margin-right-expanded' : ''}`}>
        {/* Top Navigation */}
        <Navbar bg="light" expand="lg" className="border-bottom">
          <Container fluid>
            <Button 
              variant="link" 
              onClick={() => dispatch(toggleSidebar())}
              className="p-2 me-3"
            >
              <i className="bi bi-list fs-4"></i>
            </Button>
            <Navbar.Brand>FieldTrax</Navbar.Brand>

            <Navbar.Toggle />
            <Navbar.Collapse className="justify-content-end">
              {user && (
                <Nav>
                  <Nav.Item className="d-flex align-items-center">
                    <span className="text-muted me-3">{user.fullName}</span>
                    <Button
                      variant="outline-secondary"
                      onClick={handleLogout}
                    >
                      Logout
                    </Button>
                  </Nav.Item>
                </Nav>
              )}
            </Navbar.Collapse>
          </Container>
        </Navbar>

        {/* Main Content Area */}
        <div className="flex-grow-1 overflow-auto p-4">
          <Container fluid>
            <Outlet />
          </Container>
        </div>
      </div>
    </div>
  );
};

export default DashboardLayout;