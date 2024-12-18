// src/components/common/ToastNotification.jsx
import React from 'react';
import { Toast, ToastContainer } from 'react-bootstrap';
import { useSelector, useDispatch } from 'react-redux';
import { clearNotification } from '../../store/slices/uiSlice';

const ToastNotification = () => {
  const dispatch = useDispatch();
  const notification = useSelector(state => state.ui.notification);

  if (!notification) return null;

  return (
    <ToastContainer position="top-end" className="p-3">
      <Toast 
        onClose={() => dispatch(clearNotification())}
        show={!!notification}
        delay={3000}
        autohide
        bg={notification.type}
      >
        <Toast.Header>
          <strong className="me-auto">{notification.title}</strong>
        </Toast.Header>
        <Toast.Body className={notification.type === 'success' ? 'text-white' : ''}>
          {notification.message}
        </Toast.Body>
      </Toast>
    </ToastContainer>
  );
};

export default ToastNotification;