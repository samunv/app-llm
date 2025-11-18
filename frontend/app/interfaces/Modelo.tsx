import { JSX } from "react";

export interface Modelo {
  id: string;
  nombre: string;
  version: string;
  descripcion: string;
  velocidad: "ultrarrápido" | "rápido" | "equilibrado" | "potente";
  icono: JSX.Element;
  color: string;
  recomendado?: boolean;
}