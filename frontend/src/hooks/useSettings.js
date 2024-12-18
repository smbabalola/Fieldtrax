import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { 
  fetchSettings, 
  updateSettings, 
  selectSettings, 
  selectIsLoading,
  selectError,
  setTheme,
  setDisplaySettings,
  resetSettings 
} from '../store/slices/settingsSlice';

export const useSettings = () => {
  const dispatch = useDispatch();
  const settings = useSelector(selectSettings);
  const isLoading = useSelector(selectIsLoading);
  const error = useSelector(selectError);

  useEffect(() => {
    // Load settings on initial mount if not already loaded
    if (!settings.lastUpdated) {
      dispatch(fetchSettings());
    }
  }, [dispatch, settings.lastUpdated]);

  const updateTheme = async (themeSettings) => {
    try {
      dispatch(setTheme(themeSettings));
      await dispatch(updateSettings({ 
        ...settings, 
        theme: { ...settings.theme, ...themeSettings } 
      })).unwrap();
    } catch (error) {
      console.error('Failed to update theme:', error);
      throw error;
    }
  };

  const updateDisplay = async (displaySettings) => {
    try {
      dispatch(setDisplaySettings(displaySettings));
      await dispatch(updateSettings({
        ...settings,
        display: { ...settings.display, ...displaySettings }
      })).unwrap();
    } catch (error) {
      console.error('Failed to update display settings:', error);
      throw error;
    }
  };

  const updateNotifications = async (notificationSettings) => {
    try {
      await dispatch(updateSettings({
        ...settings,
        notifications: { ...settings.notifications, ...notificationSettings }
      })).unwrap();
    } catch (error) {
      console.error('Failed to update notification settings:', error);
      throw error;
    }
  };

  const updateLocale = async (localeSettings) => {
    try {
      await dispatch(updateSettings({
        ...settings,
        locale: { ...settings.locale, ...localeSettings }
      })).unwrap();
    } catch (error) {
      console.error('Failed to update locale settings:', error);
      throw error;
    }
  };

  const updateJobDefaults = async (jobSettings) => {
    try {
      await dispatch(updateSettings({
        ...settings,
        jobDefaults: { ...settings.jobDefaults, ...jobSettings }
      })).unwrap();
    } catch (error) {
      console.error('Failed to update job default settings:', error);
      throw error;
    }
  };

  const resetAllSettings = async () => {
    try {
      await dispatch(resetSettings()).unwrap();
      await dispatch(fetchSettings()).unwrap();
    } catch (error) {
      console.error('Failed to reset settings:', error);
      throw error;
    }
  };

  return {
    settings,
    isLoading,
    error,
    updateTheme,
    updateDisplay,
    updateNotifications,
    updateLocale,
    updateJobDefaults,
    resetAllSettings
  };
};

export default useSettings;
