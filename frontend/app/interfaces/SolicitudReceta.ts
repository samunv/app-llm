import { Especificaciones } from "./Especificaciones";
import { PerfilUsuario } from "./PerfilUsuario";

export interface SolicitudReceta {
  comida: string;
  modeloIASeleccionado: string;
  imagen?: string;
  tipoImagen?: string;
  especificaciones?: Especificaciones;
  historial?: Array<{ role: string; parts: { text: string }[] }>; // <--- NUEVO CAMPO
  perfilUsuario?: PerfilUsuario;
}