"use client";

import { createContext, useState, useContext, ReactNode } from "react";
import { SolicitudReceta } from './../interfaces/SolicitudReceta';

// Tipos para el context
interface SolicitudRecetaContextType {
  solicitudReceta: SolicitudReceta | null;
  setSolicitudReceta: React.Dispatch<React.SetStateAction<SolicitudReceta | null>>;
}

// Contexto con valor inicial vacío
const SolicitudRecetaContext = createContext<SolicitudRecetaContextType | undefined>(undefined);

// Provider
export const SolicitudRecetaProvider = ({ children }: { children: ReactNode }) => {
  const [solicitudReceta, setSolicitudReceta] = useState<SolicitudReceta | null>(null);
  return (
    <SolicitudRecetaContext.Provider value={{ solicitudReceta, setSolicitudReceta }}>
      {children}
    </SolicitudRecetaContext.Provider>
  );
};

// Hook para usar el context fácilmente
export const useSolicitudReceta = () => {
  const context = useContext(SolicitudRecetaContext);
    if (context === undefined) {
        throw new Error('useSolicitudReceta debe usarse dentro de un SolicitudRecetaProvider');
    }
  return context;
};
