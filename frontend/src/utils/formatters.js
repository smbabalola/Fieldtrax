  // src/utils/formatters.js
  export const formatDate = (dateString) => {
    if (!dateString) return '';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };
  
  export const formatDepth = (depth, unit = 'ft') => {
    if (!depth) return '';
    return `${depth} ${unit}`;
  };