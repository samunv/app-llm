"use client";

import { createContext, useState, useContext, ReactNode } from "react";
import { SolicitudReceta } from "./../interfaces/SolicitudReceta";

// Tipos para el context
interface SolicitudRecetaContextType {
  solicitudReceta: SolicitudReceta | null;
  setSolicitudReceta: React.Dispatch<
    React.SetStateAction<SolicitudReceta | null>
  >;
  updateSolicitudReceta: (
    claveActualizar: string,
    valorActualizar: string
  ) => void;
  modeloSeleccionadoID: string;
  setModeloSeleccionadoID: (modelo: string) => void;
}

// Contexto con valor inicial vacío
const SolicitudRecetaContext = createContext<
  SolicitudRecetaContextType | undefined
>(undefined);

// Provider
export const SolicitudRecetaProvider = ({
  children,
}: {
  children: ReactNode;
}) => {
  const [solicitudReceta, setSolicitudReceta] =
    useState<SolicitudReceta | null>(null);

  const [modeloSeleccionadoID, setModeloSeleccionadoID] = useState<string>("");

  const updateSolicitudReceta = (
    claveActualizar: string,
    valorActualizar: string
  ) => {
    setSolicitudReceta((solicitudPrevia) => {
      if (!solicitudPrevia) {
        return {
          [claveActualizar]: valorActualizar,
          modeloIASeleccionado: modeloSeleccionadoID,
          especificaciones: undefined,
          imagen: undefined,
        };
      }
      return {
        ...solicitudPrevia,
        modeloIASeleccionado: modeloSeleccionadoID,
        [claveActualizar]: valorActualizar,
      };
    });
  };

  return (
    <SolicitudRecetaContext.Provider
      value={{
        solicitudReceta,
        setSolicitudReceta,
        updateSolicitudReceta,
        modeloSeleccionadoID,
        setModeloSeleccionadoID,
      }}
    >
      {children}
    </SolicitudRecetaContext.Provider>
  );
};

// Hook para usar el context fácilmente
export const useSolicitudReceta = () => {
  const context = useContext(SolicitudRecetaContext);
  if (context === undefined) {
    throw new Error(
      "useSolicitudReceta debe usarse dentro de un SolicitudRecetaProvider"
    );
  }
  return context;
};
