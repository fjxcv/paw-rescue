import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { authAPI } from '../api/api';
import { isAdminUser } from '../components/AdminRoute';

const ManageModeContext = createContext({
  isAdmin: false,
  manageMode: false,
  canManage: false,
  setManageMode: () => {},
  refreshAdmin: () => {},
});

export const ManageModeProvider = ({ children }) => {
  const [isAdmin, setIsAdmin] = useState(false);
  const [manageMode, setManageModeState] = useState(
    () => localStorage.getItem('manageMode') === '1',
  );

  const refreshAdmin = useCallback(async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      setIsAdmin(false);
      return;
    }
    try {
      const res = await authAPI.getProfile();
      setIsAdmin(isAdminUser(res.data));
    } catch {
      setIsAdmin(false);
    }
  }, []);

  useEffect(() => {
    refreshAdmin();
    const onStorage = () => refreshAdmin();
    window.addEventListener('storage', onStorage);
    return () => window.removeEventListener('storage', onStorage);
  }, [refreshAdmin]);

  const setManageMode = useCallback((on) => {
    setManageModeState(on);
    localStorage.setItem('manageMode', on ? '1' : '0');
  }, []);

  const value = useMemo(
    () => ({
      isAdmin,
      manageMode,
      canManage: isAdmin && manageMode,
      setManageMode,
      refreshAdmin,
    }),
    [isAdmin, manageMode, setManageMode, refreshAdmin],
  );

  return (
    <ManageModeContext.Provider value={value}>
      {children}
    </ManageModeContext.Provider>
  );
};

export const useManageMode = () => useContext(ManageModeContext);
