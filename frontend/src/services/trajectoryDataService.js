// File: src/services/trajectoryDataService.js
import Papa from 'papaparse';
import * as XLSX from 'xlsx';
import api from './api';

const trajectoryDataService = {
  importFromCSV: async (file) => {
    return new Promise((resolve, reject) => {
      Papa.parse(file, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
        complete: (results) => {
          if (results.errors.length > 0) {
            reject(new Error('Error parsing CSV: ' + results.errors[0].message));
            return;
          }
          resolve(results.data);
        },
        error: (error) => {
          reject(new Error('Error parsing CSV: ' + error.message));
        }
      });
    });
  },

  importFromExcel: async (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = e.target.result;
          const workbook = XLSX.read(data, { type: 'array' });
          const firstSheetName = workbook.SheetNames[0];
          const worksheet = workbook.Sheets[firstSheetName];
          const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
          
          // Convert to proper format
          const headers = jsonData[0];
          const rows = jsonData.slice(1).map(row => {
            const obj = {};
            headers.forEach((header, index) => {
              obj[header] = row[index];
            });
            return obj;
          });
          
          resolve(rows);
        } catch (error) {
          reject(new Error('Error parsing Excel file: ' + error.message));
        }
      };
      reader.onerror = (error) => {
        reject(new Error('Error reading file: ' + error.message));
      };
      reader.readAsArrayBuffer(file);
    });
  },

  exportToCSV: (data) => {
    const csv = Papa.unparse(data);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    return blob;
  },

  exportToExcel: (data) => {
    const ws = XLSX.utils.json_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Trajectory Data");
    const excelBuffer = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });
    const blob = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    return blob;
  },

  validateImportedData: (data) => {
    const errors = [];
    const requiredFields = ['measured_depth', 'inclination', 'azimuth'];

    // Check for required fields
    data.forEach((row, index) => {
      requiredFields.forEach(field => {
        if (row[field] === undefined || row[field] === null || row[field] === '') {
          errors.push(`Row ${index + 1}: Missing required field '${field}'`);
        }
      });

      // Validate numeric values
      if (row.measured_depth !== undefined && isNaN(parseFloat(row.measured_depth))) {
        errors.push(`Row ${index + 1}: Measured depth must be a number`);
      }
      if (row.inclination !== undefined && (isNaN(parseFloat(row.inclination)) || row.inclination < 0 || row.inclination > 180)) {
        errors.push(`Row ${index + 1}: Inclination must be a number between 0 and 180`);
      }
      if (row.azimuth !== undefined && (isNaN(parseFloat(row.azimuth)) || row.azimuth < 0 || row.azimuth > 360)) {
        errors.push(`Row ${index + 1}: Azimuth must be a number between 0 and 360`);
      }
    });

    return errors;
  },

  downloadFile: (blob, filename) => {
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  },

  createTrajectoryData: async (trajectoryData) => {
    try {
      const response = await api.post('/trajectory-data', trajectoryData);
      return response.data;
    } catch (error) {
      console.error('Error creating trajectory data:', error);
      throw error;
    }
  },

  getTrajectoryData: async (params = {}) => {
    try {
      const response = await api.get('/trajectory-data', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching trajectory data:', error);
      throw error;
    }
  },

  getTrajectoryDataById: async (dataId) => {
    try {
      const response = await api.get(`/trajectory-data/${dataId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching trajectory data details:', error);
      throw error;
    }
  },

  updateTrajectoryData: async (dataId, trajectoryData) => {
    try {
      const response = await api.put(`/trajectory-data/${dataId}`, trajectoryData);
      return response.data;
    } catch (error) {
      console.error('Error updating trajectory data:', error);
      throw error;
    }
  },

  deleteTrajectoryData: async (dataId) => {
    try {
      await api.delete(`/trajectory-data/${dataId}`);
      return true;
    } catch (error) {
      console.error('Error deleting trajectory data:', error);
      throw error;
    }
  }
};

export default trajectoryDataService;