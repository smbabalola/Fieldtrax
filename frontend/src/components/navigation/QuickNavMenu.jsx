// src/components/navigation/QuickNavMenu.jsx
import React, { useState } from 'react';
import { Dropdown, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { 
  List, 
  Tools,
  Clipboard,
  Droplet,
  Truck
} from 'react-bootstrap-icons';

const QuickNavMenu = ({ jobId }) => {
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);

  const quickNavItems = [
    {
      title: 'Job Overview',
      icon: <Clipboard className="me-2" />,
      path: jobId ? `/job/${jobId}` : '/'
    },
    {
      title: 'Rigs',
      icon: <Tools className="me-2" />,
      path: '/rigs'
    },
    {
      title: 'Physical Barriers',
      icon: <Tools className="me-2" />,
      path: jobId ? `/job/${jobId}/physical-barriers` : null
    },
    {
      title: 'Fluid Management',
      icon: <Droplet className="me-2" />,
      path: jobId ? `/job/${jobId}/fluid` : null
    },
    {
      title: 'Delivery Tickets',
      icon: <Truck className="me-2" />,
      path: jobId ? `/job/${jobId}/delivery-tickets` : null
    }
  ];

  const handleSelect = (path) => {
    if (path) {
      navigate(path);
      setIsOpen(false);
    }
  };

  return (
    <div className="quick-nav-menu">
      <Dropdown show={isOpen} onToggle={(isOpen) => setIsOpen(isOpen)}>
        <Dropdown.Toggle 
          variant="outline-primary" 
          id="quick-nav-dropdown"
          className="d-flex align-items-center"
        >
          <List className="me-2" />
          Quick Navigation
        </Dropdown.Toggle>

        <Dropdown.Menu>
          {quickNavItems.map((item, index) => (
            <React.Fragment key={item.title}>
              {index > 0 && item.path && <Dropdown.Divider />}
              <Dropdown.Item
                onClick={() => handleSelect(item.path)}
                disabled={!item.path}
                className="d-flex align-items-center"
              >
                {item.icon}
                {item.title}
              </Dropdown.Item>
            </React.Fragment>
          ))}
        </Dropdown.Menu>
      </Dropdown>
    </div>
  );
};

export default QuickNavMenu;