// frontend\src\components\common\DataTable.jsx
import React from 'react';
import { Table, Pagination } from 'react-bootstrap';
import { FaSort, FaSortUp, FaSortDown } from 'react-icons/fa';
import LoadingSpinner from './LoadingSpinner';

export const DataTable = ({ 
  columns, 
  data, 
  loading,
  onRowClick,
  className = '',
  sortField,
  sortDirection,
  onSort,
  pagination,
  onPageChange
}) => {
  const renderSortIcon = (field) => {
    if (!onSort) return null;
    if (field !== sortField) return <FaSort className="text-muted ms-2" />;
    return sortDirection === 'asc' ? 
      <FaSortUp className="text-primary ms-2" /> : 
      <FaSortDown className="text-primary ms-2" />;
  };

  const renderPagination = () => {
    if (!pagination || !onPageChange) return null;
    
    const { currentPage, totalPages } = pagination;
    return (
      <div className="d-flex justify-content-between align-items-center mt-3">
        <div>
          Showing {Math.min((currentPage - 1) * pagination.pageSize + 1, pagination.totalItems)} to {Math.min(currentPage * pagination.pageSize, pagination.totalItems)} of {pagination.totalItems} entries
        </div>
        <Pagination>
          <Pagination.First 
            disabled={currentPage === 1}
            onClick={() => onPageChange(1)}
          />
          <Pagination.Prev 
            disabled={currentPage === 1}
            onClick={() => onPageChange(currentPage - 1)}
          />
          
          {Array.from({ length: totalPages }, (_, i) => i + 1)
            .filter(page => {
              if (totalPages <= 5) return true;
              if (page === 1 || page === totalPages) return true;
              return Math.abs(page - currentPage) <= 1;
            })
            .map((page, index, array) => {
              if (index > 0 && array[index - 1] !== page - 1) {
                return [
                  <Pagination.Ellipsis key={`ellipsis-${page}`} />,
                  <Pagination.Item
                    key={page}
                    active={page === currentPage}
                    onClick={() => onPageChange(page)}
                  >
                    {page}
                  </Pagination.Item>
                ];
              }
              return (
                <Pagination.Item
                  key={page}
                  active={page === currentPage}
                  onClick={() => onPageChange(page)}
                >
                  {page}
                </Pagination.Item>
              );
            })}
          
          <Pagination.Next 
            disabled={currentPage === totalPages}
            onClick={() => onPageChange(currentPage + 1)}
          />
          <Pagination.Last 
            disabled={currentPage === totalPages}
            onClick={() => onPageChange(totalPages)}
          />
        </Pagination>
      </div>
    );
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div className={className}>
      <Table hover responsive className="data-grid mb-0">
        <thead>
          <tr>
            {columns.map((column, index) => (
              <th 
                key={index}
                onClick={() => column.sortable && onSort?.(column.field)}
                style={column.sortable ? { cursor: 'pointer' } : undefined}
              >
                <div className="d-flex align-items-center">
                  {column.header}
                  {column.sortable && renderSortIcon(column.field)}
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr 
              key={rowIndex}
              onClick={() => onRowClick?.(row)}
              style={onRowClick ? { cursor: 'pointer' } : undefined}
            >
              {columns.map((column, colIndex) => (
                <td key={colIndex}>
                  {column.render ? column.render(row) : row[column.field]}
                </td>
              ))}
            </tr>
          ))}
          {data.length === 0 && (
            <tr>
              <td colSpan={columns.length} className="text-center py-4">
                No data available
              </td>
            </tr>
          )}
        </tbody>
      </Table>
      {renderPagination()}
    </div>
  );
};

export default DataTable;