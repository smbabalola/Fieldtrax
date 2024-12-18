// File: /frontend/src/pages/LoginPage.jsx
import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate, Link } from 'react-router-dom';
import { Form, Button, Card, Container, Alert, Spinner } from 'react-bootstrap';
import { loginStart, loginSuccess, loginFailure } from '../store/slices/authSlice';
import axios from '../utils/axios';

const LoginPage = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { isAuthenticated, loading, error } = useSelector((state) => state.auth);

    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });
    const [validationErrors, setValidationErrors] = useState({});
    const [showPassword, setShowPassword] = useState(false);

    // Redirect if already authenticated
    useEffect(() => {
        if (isAuthenticated) {
            navigate('/dashboard');
        }
    }, [isAuthenticated, navigate]);

    const validateForm = () => {
        const errors = {};
        if (!formData.username.trim()) {
            errors.username = 'Username is required';
        }
        if (!formData.password) {
            errors.password = 'Password is required';
        }
        setValidationErrors(errors);
        return Object.keys(errors).length === 0;
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
        // Clear validation error when user starts typing
        if (validationErrors[name]) {
            setValidationErrors(prev => ({
                ...prev,
                [name]: ''
            }));
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // Validate form
        if (!validateForm()) {
            return;
        }

        try {
            dispatch(loginStart());

            // Create URLSearchParams for x-www-form-urlencoded format
            const params = new URLSearchParams();
            params.append('username', formData.username);
            params.append('password', formData.password);
            params.append('grant_type', 'password');

            console.log('Attempting login with:', formData.username);

            const response = await axios.post('/token', params, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                withCredentials: true
            });

            console.log('Login response received');

            if (response.data?.access_token) {
                const userData = {
                    token: response.data.access_token,
                    refreshToken: response.data.refresh_token,
                    userId: response.data.user_id,
                    isActive: true,
                    username: formData.username
                };

                // Store tokens in localStorage
                localStorage.setItem('token', response.data.access_token);
                localStorage.setItem('refreshToken', response.data.refresh_token);
                localStorage.setItem('userData', JSON.stringify(userData));

                dispatch(loginSuccess(userData));
                navigate('/dashboard');
            } else {
                throw new Error('Invalid response format');
            }
        } catch (err) {
            console.error('Login error:', err);
            const errorMessage = err.response?.data?.detail || 
                               'Unable to connect to server. Please try again later.';
            dispatch(loginFailure(errorMessage));
        }
    };

    return (
        <Container 
            className="d-flex align-items-center justify-content-center min-vh-100"
            style={{ background: '#f8f9fa' }}
        >
            <Card className="shadow-sm" style={{ maxWidth: '400px', width: '100%' }}>
                <Card.Body className="p-4">
                    {/* Logo and Title */}
                    <div className="text-center mb-4">
                        <img 
                            src="/logo.png" 
                            alt="FieldTrax Logo" 
                            className="mb-3"
                            style={{ height: '48px' }}
                        />
                        <h4 className="text-primary mb-2">Welcome to FieldTrax</h4>
                        <p className="text-muted">Sign in to your account</p>
                    </div>

                    {/* Error Alert */}
                    {error && (
                        <Alert 
                            variant="danger" 
                            className="mb-4"
                            dismissible
                            onClose={() => dispatch(loginFailure(null))}
                        >
                            {error}
                        </Alert>
                    )}

                    {/* Login Form */}
                    <Form onSubmit={handleSubmit}>
                        <Form.Group className="mb-3">
                            <Form.Label>Email</Form.Label>
                            <Form.Control
                                type="email"
                                name="username"
                                value={formData.username}
                                onChange={handleChange}
                                placeholder="Enter your email"
                                isInvalid={!!validationErrors.username}
                                disabled={loading}
                                autoComplete="email"
                                autoFocus
                            />
                            <Form.Control.Feedback type="invalid">
                                {validationErrors.username}
                            </Form.Control.Feedback>
                        </Form.Group>

                        <Form.Group className="mb-4">
                            <Form.Label className="d-flex justify-content-between">
                                <span>Password</span>
                            </Form.Label>
                            <div className="position-relative">
                                <Form.Control
                                    type={showPassword ? "text" : "password"}
                                    name="password"
                                    value={formData.password}
                                    onChange={handleChange}
                                    placeholder="Enter your password"
                                    isInvalid={!!validationErrors.password}
                                    disabled={loading}
                                    autoComplete="current-password"
                                />
                                <Button
                                    variant="link"
                                    className="position-absolute end-0 top-50 translate-middle-y text-muted"
                                    onClick={() => setShowPassword(!showPassword)}
                                    style={{ zIndex: 10 }}
                                >
                                    <i className={`bi bi-eye${showPassword ? '-slash' : ''}`}></i>
                                </Button>
                            </div>
                            <Form.Control.Feedback type="invalid">
                                {validationErrors.password}
                            </Form.Control.Feedback>
                        </Form.Group>

                        <Button
                            variant="primary"
                            type="submit"
                            className="w-100 mb-3"
                            disabled={loading}
                        >
                            {loading ? (
                                <>
                                    <Spinner
                                        as="span"
                                        animation="border"
                                        size="sm"
                                        role="status"
                                        aria-hidden="true"
                                        className="me-2"
                                    />
                                    Signing in...
                                </>
                            ) : (
                                'Sign In'
                            )}
                        </Button>

                        <div className="text-center">
                            <Link
                                to="/forgot-password"
                                className="text-decoration-none"
                            >
                                Forgot password?
                            </Link>
                        </div>
                    </Form>
                </Card.Body>
            </Card>
        </Container>
    );
};

export default LoginPage;