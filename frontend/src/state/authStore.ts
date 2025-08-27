import { create } from 'zustand'; // Changed from default to named import
import { persist } from 'zustand/middleware';

// Exporting the interface allows other files to use this type
export interface AuthState {
  token: string | null;
  setToken: (token: string) => void; // Added 'string' type to the token parameter
  clearToken: () => void;
}

const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      setToken: (token) => set({ token }),
      clearToken: () => set({ token: null }),
    }),
    {
      name: 'auth-storage',
    }
  )
);

export default useAuthStore;