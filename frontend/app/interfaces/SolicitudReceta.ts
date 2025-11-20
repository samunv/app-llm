import { Especificaciones } from "./Especificaciones";

export interface SolicitudReceta {
  comida: string;
  modeloIASeleccionado: string;
  imagen?: string;
  tipoImagen?: string;
  especificaciones?: Especificaciones;
  historial?: Array<{ role: string; parts: { text: string }[] }>;
}