import { Especificaciones } from './Especificaciones';

export interface SolicitudReceta {
    comida: string,
    especificaciones: Especificaciones | undefined,
    modeloIASeleccionado: string
}