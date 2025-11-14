"use client";

import { createContext, useState, useContext, ReactNode } from "react";
import { Comida } from "../Comida";

// Tipos para el context
interface ComidaContextType {
  comida: Comida | null;
  setComida: (comida: Comida) => void;
}

// Contexto con valor inicial vacío
const ComidaContext = createContext<ComidaContextType | undefined>(undefined);

// Provider
export const ComidaProvider = ({ children }: { children: ReactNode }) => {
  const [comida, setComida] = useState<Comida | null>(null);
  return (
    <ComidaContext.Provider value={{ comida, setComida }}>
      {children}
    </ComidaContext.Provider>
  );
};

// Hook para usar el context fácilmente
export const useComida = () => {
  const context = useContext(ComidaContext);
  if (!context) {
    throw new Error("useComida debe usarse dentro de ComidaProvider");
  }
  return context;
};
