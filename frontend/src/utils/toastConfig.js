// File: /src/utils/toastConfig.js
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const defaultConfig = {
  position: "top-right",
  autoClose: 5000,
  hideProgressBar: false,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true
};

export const showToast = {
  success: (message) => toast.success(message, defaultConfig),
  error: (message) => toast.error(message, defaultConfig),
  info: (message) => toast.info(message, defaultConfig),
  warning: (message) => toast.warning(message, defaultConfig)
};

export default showToast;