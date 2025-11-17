"use client";

import { createContext, useState, useContext, ReactNode } from "react";
import { SolicitudReceta } from "../interfaces/SolicitudReceta";
import { Especificaciones } from './../interfaces/Especificaciones';

// Tipos para el context
interface EspecificacionesContextType {
  especificaciones: Especificaciones | null;
  setEspecificaciones: (especificacionesa: Especificaciones) => void;
}

// Contexto con valor inicial vacío
const EspecificacionesContext = createContext<EspecificacionesContextType | undefined>(undefined);

// Provider
export const EspecificacionesProvider = ({ children }: { children: ReactNode }) => {
  const [especificaciones, setEspecificaciones] = useState<Especificaciones | null>(null);
  return (
    <EspecificacionesContext.Provider value={{especificaciones, setEspecificaciones }}>
      {children}
    </EspecificacionesContext.Provider>
  );
};

// Hook para usar el context fácilmente
export const useSolicitudReceta = () => {
  const context = useContext(EspecificacionesContext);
  return context;
};
