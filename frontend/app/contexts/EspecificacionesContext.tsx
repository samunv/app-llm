"use client";

import { createContext, ReactNode, useCallback, useContext, useState } from "react";
import { Especificaciones } from '../interfaces/Especificaciones';

interface EspecificacionesContextType {
  especificaciones: Especificaciones | null;
  setEspecificaciones: (esp: Especificaciones) => void;
  updateEspecificaciones: (
    claveActualizar: string,
    valorActualizar: string
  ) => void;
}

const EspecificacionesContext =
  createContext<EspecificacionesContextType | undefined>(undefined);

export const EspecificacionesProvider = ({children}:{
  children: ReactNode;
})=>{

  const [especificaciones, setEspecificaciones] = useState<Especificaciones | null>(null)

  const updateEspecificaciones = useCallback(
      (claveActualizar: string, valorActualizar: string) => {
        setEspecificaciones((espPrevias) => {
          if (!espPrevias) {
            return {
              [claveActualizar]: valorActualizar,
            };
          }
          return {
            ...espPrevias,
            [claveActualizar]: valorActualizar,
          };
        });
      },
      []
    );

  return (
    <EspecificacionesContext.Provider value={{especificaciones, setEspecificaciones, updateEspecificaciones}}>
{children}
    </EspecificacionesContext.Provider>
  )
}
export const useEspecificaciones = ()=>{
  const context = useContext(EspecificacionesContext);
    if (context === undefined) {
      throw new Error(
        "Error"
      );
    }
    return context;
}