// File: /frontend/src/components/common/Pagination.jsx
import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { setPagination, selectPagination } from '../../store/slices/jobsSlice';

const Pagination = () => {
  const dispatch = useDispatch();
  const { currentPage, pageSize, totalItems, totalPages } = useSelector(selectPagination);

  const pageSizeOptions = [10, 25, 50, 100];

  const handlePageChange = (newPage) => {
    dispatch(setPagination({ currentPage: newPage }));
  };

  const handlePageSizeChange = (event) => {
    const newSize = parseInt(event.target.value, 10);
    dispatch(setPagination({ 
      pageSize: newSize,
      currentPage: 1 // Reset to first page when changing page size
    }));
  };

  // Generate page numbers to display
  const getPageNumbers = () => {
    const delta = 2;
    const range = [];
    const rangeWithDots = [];

    for (
      let i = Math.max(2, currentPage - delta);
      i <= Math.min(totalPages - 1, currentPage + delta);
      i++
    ) {
      range.push(i);
    }

    if (currentPage - delta > 2) {
      rangeWithDots.push(1, '...', ...range);
    } else {
      rangeWithDots.push(1, ...range);
    }

    if (currentPage + delta < totalPages - 1) {
      rangeWithDots.push('...', totalPages);
    } else if (totalPages > 1) {
      rangeWithDots.push(totalPages);
    }

    return rangeWithDots;
  };

  if (totalItems === 0) return null;

  return (
    <div className="d-flex justify-content-between align-items-center mt-4">
      <div className="d-flex align-items-center">
        <select
          className="form-select form-select-sm me-2"
          value={pageSize}
          onChange={handlePageSizeChange}
          style={{ width: '100px' }}
        >
          {pageSizeOptions.map(size => (
            <option key={size} value={size}>
              {size} / page
            </option>
          ))}
        </select>
        <span className="text-muted">
          Showing {((currentPage - 1) * pageSize) + 1} to {Math.min(currentPage * pageSize, totalItems)} of {totalItems} entries
        </span>
      </div>

      <nav aria-label="Job list pagination">
        <ul className="pagination pagination-sm mb-0">
          <li className={`page-item ${currentPage === 1 ? 'disabled' : ''}`}>
            <button
              className="page-link"
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage === 1}
            >
              Previous
            </button>
          </li>

          {getPageNumbers().map((page, index) => (
            <li 
              key={index} 
              className={`page-item ${page === currentPage ? 'active' : ''} ${page === '...' ? 'disabled' : ''}`}
            >
              <button
                className="page-link"
                onClick={() => page !== '...' && handlePageChange(page)}
              >
                {page}
              </button>
            </li>
          ))}

          <li className={`page-item ${currentPage === totalPages ? 'disabled' : ''}`}>
            <button
              className="page-link"
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={currentPage === totalPages}
            >
              Next
            </button>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default Pagination;