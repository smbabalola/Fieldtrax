// File: /frontend/src/pages/SettingsPage.jsx
import React, { useEffect } from 'react';
import { Container, Row, Col, Alert, Spinner } from 'react-bootstrap';
import UnitPreview from '../components/settings/UnitPreview';
import AdvancedFormatting from '../components/settings/AdvancedFormatting';
import { useSelector } from 'react-redux';
import { useSettings } from '../hooks/useSettings';
import ModuleHeader from '../components/common/ModuleHeader';

const SettingsPage = () => {
  const isAuthenticated = useSelector(state => state.auth.isAuthenticated);
  const { loading, error } = useSettings();

  useEffect(() => {
    document.title = 'FieldTrax - Settings';
  }, []);

  if (loading) {
    return (
      <Container fluid className="d-flex justify-content-center align-items-center min-vh-50">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading settings...</span>
        </Spinner>
      </Container>
    );
  }

  return (
    <Container fluid>
      <ModuleHeader 
        title="Settings"
        subtitle="Manage your system preferences and display settings"
      />

      {error && (
        <Alert variant="danger" className="mt-3">
          <Alert.Heading>Error Loading Settings</Alert.Heading>
          <p>{error}</p>
        </Alert>
      )}

      <Row className="mt-4">
        <Col lg={6} className="mb-4">
          <ErrorBoundary
            fallback={
              <SettingsErrorFallback
                message="Error loading unit preferences"
                onRetry={() => window.location.reload()}
              />
            }
          >
            <UnitPreview />
          </ErrorBoundary>
        </Col>
        
        <Col lg={6} className="mb-4">
          <ErrorBoundary
            fallback={
              <SettingsErrorFallback
                message="Error loading display settings"
                onRetry={() => window.location.reload()}
              />
            }
          >
            <AdvancedFormatting />
          </ErrorBoundary>
        </Col>
      </Row>
    </Container>
  );
};

// Improved Error Boundary Component
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    // Here you could add error reporting to your monitoring service
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <Alert variant="danger" className="my-3">
          <Alert.Heading>Component Error</Alert.Heading>
          <p>Something went wrong loading this component.</p>
          <div className="d-flex justify-content-end">
            <button 
              className="btn btn-outline-danger"
              onClick={() => window.location.reload()}
            >
              Reload Page
            </button>
          </div>
        </Alert>
      );
    }

    return this.props.children;
  }
}

// Error Fallback Component
const SettingsErrorFallback = ({ message, onRetry }) => (
  <Alert variant="danger" className="h-100 d-flex flex-column">
    <Alert.Heading>Settings Error</Alert.Heading>
    <p>{message}</p>
    <div className="mt-auto d-flex justify-content-end">
      <button 
        className="btn btn-outline-danger"
        onClick={onRetry}
      >
        Retry
      </button>
    </div>
  </Alert>
);

export default SettingsPage;