// src/utils/navigationHelpers.js
import { matchPath } from 'react-router-dom';

export const isActiveRoute = (pathname, route) => {
  return !!matchPath(route, pathname);
};

export const getBreadcrumbs = (pathname, routes) => {
  const paths = pathname.split('/').filter(Boolean);
  return paths.map((path, index) => {
    const url = `/${paths.slice(0, index + 1).join('/')}`;
    const route = routes.find(r => matchPath(r.path, url));
    return {
      label: route?.label || path,
      path: url,
      isActive: index === paths.length - 1
    };
  });
};

export const getTabRoutes = (baseUrl, tabs) => {
  return tabs.map(tab => ({
    path: `${baseUrl}/${tab.id}`,
    label: tab.label,
    component: tab.component,
    validation: tab.validation
  }));
};

export const getPreviousRoute = (currentPath, routes) => {
  const currentIndex = routes.findIndex(route => 
    matchPath(route.path, currentPath)
  );
  return currentIndex > 0 ? routes[currentIndex - 1].path : null;
};

export const getNextRoute = (currentPath, routes) => {
  const currentIndex = routes.findIndex(route => 
    matchPath(route.path, currentPath)
  );
  return currentIndex < routes.length - 1 ? routes[currentIndex + 1].path : null;
};

export const checkRequiredFields = (data, fields = []) => {
  return fields.every(field => {
    if (typeof field === 'string') {
      return data[field] !== undefined && data[field] !== null && data[field] !== '';
    }
    if (typeof field === 'object' && field.name && field.validator) {
      return field.validator(data[field.name]);
    }
    return false;
  });
};