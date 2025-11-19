import { Receta } from "./Receta";

export interface Conversacion {
  id: string;
  titulo: string; // Ej: "Paella Valenciana"
  fecha: string;
  receta: Receta;
}