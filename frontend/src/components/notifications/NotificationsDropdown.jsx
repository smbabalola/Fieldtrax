// File: /frontend/src/components/notifications/NotificationsDropdown.jsx
import React, { useState } from 'react';
import { Dropdown, Badge, ListGroup } from 'react-bootstrap';
import { format } from 'date-fns';

const NotificationsDropdown = () => {
  // Sample notifications - replace with real data from your backend
  const [notifications, setNotifications] = useState([
    {
      id: 1,
      type: 'job',
      message: 'New job assignment: Well A-123',
      time: new Date(),
      read: false
    },
    {
      id: 2,
      type: 'report',
      message: 'Daily report pending for Job #45678',
      time: new Date(Date.now() - 3600000), // 1 hour ago
      read: false
    },
    {
      id: 3,
      type: 'alert',
      message: 'Equipment maintenance due in 2 days',
      time: new Date(Date.now() - 7200000), // 2 hours ago
      read: true
    }
  ]);

  const unreadCount = notifications.filter(n => !n.read).length;

  const markAsRead = (notificationId) => {
    setNotifications(notifications.map(notification => 
      notification.id === notificationId 
        ? { ...notification, read: true }
        : notification
    ));
  };

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'job':
        return 'bi-briefcase';
      case 'report':
        return 'bi-file-text';
      case 'alert':
        return 'bi-exclamation-circle';
      default:
        return 'bi-bell';
    }
  };

  const getTimeAgo = (date) => {
    const now = new Date();
    const diffInMinutes = Math.floor((now - date) / 60000);

    if (diffInMinutes < 60) {
      return `${diffInMinutes}m ago`;
    } else if (diffInMinutes < 1440) {
      return `${Math.floor(diffInMinutes / 60)}h ago`;
    } else {
      return format(date, 'MMM d, yyyy');
    }
  };

  return (
    <Dropdown align="end">
      <Dropdown.Toggle 
        variant="link" 
        className="text-muted position-relative nav-link"
      >
        <i className="bi bi-bell fs-5"></i>
        {unreadCount > 0 && (
          <Badge 
            bg="danger" 
            className="position-absolute top-0 start-100 translate-middle rounded-pill"
          >
            {unreadCount}
          </Badge>
        )}
      </Dropdown.Toggle>

      <Dropdown.Menu className="dropdown-menu-end notification-dropdown shadow">
        <div className="px-3 py-2 d-flex justify-content-between align-items-center">
          <h6 className="mb-0">Notifications</h6>
          {unreadCount > 0 && (
            <Badge bg="danger" pill>
              {unreadCount} New
            </Badge>
          )}
        </div>
        <Dropdown.Divider />
        <ListGroup variant="flush" style={{ maxHeight: '300px', overflowY: 'auto' }}>
          {notifications.length > 0 ? (
            notifications.map(notification => (
              <ListGroup.Item 
                key={notification.id}
                action
                className={`px-3 ${!notification.read ? 'bg-light' : ''}`}
                onClick={() => markAsRead(notification.id)}
              >
                <div className="d-flex align-items-center">
                  <div className="me-3">
                    <i className={`bi ${getNotificationIcon(notification.type)} fs-4`}></i>
                  </div>
                  <div className="flex-grow-1">
                    <div className={`mb-1 ${!notification.read ? 'fw-bold' : ''}`}>
                      {notification.message}
                    </div>
                    <small className="text-muted">
                      {getTimeAgo(notification.time)}
                    </small>
                  </div>
                  {!notification.read && (
                    <div className="ms-2">
                      <div className="notification-dot"></div>
                    </div>
                  )}
                </div>
              </ListGroup.Item>
            ))
          ) : (
            <ListGroup.Item className="text-center py-4">
              <i className="bi bi-check2-circle text-muted fs-4 mb-2"></i>
              <p className="text-muted mb-0">No new notifications</p>
            </ListGroup.Item>
          )}
        </ListGroup>
        {notifications.length > 0 && (
          <>
            <Dropdown.Divider />
            <div className="p-2 text-center">
              <button className="btn btn-link btn-sm text-decoration-none">
                View All Notifications
              </button>
            </div>
          </>
        )}
      </Dropdown.Menu>
    </Dropdown>
  );
};

export default NotificationsDropdown;