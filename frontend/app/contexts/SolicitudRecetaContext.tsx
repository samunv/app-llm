"use client";

import { createContext, useState, useContext, ReactNode, useCallback } from "react";
import { SolicitudReceta } from "./../interfaces/SolicitudReceta";
import { Especificaciones } from "../interfaces/Especificaciones";

// Tipos para el context
interface SolicitudRecetaContextType {
  solicitudReceta: SolicitudReceta | null;
  setSolicitudReceta: React.Dispatch<
    React.SetStateAction<SolicitudReceta | null>
  >;
  updateSolicitudReceta: (
    claveActualizar: string,
    valorActualizar: string | Especificaciones
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

  const [modeloSeleccionadoID, setModeloSeleccionadoID] = useState<string>("gemini-2.5-flash");

  const updateSolicitudReceta = useCallback(
    (claveActualizar: string, valorActualizar: string | Especificaciones) => {
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
          [claveActualizar]: valorActualizar,
        };
      });
    },
    [modeloSeleccionadoID] // Solo se redefine si cambia el ID
  );

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
